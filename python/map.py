from ctypes import *

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
            it.forward()
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
            it.forward()

    def keys(self):
        it = _MapIterator(cmap_lib.LSQ_GetFrontElement(self.cmap))
        while not it.is_past_rear():
            yield it.key()
            it.forward()

    def values(self):
        it = _MapIterator(cmap_lib.LSQ_GetFrontElement(self.cmap))
        while not it.is_past_rear():
            yield it.value()
            it.forward()

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
            it.forward()


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

    def forward(self):
        cmap_lib.LSQ_AdvanceOneElement(self.iterator)

    def is_past_rear(self):
        return cmap_lib.LSQ_IsIteratorPastRear(self.iterator)
