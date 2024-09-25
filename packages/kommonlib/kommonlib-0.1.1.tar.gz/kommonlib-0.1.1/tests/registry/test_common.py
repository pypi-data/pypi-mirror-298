import pytest

from kommonlib.registry import AbstractRegistry


class TestableAbstractRegistry(AbstractRegistry[str, str]):
    __test__ = False

    def __init__(self, is_bidirectional: bool, is_unique: bool):
        self._is_bidirectional_var = is_bidirectional
        self._is_unique_var = is_unique

        super().__init__()

    def _is_bidirectional(self) -> bool:
        return self._is_bidirectional_var

    def _is_unique(self) -> bool:
        return self._is_unique_var

    def default_is_bidirectional(self) -> bool:
        return super()._is_bidirectional()

    def default_is_unique(self) -> bool:
        return super()._is_unique()


class TestAbstractRegistry(object):
    def test_assert_defaults(self):
        registry = TestableAbstractRegistry(False, False)

        assert registry.default_is_bidirectional() is False
        assert registry.default_is_unique() is False

    def test_register_bidirectional_not_unique(self):
        registry = TestableAbstractRegistry(True, False)

        registry.register("key1", "value1")
        registry.register("key1", "value2")
        registry.register("key2", "value1")
        registry.register("key2", "value2")

        assert registry.get_by_key("key1") == ["value1", "value2"]
        assert registry.get_by_key("key2") == ["value1", "value2"]
        assert registry.get_by_value("value1") == ["key1", "key2"]
        assert registry.get_by_value("value2") == ["key1", "key2"]

    def test_register_bidirectional_not_unique_does_not_duplicate_data(self):
        registry = TestableAbstractRegistry(True, False)

        registry.register("key1", "value1")
        registry.register("key1", "value1")

        registry.register("key1", "value1")
        registry.register("key1", "value2")
        registry.register("key1", "value3")

        registry.register("key1", "value1")
        registry.register("key2", "value1")
        registry.register("key3", "value1")

        assert registry.get_keys() == ["key1", "key2", "key3"]
        assert registry.get_values() == ["value1", "value2", "value3"]

    def test_register_bidirectional_unique(self):
        registry = TestableAbstractRegistry(True, True)

        registry.register("key1", "value1")
        registry.register("key2", "value2")

        assert registry.get_by_key("key1") == ["value1"]
        assert registry.get_by_key("key2") == ["value2"]
        assert registry.get_by_value("value1") == ["key1"]
        assert registry.get_by_value("value2") == ["key2"]

    def test_register_bidirectional_unique_does_not_duplicate_data(self):
        registry = TestableAbstractRegistry(True, True)

        registry.register("key1", "value1")

        with pytest.raises(KeyError):
            registry.register("key1", "value2")
        with pytest.raises(ValueError):
            registry.register("key2", "value1")

        assert registry.get_keys() == ["key1"]
        assert registry.get_values() == ["value1"]

    def test_register_unidirectional(self):
        registry = TestableAbstractRegistry(False, False)

        registry.register("key1", "value1")
        registry.register("key1", "value2")
        registry.register("key2", "value1")
        registry.register("key2", "value2")

        with pytest.raises(RuntimeError):
            registry.get_by_value("value1")
        with pytest.raises(RuntimeError):
            registry.get_by_value("value2")

        assert registry.get_by_key("key1") == ["value1", "value2"]
        assert registry.get_by_key("key2") == ["value1", "value2"]

    def test_unregister_bidirectional(self):
        registry = TestableAbstractRegistry(True, False)

        registry._registry["key1"] = ["value1"]
        registry._registry["key2"] = ["value2"]

        registry._reverse_registry["value1"] = ["key1"]
        registry._reverse_registry["value2"] = ["key2"]

        registry.unregister("key1", "value1")

        assert not registry.is_key_registered("key1")
        assert not registry.is_value_registered("value1")

        assert registry.is_key_registered("key2")
        assert registry.is_value_registered("value2")

    def test_unregister_unidirectional(self):
        registry = TestableAbstractRegistry(False, False)

        registry._registry["key1"] = ["value1"]
        registry._registry["key2"] = ["value2"]

        registry.unregister("key1", "value1")

        assert not registry.is_key_registered("key1")

        assert registry.is_key_registered("key2")

    def test_is_registered_bidirectional(self):
        registry = TestableAbstractRegistry(True, False)

        assert registry.is_key_registered("key1") is False
        assert registry.is_value_registered("value1") is False

        registry._registry["key1"] = ["value1", "value2"]
        registry._registry["key2"] = ["value2"]

        registry._reverse_registry["value1"] = ["key1"]
        registry._reverse_registry["value2"] = ["key1", "key2"]

        assert registry.is_key_registered("key1") is True
        assert registry.is_value_registered("value1") is True

        assert registry.is_key_registered("key2") is True
        assert registry.is_value_registered("value2") is True

        assert registry.is_key_registered("key3") is False
        assert registry.is_value_registered("value3") is False

    def test_is_registered_unidirectional(self):
        registry = TestableAbstractRegistry(False, False)

        assert registry.is_key_registered("key1") is False
        assert registry.is_value_registered("value1") is False

        registry._registry["key1"] = ["value1"]

        assert registry.is_key_registered("key1") is True
        assert (
            registry.is_value_registered("value1") is False
        )  # always false for unidirectional registries

    def test_get_by(self):
        registry = TestableAbstractRegistry(True, False)

        registry._registry["key1"] = ["value1", "value2"]
        registry._registry["key2"] = ["value2"]

        registry._reverse_registry["value1"] = ["key1"]
        registry._reverse_registry["value2"] = ["key1", "key2"]

        assert registry.get_by_key("key1") == ["value1", "value2"]
        assert registry.get_by_key("key2") == ["value2"]

        assert registry.get_by_value("value1") == ["key1"]
        assert registry.get_by_value("value2") == ["key1", "key2"]

    def test_get_all_by(self):
        registry = TestableAbstractRegistry(True, False)

        registry._registry["key1"] = ["value1", "value2"]
        registry._registry["key2"] = ["value2"]

        registry._reverse_registry["value1"] = ["key1"]
        registry._reverse_registry["value2"] = ["key1", "key2"]

        assert registry.get_all_by_key() == {
            "key1": ["value1", "value2"],
            "key2": ["value2"],
        }
        assert registry.get_all_by_value() == {
            "value1": ["key1"],
            "value2": ["key1", "key2"],
        }

    def test_get_keys_or_values(self):
        registry = TestableAbstractRegistry(True, False)

        registry._registry["key1"] = ["value1", "value2"]
        registry._registry["key2"] = ["value2"]

        registry._reverse_registry["value1"] = ["key1"]
        registry._reverse_registry["value2"] = ["key1", "key2"]

        assert registry.get_keys() == ["key1", "key2"]
        assert registry.get_values() == ["value1", "value2"]

    def test_find_by(self):
        registry = TestableAbstractRegistry(True, False)

        registry._registry["key1"] = ["value1", "value2"]
        registry._registry["key2"] = ["value2"]

        registry._reverse_registry["value1"] = ["key1"]
        registry._reverse_registry["value2"] = ["key1", "key2"]

        assert registry.find_by_key("key_") is None
        assert registry.find_by_value("value_") is None

        assert registry.find_by_key("key2") == "value2"
        assert registry.find_by_value("value1") == "key1"

        with pytest.raises(KeyError):
            registry.find_by_key("key1")
        with pytest.raises(ValueError):
            registry.find_by_value("value2")

    def test_clear(self):
        registry = TestableAbstractRegistry(True, False)

        registry._registry["key1"] = ["value1", "value2"]
        registry._registry["key2"] = ["value2"]

        registry._reverse_registry["value1"] = ["key1"]
        registry._reverse_registry["value2"] = ["key1", "key2"]

        registry.clear()

        assert registry.get_keys() == []
        assert registry.get_values() == []

    def test_update(self):
        registry = TestableAbstractRegistry(True, False)

        registry._registry["key1"] = ["value1", "value2"]
        registry._registry["key2"] = ["value2"]

        registry._reverse_registry["value1"] = ["key1"]
        registry._reverse_registry["value2"] = ["key1", "key2"]

        data = {"key2": ["value2", "value5", "value6"], "key5": ["value1", "value5"]}
        registry.update(data)

        assert registry.get_by_key("key1") == ["value1", "value2"]
        assert registry.get_by_key("key2") == ["value2", "value5", "value6"]
        assert registry.get_by_key("key5") == ["value1", "value5"]

        assert registry.get_by_value("value1") == ["key1", "key5"]
        assert registry.get_by_value("value2") == ["key1", "key2"]
        assert registry.get_by_value("value5") == ["key2", "key5"]
        assert registry.get_by_value("value6") == ["key2"]

    def test_set(self):
        registry = TestableAbstractRegistry(True, False)

        registry._registry["key1"] = ["value1", "value2"]
        registry._registry["key2"] = ["value2"]

        registry._reverse_registry["value1"] = ["key1"]
        registry._reverse_registry["value2"] = ["key1", "key2"]

        data = {"key3": ["value2", "value5"], "key5": ["value1", "value5"]}
        registry.set(data)

        assert registry.get_keys() == ["key3", "key5"]
        assert registry.get_values() == ["value2", "value5", "value1"]
        assert registry.get_by_key("key3") == ["value2", "value5"]
        assert registry.get_by_key("key5") == ["value1", "value5"]

        assert registry.get_by_value("value1") == ["key5"]
        assert registry.get_by_value("value2") == ["key3"]
        assert registry.get_by_value("value5") == ["key3", "key5"]
