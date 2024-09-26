from sheepy.sheeptest import SheepyTestCase
from ..sheepy.core.indexer import TestIndexer

class TestTestIndexer(SheepyTestCase):
    def setUp(self):
        self.indexer = TestIndexer()

    def tearDown(self):
        pass

    def test_add_test_methods(self):
        class MockTestCase:
            def test_method(self):
                pass

        self.indexer.add_test_methods(MockTestCase)
        self.assertTrue(self.indexer.has_tests())

    def test_get_tests(self):
        class MockTestCase:
            def test_method(self):
                pass

        self.indexer.add_test_methods(MockTestCase)
        tests = self.indexer.get_tests()
        self.assertTrue(len(tests) > 0)
