from functools import reduce
import random
import re
import decimal
import numpy as np
from sys import maxsize as MAX
from copy import deepcopy
from collections import deque, defaultdict
from typing import *
from types import MappingProxyType
import heapq as h
import bisect as bs
import pickle
import gzip
import traceback
import os
import sys
import inspect
import json

decimal.getcontext().rounding = decimal.ROUND_FLOOR
d = decimal.Decimal
NUMBER = (int, d)
NUM_T = TypeVar('NUM_T', *NUMBER)


def simpl(x):
    if isinstance(x, int):
        x = d(x)
    return x.quantize(d(1)) if x == x.to_integral() else x.normalize()


PATH = getattr(sys, '_MEIPASS', os.path.abspath('.'))
with gzip.open(os.path.join(PATH, 'data', 'unitdata'), 'rb') as f:
    UNITDATA = pickle.load(f)
del f


class Pos:
    _x: int
    _y: int

    def __init__(self, x, y=None, grid=(3, 3)):
        self.grid: Tuple[int, int] = grid
        if y is None:
            if isinstance(x, Pos):
                self._x = x.x()
                self._y = x.y()
                self.grid = x.grid
            elif isinstance(x, tuple):
                if x[0] < 0 or x[0] >= grid[0] or x[1] < 0 or x[1] >= grid[1]:
                    raise ValueError(f"범위를 벗어난 값 : {x[0]}, {x[1]} {grid}")
                self._x = x[0]
                self._y = x[1]
            elif isinstance(x, str):
                if x.isnumeric():
                    temp = Pos(int(x), grid=grid)
                    self._x = temp.x()
                    self._y = temp.y()
            else:
                if x < 0 or x >= grid[0]*grid[1]:
                    raise ValueError(f"범위를 벗어난 값 : {x} {grid}")
                self._x = x // grid[0]
                self._y = x % grid[0]
        else:
            if x < 0 or x >= grid[0] or y < 0 or y >= grid[1]:
                raise ValueError(f"범위를 벗어난 값 : {x}, {y} {grid}")
            self._x = x
            self._y = y
    
    def x(self):
        return self._x
    
    def y(self):
        return self._y
     
    def xy(self):
        return self._x, self._y
    
    def n(self):
        return self._x * self.grid[0] + self._y
    
    def __eq__(self, other):
        if isinstance(other, Pos):
            return self.x() == other.x() and self.y() == other.y()
        elif isinstance(other, int):
            return self.n() == other
        elif isinstance(other, tuple) and len(other) == 2:
            return self.xy() == other
        else:
            return False
    
    def __add__(self, other):
        if isinstance(other, tuple) and len(other) == 2:
            r = deepcopy(self)
            r._x += other[0]
            r._y += other[1]
            if r.x() < 0 or r.x() >= r.grid[0] or r.y() < 0 or r.y() >= r.grid[1]:
                return None
            return r
        else:
            raise TypeError(f"잘못된 타입 : {type(other).__name__!r}")
    
    def __repr__(self):
        return f"({self._x}, {self._y})"


if TYPE_CHECKING:
    from lo_char_base import Character


class Datas:
    class TargetProtect(NamedTuple):
        # 지정 보호 정보; 지정 보호 시전자
        # 다음 버프에 사용됨 : TARGET_PROTECT
        target: 'Character'

    class Provoked(NamedTuple):
        # 도발 정보; 도발 시전자
        # 다음 버프에 사용됨 : PROVOKED
        target: 'Character'

    class FollowAttack(NamedTuple):
        # 지원 공격 정보; 지원 공격 시전자
        # 다음 버프에 사용됨 : FOLLOW_ATTACK
        attacker: 'Character'

    class CoopAttack(NamedTuple):
        # 협동 공격 정보; 협동 공격 시전자, 스킬 번호
        # 다음 버프에 사용됨 : COOP_ATTACK
        attacker: 'Character'
        skill_no: int

    class BuffCond(NamedTuple):
        # 버프 조건 정보;
        # 타입("버프" 또는 {"버프1", "버프2", ...}), 이로운/해로운/기타 효과(BET), 태그, 판별 함수(lambda b: ...),
        # ID, 수치 부호(-1, 0, 또는 1), (제거 시) 개수 제한, (제거 시) 강제 제거 여부
        # 다음 버프에 사용됨 : IMMUNE_BUFF, REMOVE_BUFF
        type_: Union[str, Iterable] = None
        efft: int = None
        tag: str = None
        func: Callable = None
        id_: int = None
        val_sign: int = None
        limit: int = MAX
        force: bool = False

    class DmgHPInfo(NamedTuple):
        # HP비례 데미지 정보; HP비례의 타깃과 비례 타입, 데미지 속성(E)
        # (0=없음, 1=자신/높을수록, 2=대상/높을수록, 3=자신/낮을수록, 4=대상/낮을수록)
        # 다음 버프에 사용됨 : TAKEDMGINC, TAKEDMGDEC, GIVEDMGINC, GIVEDMGDEC
        # (나/대상의 HP%가 낮을/높을수록 피해량 증가/감소)
        type_: int = 0
        element: int = 0

    class FDmgInfo(NamedTuple):
        # 공격력% & 속성 데미지 정보; 공격력을 계산할 캐릭터, 데미지 속성(E)
        # 다음 버프에 사용됨 : TAKEDMGINC, TAKEDMGDEC, GIVEDMGINC, GIVEDMGDEC, INSTANT_DMG
        # 공격력% 고정피해 / 속성 추가 피해
        # GET_HIT를 트리거할 때 사용됨; 인화물 기믹 작동 목적
        subject: 'Character' = None
        element: int = 0


D = Datas

temp = dict(inspect.getmembers(D(), inspect.isclass))
del temp['__class__']
D.ALL = set(temp.values())
Data = TypeVar('Data', *D.ALL)
del temp
