"""
필요한 모듈들과 데이터들을 불러오는 모듈입니다.
기본으로 쓰이는 변수들과 Pos, Datas 등의 클래스들도 여기에 선언되어 있습니다.
"""

from functools import reduce
import random
import re
import decimal
from sys import maxsize as MAX
from copy import deepcopy
from collections import deque, defaultdict
from typing import *
from types import MappingProxyType
from heapq import heappop, heappush
import pickle
import gzip
import traceback
import os
import sys
import inspect
import json
import math
import operator

from .lo_enum import BET, Element

decimal.getcontext().rounding = decimal.ROUND_FLOOR
d = decimal.Decimal
NUMBER = (int, d)
NUM_T = int | d

sys.setrecursionlimit(150)


def simpl(x):
    """:meta private:"""
    if isinstance(x, int):
        x = d(x)
    return x.quantize(d(1)) if x == x.to_integral() else x.normalize()


def solve_linear(coefficient, constant, debug=False):
    if len(coefficient) > 0 and not(len(constant) == len(coefficient) == len(coefficient[0])):
        raise ValueError(f"행렬의 사이즈가 너무 작거나 다릅니다. "
                         f"(계수 행렬 {len(coefficient)}x{len(coefficient[0])}, 상수 {len(constant)}개)")
    coefficient = [_[:] for _ in coefficient]
    constant = constant[:]
    size = len(constant)
    if debug:
        print(f"{size=}\n{coefficient=}\n{constant=}")
    decimalfactor = 10 ** -min(simpl(v).as_tuple().exponent for arr in [*coefficient, constant] for v in arr)
    if debug:
        print(f"{decimalfactor=}")
    for i in range(size):
        for j in range(size):
            coefficient[i][j] *= decimalfactor
        constant[i] *= decimalfactor
    for i in range(size):
        if debug:
            print(f"row_{i} targeted")
        if coefficient[i][i] == 0:
            if debug:
                print(f"row_{i}: element_{i} is 0, adding with other row")
            tempj = -1
            for j in range(i, size):
                if coefficient[j][i] != 0:
                    tempj = j
                    break
            if tempj == -1:
                coefficient[i][i] = 1
                constant[i] *= d("Infinity")
                if debug:
                    print(f"row_{i}: all row's element_{i} is 0  => {coefficient[i]}, {constant[i]}")
                break
            for k in range(size):
                coefficient[i][k] += coefficient[tempj][k]
            constant[i] += constant[tempj]
            if debug:
                print(f"row_{i}: add with row_{tempj} => {coefficient[i]}, {constant[i]}")
        lcm = math.lcm(*(ci for l in coefficient if (ci := int(l[i])) != 0))
        if debug:
            print(f"row_{i}: {lcm=}")
            print(f"row_{i}: multiplying other rows")
        for j in range(size):
            if coefficient[j][i] == 0:
                if debug:
                    print(f"row_{i}: pass row_{j}")
                continue
            factor = lcm // coefficient[j][i]
            for k in range(size):
                coefficient[j][k] *= factor
            constant[j] *= factor
            if debug:
                print(f"row_{i}: multiply row_{j} by {factor} => {coefficient[j]}, {constant[j]}")
        if debug:
            print(f"row_{i}: substiuting with other rows")
        for j in range(size):
            if i == j or coefficient[j][i] == 0:
                if debug:
                    print(f"row_{i}: pass row_{j}")
                continue
            for k in range(size):
                coefficient[j][k] -= coefficient[i][k]
            constant[j] -= constant[i]
            if debug:
                print(f"row_{i}: substitute to row_{j} => {coefficient[j]}, {constant[j]}")
    for i in range(size):
        constant[i] /= coefficient[i][i]
        if debug:
            print(f"row_{i}: divide constant to coefficient => {constant[i]}")
    return constant


try:
    PATH = getattr(sys, '_MEIPASS', os.path.abspath('.'))
    with gzip.open(os.path.join(PATH, 'data', 'unitdata'), 'rb') as f:
        UNITDATA = pickle.load(f)
    del f
except FileNotFoundError:
    try:
        PATH = os.path.abspath(os.path.join(__file__, '..', '..'))
        with gzip.open(os.path.join(PATH, 'data', 'unitdata'), 'rb') as f:
            UNITDATA = pickle.load(f)
        del f
    except FileNotFoundError:
        print("[err] File not found!")
        UNITDATA = dict()


