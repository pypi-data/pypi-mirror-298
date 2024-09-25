from abc import abstractmethod, ABC
from typing import TypeVar, Generic, Optional

REGISTRY_KEY = TypeVar("REGISTRY_KEY", bound=object)
REGISTRY_VALUE = TypeVar("REGISTRY_VALUE", bound=object)


class AbstractRegistry(ABC, Generic[REGISTRY_KEY, REGISTRY_VALUE]):
    def __init__(self) -> None:
        self._registry: dict[REGISTRY_KEY, list[REGISTRY_VALUE]] = {}
        self._reverse_registry: dict[REGISTRY_VALUE, list[REGISTRY_KEY]] = {}

    @abstractmethod
    def _is_bidirectional(self) -> bool:
        return False

    @abstractmethod
    def _is_unique(self) -> bool:
        return False

    def register(self, key: REGISTRY_KEY, value: REGISTRY_VALUE) -> None:
        if self._is_unique():
            if self.is_key_registered(key):
                raise KeyError(f"Key {key} is already registered")
            if self.is_value_registered(value):
                raise ValueError(f"Value {value} is already registered")

        if key not in self._registry:
            self._registry[key] = []
        if value not in self._registry[key]:
            self._registry[key].append(value)

        if not self._is_bidirectional():
            return

        if value not in self._reverse_registry:
            self._reverse_registry[value] = []
        if key not in self._reverse_registry[value]:
            self._reverse_registry[value].append(key)

    def unregister(self, key: REGISTRY_KEY, value: REGISTRY_VALUE) -> None:
        if key in self._registry and value in self._registry[key]:
            self._registry[key].remove(value)

        if not self._is_bidirectional():
            return

        if value in self._reverse_registry and key in self._reverse_registry[value]:
            self._reverse_registry[value].remove(key)

    def is_key_registered(self, key: REGISTRY_KEY) -> bool:
        return len(self._registry.get(key, [])) > 0

    def is_value_registered(self, value: REGISTRY_VALUE) -> bool:
        if not self._is_bidirectional():
            return False

        return len(self._reverse_registry.get(value, [])) > 0

    def get_by_key(self, key: REGISTRY_KEY) -> list[REGISTRY_VALUE]:
        return self._registry.get(key, [])

    def get_by_value(self, value: REGISTRY_VALUE) -> list[REGISTRY_KEY]:
        return self._ensure_bidirectional()._reverse_registry.get(value, [])

    def get_all_by_key(self) -> dict[REGISTRY_KEY, list[REGISTRY_VALUE]]:
        return self._registry

    def get_all_by_value(self) -> dict[REGISTRY_VALUE, list[REGISTRY_KEY]]:
        return self._ensure_bidirectional()._reverse_registry

    def get_keys(self) -> list[REGISTRY_KEY]:
        return list(self._registry.keys())

    def get_values(self) -> list[REGISTRY_VALUE]:
        return list(self._ensure_bidirectional()._reverse_registry.keys())

    def find_by_key(self, key: REGISTRY_KEY) -> Optional[REGISTRY_VALUE]:
        values = self.get_by_key(key)

        if len(values) == 0:
            return None
        if len(values) > 1:
            raise KeyError(f"Multiple values found for key {key}")

        return values[0]

    def find_by_value(self, value: REGISTRY_VALUE) -> Optional[REGISTRY_KEY]:
        values = self.get_by_value(value)

        if len(values) == 0:
            return None
        if len(values) > 1:
            raise ValueError(f"Multiple keys found for value {value}")

        return values[0]

    def clear(self) -> None:
        self._registry.clear()
        self._reverse_registry.clear()

    def update(self, data: dict[REGISTRY_KEY, list[REGISTRY_VALUE]]) -> None:
        for key, values in data.items():
            for value in values:
                self.register(key, value)

    def set(self, data: dict[REGISTRY_KEY, list[REGISTRY_VALUE]]) -> None:
        self.clear()
        self.update(data)

    def _ensure_bidirectional(self):
        if not self._is_bidirectional():
            raise RuntimeError("Registry is not bidirectional")

        return self
