import numpy as np
from typing import Any, Sequence
from numbers import Number
from itertools import product
TABLE = {'x': 0, 'y': 1, 'z': 2, 'w': 3, 'r': 0, 'g': 1, 'b': 2, 'a': 3}

PROPERTY = [''.join(prod) for prod in product('x', repeat=1)]
PROPERTY += [''.join(prod) for prod in product('r', repeat=1)]
PROPERTY += [''.join(prod) for prod in product('xy', repeat=2)]
PROPERTY += [''.join(prod) for prod in product('rg', repeat=2)]
PROPERTY += [''.join(prod) for prod in product('xyz', repeat=3)]
PROPERTY += [''.join(prod) for prod in product('xyz', repeat=3)]
PROPERTY += [''.join(prod) for prod in product('xyzw', repeat=4)]
PROPERTY += [''.join(prod) for prod in product('rgba', repeat=4)]

class Vec2(np.ndarray):
    __slots__ = [x for x in PROPERTY if len(x) <= 2]

    def __new__(cls: type, *args):
        if len(args) == 1:
            args = args[0]
        assert len(args) == 2
        obj = np.asarray(args, dtype=np.float64).view(cls)
        return obj

    def __bool__(self) -> bool:
        return bool(self[0] != 0 or self[1] != 0)

    def __getattribute__(self, __name: str) -> Any:
        length = len(__name)
        if 1 <= length <= 2 and all([x in 'xyrg' for x in __name]):
            value = [self[TABLE[x]] for x in __name]
            if length == 1:
                return value[0]
            if length == 2:
                return Vec2(value)
        return super().__getattribute__(__name)

    def __setattr__(self, __name: str, __value: Any) -> None:
        length = len(__name)
        if 1 <= length <= 2 and all([x in 'xyrg' for x in __name]):
            if isinstance(__value, Number):
                for i in range(length):
                    self[TABLE[__name[i]]] = __value
                return self
            elif isinstance(__value, Sequence):
                assert len(__value) == length
                for i in range(length):
                    self[TABLE[__name[i]]] = __value[i]
                return self
        return super().__setattr__(__name, __value)

class Vec3(np.ndarray):
    __slots__ = [x for x in PROPERTY if len(x) <= 3]

    def __new__(cls: type, *args):
        if len(args) == 1:
            args = args[0]
        assert len(args) == 3
        obj = np.asarray(args, dtype=np.float64).view(cls)
        return obj

    def __bool__(self) -> bool:
        return bool(self[0] != 0 or self[1] != 0 or self[2] != 0)

    def __getattribute__(self, __name: str) -> Any:
        length = len(__name)
        if 1 <= length <= 3 and all([x in 'xyzrgb' for x in __name]):
            value = [self[TABLE[x]] for x in __name]
            if length == 1:
                return value[0]
            if length == 2:
                return Vec2(value)
            if length == 3:
                return Vec3(value)
        return super().__getattribute__(__name)

    def __setattr__(self, __name: str, __value: Any) -> None:
        length = len(__name)
        if 1 <= length <= 3 and all([x in 'xyzrgb' for x in __name]):
            if isinstance(__value, Number):
                for i in range(length):
                    self[TABLE[__name[i]]] = __value
                return self
            elif isinstance(__value, Sequence):
                assert len(__value) == length
                for i in range(length):
                    self[TABLE[__name[i]]] = __value[i]
                return self
        return super().__setattr__(__name, __value)

class Vec4(np.ndarray):
    __slots__ = [x for x in PROPERTY if len(x) <= 4]

    def __new__(cls: type, *args):
        if len(args) == 1:
            args = args[0]
        assert len(args) == 4
        obj = np.asarray(args, dtype=np.float64).view(cls)
        return obj

    def __bool__(self) -> bool:
        return bool(self[0] != 0 or self[1] != 0 or self[2] != 0 or self[3] != 0)

    def __getattribute__(self, __name: str) -> Any:
        length = len(__name)
        if 1 <= length <= 4 and all([x in 'xyzwrgba' for x in __name]):
            value = [self[TABLE[x]] for x in __name]
            if length == 1:
                return value[0]
            if length == 2:
                return Vec2(value)
            if length == 3:
                return Vec3(value)
            if length == 4:
                return Vec4(value)
        return super().__getattribute__(__name)

    def __setattr__(self, __name: str, __value: Any) -> None:
        length = len(__name)
        if 1 <= length <= 4 and all([x in 'xyzwrgba' for x in __name]):
            if isinstance(__value, Number):
                for i in range(length):
                    self[TABLE[__name[i]]] = __value
                return self
            elif isinstance(__value, Sequence):
                assert len(__value) == length
                for i in range(length):
                    self[TABLE[__name[i]]] = __value[i]
                return self
        return super().__setattr__(__name, __value)
