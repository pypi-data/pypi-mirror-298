from importlib import import_module
from pkgutil import walk_packages
from typing import Type

from lcmutils.typing import LCMType


class LCMTypeRegistry:
    """
    Registry of LCM types. Key-value pairs are stored as (fingerprint, class).
    """

    def __init__(self, *classes: tuple[LCMType]) -> None:
        self._registry: dict[bytes, LCMType] = {}

        for cls in classes:
            self.register(cls)

    def register(self, cls: LCMType) -> None:
        """
        Register an LCM type class.

        Args:
            cls (LCMType): LCM class to register.
        """
        self._registry[cls._get_packed_fingerprint()] = cls

    @property
    def types(self) -> list[LCMType]:
        """
        Get the list of registered LCM types.

        Returns:
            list[LCMType]: List of registered LCM types.
        """
        return list(self._registry.values())

    def clear(self) -> None:
        """
        Clear the registry.
        """
        self._registry.clear()

    def get(self, fingerprint: bytes) -> LCMType | None:
        """
        Get the LCM class associated with a fingerprint.

        Args:
            fingerprint (bytes): Fingerprint to look up.

        Returns:
            LCMType | None: LCM type class associated with the fingerprint, or None if no class is registered for the fingerprint.
        """
        return self._registry.get(fingerprint, None)

    def detect(self, data: bytes) -> Type[LCMType]:
        """
        Detect the LCM type class associated with LCM message data.
        
        Args:
            data (bytes): LCM message data.
        
        Returns:
            Type[LCMType]: LCM type class associated with the data.
        """
        fingerprint = data[:8]
        cls = self.get(fingerprint)
        return cls

    def decode(self, data: bytes) -> LCMType | None:
        """
        Decode data into an LCM type instance, if its class is registered.

        Args:
            data (bytes): LCM data to decode.

        Returns:
            LCMType | None: Decoded instance, or None if the class is not registered.
        """
        cls = self.detect(data)

        if cls is None:
            return None

        return cls.decode(data)

    def discover(self, package_name: str):
        """
        Discover LCM type classes in a Python package by name.

        Args:
            package_name (str): Package to discover.

        Raises:
            PackageNotFoundError: If the package is not found.
        """
        package = import_module(package_name)

        for loader, module_name, _ in walk_packages(package.__path__):
            module = loader.find_module(module_name).load_module(module_name)

            for name in dir(module):
                cls = getattr(module, name)

                if isinstance(cls, type) and issubclass(cls, LCMType):
                    self.register(cls)


__all__ = ["LCMTypeRegistry"]
