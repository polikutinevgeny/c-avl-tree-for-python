import unittest
from map import map


class CMapTests(unittest.TestCase):
    def test_construction(self):
        m = map()
        self.assertTrue(m.cmap)

    def test_set_and_get(self):
        m = map()
        m[1] = 12
        m[5] = 17
        m[2] = 13
        m[4] = 16
        self.assertEqual(m[1], 12)
        self.assertEqual(m[2], 13)
        self.assertEqual(m[4], 16)
        self.assertEqual(m[5], 17)

    def test_len(self):
        m = map()
        m[1] = 12
        m[5] = 17
        m[2] = 13
        m[4] = 16
        self.assertEqual(len(m), 4)

    def test_delitem(self):
        m = map()
        m[1] = 12
        m[5] = 17
        m[2] = 13
        m[4] = 16
        del m[2]
        self.assertEqual(len(m), 3)
        self.assertEqual(m[1], 12)
        self.assertEqual(m[4], 16)
        self.assertEqual(m[5], 17)

    def test_contains(self):
        m = map()
        m[1] = 12
        m[5] = 17
        m[2] = 13
        m[4] = 16
        self.assertTrue(2 in m)
        self.assertFalse(3 in m)

    def test_clear(self):
        m = map()
        m[1] = 12
        m[5] = 17
        m[2] = 13
        m[4] = 16
        m.clear()
        self.assertEqual(len(m), 0)

    def test_copy(self):
        m = map()
        m[1] = 12
        m[5] = 17
        m[2] = 13
        m[4] = 16
        c = m.copy()
        self.assertEqual(m[1], 12)
        self.assertEqual(m[2], 13)
        self.assertEqual(m[4], 16)
        self.assertEqual(m[5], 17)
        self.assertEqual(c[1], 12)
        self.assertEqual(c[2], 13)
        self.assertEqual(c[4], 16)
        self.assertEqual(c[5], 17)
        self.assertEqual(len(m), 4)
        self.assertEqual(len(c), 4)

    def test_get(self):
        m = map()
        m[1] = 12
        m[5] = 17
        m[2] = 13
        m[4] = 16
        self.assertEqual(m.get(1), 12)
        self.assertEqual(m.get(3), None)

    def test_items(self):
        m = map()
        m[1] = 12
        m[5] = 17
        m[2] = 13
        m[4] = 16
        self.assertEqual(m.items(), [(1, 12), (2, 13), (4, 16), (5, 17)])

    def test_keys(self):
        m = map()
        m[1] = 12
        m[5] = 17
        m[2] = 13
        m[4] = 16
        self.assertEqual(m.keys(), [1, 2, 4, 5])

    def test_values(self):
        m = map()
        m[1] = 12
        m[5] = 17
        m[2] = 13
        m[4] = 16
        self.assertEqual(m.values(), [12, 13, 16, 17])

    def test_pop(self):
        m = map()
        m[1] = 12
        m[5] = 17
        m[2] = 13
        m[4] = 16
        self.assertEqual(m.pop(2), 13)
        self.assertEqual(len(m), 3)
        self.assertEqual(m.pop(3), None)
        self.assertEqual(len(m), 3)

    def test_iter(self):
        m = map()
        m[1] = 12
        m[5] = 17
        m[2] = 13
        m[4] = 16
        a = []
        for i in m:
            a.append(i)
        self.assertEqual(a, [1, 2, 4, 5])


if __name__ == '__main__':
    unittest.main()
