import unittest

from src.utils import flatten


class Test_utils(unittest.TestCase):
    def test_flatten(self):
        self.assertEqual((1, 2, 3, 4), flatten(((1, 2), (), (3,), 4)))
        self.assertIsInstance(flatten([1, 2, [3, 4]]), list)
