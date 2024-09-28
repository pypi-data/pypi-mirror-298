from __future__ import annotations

from pydantic import validate_call

import zwoasi as _zwoasi
from pydantic import BaseModel
import inspect
import re
import numpy as np
from obstechutils.dataclasses import autoconverted

from abc import ABC, abstractclassmethod
import functools

_ZWOASI_DLL_PATH = "C:/Users/I5 Astro Backup/PycharmProjects/dimm/lib/ASICamera2.dll"
_zwoasi.init(_ZWOASI_DLL_PATH)

# Enumarations

class Enum(ABC):

    @abstractclassmethod
    def module(): ...

    @abstractclassmethod
    def namespace(): ...
 
    @abstractclassmethod
    def namespace(self) -> str: ...

    
    def __int__(self) -> int:
        return self._types[self._name]

    def __repr__(self) -> str:
        return f"{type(self).__name__}('{self}')"
 
    def __str__(self) -> str:
        return self._name.removeprefix(self._prefix)

    def __init__(self, x: int | str):

        if isinstance(x, int):
            self._name = self._nums[x]
            return

        name = f'{self._prefix}_{x}'
        if name not in self._types:
            raise ValueError(f'No such key {x}')
        self._name = name
    
    @classmethod
    @lambda f: property(fget=f)
    @functools.cache
    def _prefix(cls) -> dict[str, int]:
        return f"{self.namespace}_{self.subnamespace}_" 

    @classmethod
    @lambda f: property(fget=f)
    @functools.cache
    def _nums(cls) -> dict[str, int]:
        return { 
            v: k for k, v in vars(_zwoasi).items()
                if k.startswith(f'ASI_{cls.namespace}_')                                                                        }

    @classmethod
    @lambda f: property(fget=f)
    @functools.cache
    def _types(cls) -> dict[int, str]:
        return {v: k for k, v in cls._types.items()}
