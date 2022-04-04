from ..lo_char import *

id_ = "DummyAlly"
name = "더미(아군)"
code = "DummyAlly"
group = None
isenemy = False

stats = ('50', '20', '20', '2', '0', '0', '3', '0', '75', '0', '0', '0', '0')
skills = [[
    {
        'apcost': (None, 4),
        'atkrate': (None, '1'),
        'accbonus': (None, 0),
        'range': (None, 2),
        'isattack': 2046,
        'isgrid': 0,
        'isignoreprot': 0,
        'element': (None, 0),
        'aoe': ((0, True, ((0, 0, 1),)),),
        'buff': ('.2',)
    },
    {
        'apcost': (None, 6),
        'atkrate': (None, '1.2'),
        'accbonus': (None, 0),
        'range': (None, 1),
        'isattack': 2046,
        'isgrid': 0,
        'isignoreprot': 0,
        'element': ((0, True, ((0, 0, 1),)),),
        'aoe': (None, 0),
        'buff': ('.2',)
    },
    None, None, None
], [None, None, None, None, None], None]
type_ = (0, 0)
isags = 0
link_bonus = BuffList()
full_link_bonuses = [None]

def _active1(self,
             targets: Dict['Character', NUM_T],
             atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
             bv: Sequence[NUM_T],
             wr: NUM_T,
             element: int):
    for t in targets:
        if targets[t] > 0 and t.find_buff(BT.ROOTED, efft=BET.DEBUFF):
            t.give_buff(BT.TAKEDMGINC, 1, bv[0], round_=0)
    return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

def _active2(self,
             targets: Dict['Character', NUM_T],
             atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
             bv: Sequence[NUM_T],
             wr: NUM_T,
             element: int):
    for t in targets:
        if targets[t] > 0 and t.find_buff(BT.ROOTED, efft=BET.DEBUFF):
            t.give_buff(BT.TAKEDMGINC, 1, bv[0], round_=0)
    return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

def extra_passive(self, tt, args=None):
    if tt == TR.IDLE:
        self.give_buff(BT.RANGE, 0, 2, efft=0, round_=2)