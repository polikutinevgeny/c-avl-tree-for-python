import unittest
from map import map


class CMapTests(unittest.TestCase):
    def test_construction(self):
        m = map()
        self.assertTrue(m.cmap)

    def test_insertion(self):
        m = map()
        m[1] = 12
        m[5] = 17
        m[2] = 13
        m[4] = 16
        self.assertEqual(m[1], 12)
        self.assertEqual(m[2], 13)
        self.assertEqual(m[4], 16)
        self.assertEqual(m[5], 17)


if __name__ == '__main__':
    unittest.main()
