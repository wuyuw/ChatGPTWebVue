import unittest


class TestHello(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def test_hello(self):
        assert 1+2 == 3
