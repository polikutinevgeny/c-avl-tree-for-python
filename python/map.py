from ctypes import *
import unittest

cmap_lib = CDLL("libc_avl_tree_for_python")


class Map:

    def __init__(self):
        self.cmap = cmap_lib.LSQ_CreateSequence()

    def __del__(self):
        cmap_lib.LSQ_DestroySequence(self.cmap)

    def __len__(self):
        return cmap_lib.LSQ_GetSize(self.cmap)

    def __setitem__(self, key, item):
        it = _MapIterator(cmap_lib.LSQ_GetElementByIndex(self.cmap, c_int(key)))
        if it.is_past_rear():
            cmap_lib.LSQ_InsertElement(self.cmap, c_int(key), c_int(item))
        else:
            it.pointer().contents.value = item

    def __getitem__(self, item):
        it = _MapIterator(cmap_lib.LSQ_GetElementByIndex(self.cmap, c_int(item)))
        if it.is_past_rear():
            raise KeyError
        return it.value()

    def __delitem__(self, key):
        cmap_lib.LSQ_DeleteElement(self.cmap, c_int(key))

    def __contains__(self, item):
        it = _MapIterator(cmap_lib.LSQ_GetElementByIndex(self.cmap, c_int(item)))
        return not it.is_past_rear()

    def clear(self):
        cmap_lib.LSQ_DestroySequence(self.cmap)
        self.cmap = cmap_lib.LSQ_CreateSequence()

    def copy(self):
        new = Map()
        it = _MapIterator(cmap_lib.LSQ_GetFrontElement(self.cmap))
        while not it.is_past_rear():
            new[it.key()] = it.value()
            it.next()
        return new

    def get(self, key, default=None):
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def items(self):
        it = _MapIterator(cmap_lib.LSQ_GetFrontElement(self.cmap))
        while not it.is_past_rear():
            yield it.pair()
            it.next()

    def keys(self):
        it = _MapIterator(cmap_lib.LSQ_GetFrontElement(self.cmap))
        while not it.is_past_rear():
            yield it.key()
            it.next()

    def values(self):
        it = _MapIterator(cmap_lib.LSQ_GetFrontElement(self.cmap))
        while not it.is_past_rear():
            yield it.value()
            it.next()

    def pop(self, key, default=None):
        it = _MapIterator(cmap_lib.LSQ_GetElementByIndex(self.cmap, c_int(key)))
        if it.is_past_rear():
            return default
        v = it.value()
        cmap_lib.LSQ_DeleteElement(self.cmap, c_int(key))
        return v

    def __iter__(self):
        it = _MapIterator(cmap_lib.LSQ_GetFrontElement(self.cmap))
        while not it.is_past_rear():
            yield it.key()
            it.next()


class _MapIterator:
    def __init__(self, iterator):
        self.iterator = iterator

    def __del__(self):
        cmap_lib.LSQ_DestroyIterator(self.iterator)

    def key(self):
        return int(cmap_lib.LSQ_GetIteratorKey(self.iterator))

    def value(self):
        return cast(cmap_lib.LSQ_DereferenceIterator(self.iterator),
                    POINTER(c_int)).contents.value

    def pointer(self):
        return cast(cmap_lib.LSQ_DereferenceIterator(self.iterator),
                    POINTER(c_int))

    def pair(self):
        return (cmap_lib.LSQ_GetIteratorKey(self.iterator),
                cast(cmap_lib.LSQ_DereferenceIterator(self.iterator),
                     POINTER(c_int)).contents.value)

    def next(self):
        cmap_lib.LSQ_AdvanceOneElement(self.iterator)

    def is_past_rear(self):
        return cmap_lib.LSQ_IsIteratorPastRear(self.iterator)


class CMapTests(unittest.TestCase):
    def test_construction(self):
        m = Map()
        self.assertTrue(m.cmap)

    def test_set_and_get(self):
        m = Map()
        m[1] = 12
        m[5] = 17
        m[2] = 13
        m[4] = 16
        self.assertEqual(m[1], 12)
        self.assertEqual(m[2], 13)
        self.assertEqual(m[4], 16)
        self.assertEqual(m[5], 17)

    def test_change(self):
        m = Map()
        m[1] = 12
        m[5] = 17
        m[2] = 13
        m[4] = 16
        m[1] = 1
        m[2] = 2
        m[4] = 4
        m[5] = 5
        self.assertEqual(m[1], 1)
        self.assertEqual(m[2], 2)
        self.assertEqual(m[4], 4)
        self.assertEqual(m[5], 5)

    def test_len(self):
        m = Map()
        m[1] = 12
        m[5] = 17
        m[2] = 13
        m[4] = 16
        self.assertEqual(len(m), 4)

    def test_delitem(self):
        m = Map()
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
        m = Map()
        m[1] = 12
        m[5] = 17
        m[2] = 13
        m[4] = 16
        self.assertTrue(2 in m)
        self.assertFalse(3 in m)

    def test_clear(self):
        m = Map()
        m[1] = 12
        m[5] = 17
        m[2] = 13
        m[4] = 16
        m.clear()
        self.assertEqual(len(m), 0)

    def test_copy(self):
        m = Map()
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
        m = Map()
        m[1] = 12
        m[5] = 17
        m[2] = 13
        m[4] = 16
        self.assertEqual(m.get(1), 12)
        self.assertEqual(m.get(3), None)

    def test_items(self):
        m = Map()
        m[1] = 12
        m[5] = 17
        m[2] = 13
        m[4] = 16
        self.assertEqual(list(m.items()), [(1, 12), (2, 13), (4, 16), (5, 17)])

    def test_keys(self):
        m = Map()
        m[1] = 12
        m[5] = 17
        m[2] = 13
        m[4] = 16
        self.assertEqual(list(m.keys()), [1, 2, 4, 5])

    def test_values(self):
        m = Map()
        m[1] = 12
        m[5] = 17
        m[2] = 13
        m[4] = 16
        self.assertEqual(list(m.values()), [12, 13, 16, 17])

    def test_pop(self):
        m = Map()
        m[1] = 12
        m[5] = 17
        m[2] = 13
        m[4] = 16
        self.assertEqual(m.pop(2), 13)
        self.assertEqual(len(m), 3)
        self.assertEqual(m.pop(3), None)
        self.assertEqual(len(m), 3)

    def test_iter(self):
        m = Map()
        m[1] = 12
        m[5] = 17
        m[2] = 13
        m[4] = 16
        a = []
        for i in m:
            a.append(i)
        self.assertEqual(a, [1, 2, 4, 5])

    def test_key_error(self):
        m = Map()
        self.assertRaises(KeyError, lambda: m[10])


class IteratorTests(unittest.TestCase):
    def test_iterator(self):
        m = Map()
        m[1] = 12
        it = _MapIterator(cmap_lib.LSQ_GetFrontElement(m.cmap))
        self.assertEqual(it.key(), 1)
        self.assertEqual(it.value(), 12)
        self.assertTrue(it.pointer())
        self.assertEqual(it.pair(), (1, 12))
        it.next()
        self.assertTrue(it.is_past_rear())


if __name__ == '__main__':
    unittest.main()