class Pos:
    """2차원 좌표를 다루는 클래스입니다.

    Attributes:
        _x (:obj:`int`): x좌표입니다.
        _y (:obj:`int`): y좌표입니다.
        grid ((:obj:`int`, :obj:`int`)): 전체 필드 크기입니다.

    Args:
        x (:obj:`int`, (:obj:`int`, :obj:`int`), ``Pos``): x좌표 또는 ``(int, int)`` 형태의 튜플, 또는 ``Pos`` 객체입니다.
            x좌표와 y좌표 각각을 인수로 받을 수도 있고, 튜플이나 ``Pos`` 객체를 받을 수도 있습니다.
        y (:obj:`int`): 만약 x에 x좌표를 입력했다면 y좌표, 아니면 ``None`` 입니다.
        grid ((:obj:`int`, :obj:`int`)): 전체 필드 크기이고, 기본값은 (3, 3)입니다.

    Raises:
        ValueError: `x` 또는 `y` 의 값이 주어진 필드 크기 `grid` 에 벗어나면 발생합니다.

    Examples:
        >>> a = Pos(1, 2)
        >>> a
        (1, 2)
        >>> a + (1, -1)
        (2, 1)
        >>> a == Pos(1, 2) and a == 1 * 3 + 2 and a == (1, 2)
        True

    Notes:
        각 좌표값은 0 이상, `grid` 의 좌표값 미만이어야 합니다.
        즉, ``0 <= x < grid[0] and 0 <= y < grid[1]`` 의 값은 항상 :obj:`True` 입니다.
        후술할 덧셈 결과에 대해 이 값이 :obj:`False` 가 되면, ``__add__`` 는 :obj:`None` 을 반환합니다.

        >>> b = Pos(1, 1)
        >>> print(b + (0, 2))
        None

    Notes:
        대소관계 중 같음(``=``)만 지원됩니다. 다른 비교에 대해서는 정상 작동을 보장하지 않습니다.
        오로지 :obj:`int`, (:obj:`int`, :obj:`int`), ``Pos`` 객체와만 비교할 수 있으며,
        다른 데이터 형태와의 비교는 무조건 :obj:`False` 값을 반환합니다.

        >>> a == 5.0 or a == (1, 2, 3) or a == '5' or a == '(1, 2)'
        False
    """
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
                    raise ValueError(f"숫자가 아님 : {x}")
            else:
                if x < 0 or x >= grid[0] * grid[1]:
                    raise ValueError(f"범위를 벗어난 값 : {x} {grid}")
                self._x = x // grid[0]
                self._y = x % grid[0]
        else:
            if x < 0 or x >= grid[0] or y < 0 or y >= grid[1]:
                raise ValueError(f"범위를 벗어난 값 : {x}, {y} {grid}")
            self._x = x
            self._y = y

    def x(self):
        """x좌표 값을 반환합니다."""
        return self._x

    def y(self):
        """y좌표 값을 반환합니다."""
        return self._y

    def xy(self):
        """x, y좌표 값을 튜플로 반환합니다."""
        return self._x, self._y

    def n(self):
        """x, y좌표 값을 하나의 수로 convert 후 반환합니다."""
        return self._x * self.grid[0] + self._y

    def __eq__(self, other):
        """좌표끼리 비교합니다.

        Notes:
            오로지 :obj:`int`, (:obj:`int`, :obj:`int`), ``Pos`` 객체와만 비교할 수 있으며,
            다른 데이터 형태와의 비교는 무조건 :obj:`NotImplemented` 값을 반환합니다.
        """
        if isinstance(other, Pos):
            return self.x() == other.x() and self.y() == other.y()
        elif isinstance(other, int):
            return self.n() == other
        elif isinstance(other, tuple) and len(other) == 2:
            return self.xy() == other
        else:
            return NotImplemented

    def __add__(self, other):
        """좌표끼리 더합니다.

        Notes:
            한 좌표값이 `grid` 를 벗어나면 :obj:`None` 을 반환합니다.

        Raises:
            TypeError: `other` 의 타입이 위 타입들 중 없으면 발생합니다.
        """
        if isinstance(other, Pos):
            return self.__add__(other.xy())
        elif isinstance(other, tuple) and len(other) == 2:
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
    
    def __hash__(self):
        return hash((self._x, self._y))


