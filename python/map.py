from ctypes import *

cmap_lib = CDLL("libc_avl_tree_for_python")


class map:

    def __init__(self):
        self.cmap = cmap_lib.LSQ_CreateSequence()

    def __del__(self):
        cmap_lib.LSQ_DestroySequence(self.cmap)

    def __len__(self):
        return cmap_lib.LSQ_GetSize(self.cmap)

    def __setitem__(self, key, item):
        cmap_lib.LSQ_InsertElement(self.cmap, c_int(key), c_int(item))

    def __getitem__(self, item):
        it = cmap_lib.LSQ_GetElementByIndex(self.cmap, c_int(item))
        if cmap_lib.LSQ_IsIteratorPastRear(it):
            cmap_lib.LSQ_DestroyIterator(it)
            raise KeyError
        p = cmap_lib.LSQ_DereferenceIterator(it)
        cmap_lib.LSQ_DestroyIterator(it)
        return int(cast(p, POINTER(c_int)).contents)

    def __delitem__(self, key):
        cmap_lib.LSQ_DeleteElement(self.cmap, c_int(key))

    def __contains__(self, item):
        it = cmap_lib.LSQ_GetElementByIndex(self.cmap, c_int(item))
        r = cmap_lib.LSQ_IsIteratorPastRear(it)
        cmap_lib.LSQ_DestroyIterator(it)
        return bool(r)

    def clear(self):
        cmap_lib.LSQ_DestroySequence(self.cmap)
        self.cmap = cmap_lib.LSQ_CreateSequence()

    def copy(self):
        pass

    def get(self, key, default=None):
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def items(self):
        pass

    def keys(self):
        pass

    def pop(self, key, default=None):
        it = cmap_lib.LSQ_GetElementByIndex(self.cmap, c_int(key))
        if cmap_lib.LSQ_IsIteratorPastRear(it):
            cmap_lib.LSQ_DestroyIterator(it)
            return default
        v = int(cast(cmap_lib.LSQ_DereferenceIterator(it), POINTER(c_int)).contents)
        cmap_lib.LSQ_DestroyIterator(it)
        cmap_lib.LSQ_DeleteElement(self.cmap, c_int(key))
        return v
