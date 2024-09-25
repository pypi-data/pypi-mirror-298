from abc import ABC
from typing import Optional, OrderedDict, Generic

from kommonlib.registry.common import REGISTRY_KEY, REGISTRY_VALUE, AbstractRegistry


class NamespaceKey(Generic[REGISTRY_KEY]):
    def __init__(self, namespace: str, key: REGISTRY_KEY) -> None:
        self._namespace: str = namespace
        self._key: REGISTRY_KEY = key

    def namespace(self) -> str:
        return self._namespace

    def key(self) -> REGISTRY_KEY:
        return self._key

    def to_any_namespace(self) -> "NamespaceKey":
        return NamespaceKey("*", self._key)

    def __str__(self):
        return f"{self._namespace}/{self._key}"

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return str(self) == str(other)


class AbstractNamespaceRegistry(
    AbstractRegistry[NamespaceKey[REGISTRY_KEY], REGISTRY_VALUE], ABC
):
    def find_by_key_globally(
        self, key: NamespaceKey[REGISTRY_KEY]
    ) -> Optional[REGISTRY_VALUE]:
        value = super().find_by_key(key)
        if value is not None:
            return value

        return super().find_by_key(key.to_any_namespace())

    def get_by_key_globally(
        self, key: NamespaceKey[REGISTRY_KEY]
    ) -> list[REGISTRY_VALUE]:
        result = []

        result.extend(super().get_by_key(key))
        result.extend(super().get_by_key(key.to_any_namespace()))

        return list(OrderedDict.fromkeys(result))