if TYPE_CHECKING:
    from .lo_char import Character


class Datas:
    """버프의 여러 정보를 담을 때 사용되는 :obj:`NamedTuple` 모음 클래스입니다.

    줄여서 ``D`` 로도 접근할 수 있습니다.
    """

    class TargetProtect(NamedTuple):
        """지정 보호 버프의 정보를 저장합니다."""
        # 지정 보호 정보; 지정 보호 시전자
        # 다음 버프에 사용됨 : TARGET_PROTECT
        target: 'Character'
        """지정 보호 시전자"""

    class Provoked(NamedTuple):
        """도발 버프의 정보를 저장합니다."""
        # 도발 정보; 도발 시전자
        # 다음 버프에 사용됨 : PROVOKED
        target: 'Character'
        """도발 시전자"""

    class FollowAttack(NamedTuple):
        """지원 공격 버프의 정보를 저장합니다."""
        # 지원 공격 정보; 지원 공격 시전자
        # 다음 버프에 사용됨 : FOLLOW_ATTACK
        attacker: 'Character'
        """지원 공격 시전자"""
        chance: NUM_T = 100
        """지원 공격 확률"""

    class CoopAttack(NamedTuple):
        """협동 공격 버프의 정보를 저장합니다."""
        # 협동 공격 정보; 협동 공격 시전자, 스킬 번호
        # 다음 버프에 사용됨 : COOP_ATTACK
        attacker: 'Character'
        """협동 공격 시전자"""
        skill_no: int
        """협동 공격할 스킬 번호"""

    class BuffCond(NamedTuple):
        """버프 조건의 정보를 저장합니다.
        강화 해제(버프 제거) 버프, 버프 면역 버프, 버프 검색 등에 사용됩니다."""
        # 버프 조건 정보;
        # 타입("버프" 또는 {"버프1", "버프2", ...}), 이로운/해로운/기타 효과(BET), 태그, 판별 함수(lambda b: ...),
        # ID, 수치 부호(-1, 0, 또는 1), (제거 시) 개수 제한, (제거 시) 강제 제거 여부, 확률
        # 다음 버프에 사용됨 : IMMUNE_BUFF, REMOVE_BUFF

        type_: Union[str, Iterable] = None
        """버프 문자열 또는 그 문자열의 리스트; ``BuffType`` 을 참고하세요."""
        efft: BET = BET.BUFF | BET.DEBUFF | BET.NORMAL
        """`0~7` 중 하나; ``BuffEffectType`` 을 참고하세요."""
        tag: str = None
        """찾고자 하는 태그 또는 그 태그의 접두어"""
        func: Callable = None
        """``Buff`` 를 인자로 갖는 함수이며, 버프가 조건에 부합하면 :obj:`True`, 아니면 :obj:`False` 를 반환해야 합니다."""
        id_: int | Iterable[int] = None
        """찾고자 하는 버프의 ID 또는 ID들의 집합"""
        val_sign: int = None
        """`-1`, `0`, `1` 중 하나; 버프 수치의 부호"""
        limit: int = MAX
        """(버프 제거에 사용) 제거할 버프 개수, 기본값은 64비트 signed 정수의 최댓값입니다."""
        force: bool = False
        """(버프 제거에 사용) 강제 제거 여부"""
        chance: NUM_T = 100
        """(버프 검색에 사용) 모든 조건을 충족한 경우, ``chance`` %의 확률로 :obj:`True` 를 반환합니다."""

        def __contains__(self, item):
            if self.__class__ is item.__class__:
                return (self.type_ is None or (item.type_ is not None and self.type_ <= item.type_)) and \
                       (self.efft in item.efft) and \
                       (self.tag is None or (item.tag is not None and item.tag.startswith(self.tag))) and \
                       (self.id_ is None or self.id_ == item.id_) and \
                       (self.val_sign is None and self.val_sign == item.val_sign) and \
                       (item.limit <= self.limit)
            return tuple(self).__contains__(item)

    class _DmgInfo(NamedTuple):
        """추가/고정 피해 비율 및 HP% 비례 정보를 저장합니다.
        지속 피해 / 속성 추가 피해 / 공격력% 고정 피해 버프 / HP% 비례 주는/받는 피해 버프에 사용됩니다.
        추가로 ``Trigger.GET_HIT`` (`피격 시`) 트리거를 발동할 때에도 사용되는데, 이는 인화물 버프 발동을 위함입니다."""
        # 공격력% & HP비례 & 속성 데미지 정보; 공격력을 계산할 캐릭터, HP비례의 타깃과 비례 타입, 데미지 속성(E)
        # (0=없음, 1=자신/높을수록, 2=대상/높을수록, 3=자신/낮을수록, 4=대상/낮을수록)
        # 다음 버프에 사용됨 : TAKEDMGINC, TAKEDMGDEC, GIVEDMGINC, GIVEDMGDEC, INSTANT_DMG, DOT_DMG
        # 공격력% 고정피해 (INSTANT_DMG) / 속성 추가 피해, (나/대상의 HP%가 낮을/높을수록 피해량 증가/감소) (나머지)
        # GET_HIT를 트리거할 때에도 사용됨; 인화물 기믹 작동 목적
        subject: 'Character' = None
        """고정 피해를 입힐 때 계산될 공격력을 가지는 캐릭터를 넣으세요."""
        hp_type: int = 0
        """비례 유형입니다. 다음 숫자 중 하나를 입력해야 하며, 이외의 숫자들은 오류를 일으킬 수 있습니다.
            `0` = 비례하지 않음 (기본값)
            `1` = 자신의 HP%가 높을수록
            `2` = 대상의 HP%가 높을수록
            `3` = 자신의 HP%가 낮을수록
            `4` = 대상의 HP%가 낮을수록"""
        element: Element = Element.PHYSICAL
        """`0~3` 중 하나; ``Element`` 를 참고하세요."""

    class DmgInfo(_DmgInfo):
        """추가/고정 피해 비율 및 HP% 비례 정보를 저장합니다.
        지속 피해 / 속성 추가 피해 / 공격력% 고정 피해 버프 / HP% 비례 주는/받는 피해 버프에 사용됩니다.
        추가로 ``Trigger.GET_HIT`` (`피격 시`) 트리거를 발동할 때에도 사용되는데, 이는 인화물 버프 발동을 위함입니다."""
        # 공격력% & HP비례 & 속성 데미지 정보; 공격력을 계산할 캐릭터, HP비례의 타깃과 비례 타입, 데미지 속성(E)
        # (0=없음, 1=자신/높을수록, 2=대상/높을수록, 3=자신/낮을수록, 4=대상/낮을수록)
        # 다음 버프에 사용됨 : TAKEDMGINC, TAKEDMGDEC, GIVEDMGINC, GIVEDMGDEC, INSTANT_DMG, DOT_DMG
        # 공격력% 고정피해 (INSTANT_DMG) / 속성 추가 피해, (나/대상의 HP%가 낮을/높을수록 피해량 증가/감소) (나머지)
        # GET_HIT를 트리거할 때에도 사용됨; 인화물 기믹 작동 목적

        def __new__(cls, *args, **kwargs):
            if len(args) >= 3:
                try:
                    args = args[:2] + (Element(args[2]),) + args[3:]
                except ValueError:
                    pass
            if "element" in kwargs:
                try:
                    kwargs["element"] = Element(kwargs["element"])
                except ValueError:
                    pass
            return super().__new__(cls, *args, **kwargs)

    class BattleLogInfo(NamedTuple):
        """``Game.buff_log`` 에서, 전투/공격 이벤트 기록에 사용됩니다."""
        # Game.buff_log에 전투 이벤트를 구분하기 위해 사용
        bufftype: str
        """"""
        desc: str
        """"""
        random_status: tuple
        """"""

    @classmethod
    def get_all(cls):
        """:meta private:"""
        temp = dict(inspect.getmembers(cls, inspect.isclass))
        del temp['__class__']
        return set(temp.values())


D = Datas  #: :meta private:
Data = TypeVar('Data', *D.get_all())


if __name__ == '__main__':
    print(solve_linear([[1, 3], [4, 1]], [2, 3], True))
