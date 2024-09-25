from kommonlib.registry.namespace import NamespaceKey, AbstractNamespaceRegistry


class TestableNamespaceRegistry(AbstractNamespaceRegistry):
    __test__ = False

    def _is_bidirectional(self) -> bool:
        return False

    def _is_unique(self) -> bool:
        return False


class TestNamespaceKey:
    def test_create_namespace_key(self):
        ns_key = NamespaceKey("namespace", "key")

        assert ns_key.namespace() == "namespace"
        assert ns_key.key() == "key"

    def test_namespace_key_to_any_namespace(self):
        ns_key = NamespaceKey("namespace", "key").to_any_namespace()

        assert ns_key.namespace() == "*"
        assert ns_key.key() == "key"

    def test_namespace_key_str(self):
        ns_key = NamespaceKey("namespace", "key")

        assert str(ns_key) == "namespace/key"

    def test_namespace_key_hash(self):
        ns_key = NamespaceKey("namespace", "key")

        assert hash(ns_key) == hash("namespace/key")

    def test_namespace_key_equals(self):
        ns_key1 = NamespaceKey("namespace", "key")
        ns_key2 = NamespaceKey("namespace", "key")

        ns_key3 = NamespaceKey("namespace1", "key")
        ns_key4 = NamespaceKey("namespace", "key1")

        not_ns_key = "namespace/key"

        assert ns_key1 == ns_key2
        assert ns_key1 != ns_key3
        assert ns_key1 != ns_key4

        assert ns_key1 != not_ns_key


class TestNamespaceRegistry:
    def test_returns_value_when_key_found(self):
        key = NamespaceKey("namespace", "key")

        registry = TestableNamespaceRegistry()

        registry.register(key, "value1")

        result = registry.find_by_key_globally(key)

        assert result == "value1"

    def test_returns_value_when_key_found_in_global_namespace(self):
        key = NamespaceKey("namespace", "key")

        registry = TestableNamespaceRegistry()

        registry.register(key.to_any_namespace(), "value1")

        result = registry.find_by_key_globally(key)

        assert result == "value1"

    def test_returns_none_when_key_not_found(self):
        key = NamespaceKey("namespace", "key")

        registry = TestableNamespaceRegistry()

        result = registry.find_by_key_globally(key)

        assert result is None

    def test_returns_values_when_key_found(self):
        key = NamespaceKey("namespace1", "key1")

        registry = TestableNamespaceRegistry()

        registry.register(key, "value1")
        registry.register(key, "value2")
        registry.register(key.to_any_namespace(), "value2")
        registry.register(key.to_any_namespace(), "value3")

        result = registry.get_by_key_globally(key)

        assert result == ["value1", "value2", "value3"]

    def test_returns_empty_list_when_key_not_found(self):
        registry = TestableNamespaceRegistry()

        key = NamespaceKey("namespace1", "key1")
        nonexistent_key = NamespaceKey("namespace1", "nonexistent_key")

        registry.register(key, "value1")
        registry.register(key, "value2")
        registry.register(key.to_any_namespace(), "value2")
        registry.register(key.to_any_namespace(), "value3")

        result = registry.get_by_key_globally(nonexistent_key)

        assert result == []
