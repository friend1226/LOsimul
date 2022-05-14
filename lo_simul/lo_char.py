from .lo_enum import *
from .lo_imports import *
from .lo_system import *
from .lo_equips import *


class CharacterPools:
    ALL_CODES: Dict[str, Type['Character']] = {}
    ALLY: Dict[str, Type['Character']] = {}
    ENEMY: Dict[str, Type['Character']] = {}
    ALL: Dict[str, Type['Character']] = {}


class Character:
    id_: int
    name: str
    code: str
    group: str
    isenemy: bool
    is21squad: bool = False
    isboss: bool = False
    icon_name: str = ''

    stats: Tuple[str, ...]
    skills: Union[
        Tuple[Tuple[Optional[MappingProxyType]], Tuple[Optional[MappingProxyType]], Optional[MappingProxyType]],
        Tuple[Union[Tuple, MappingProxyType], ...]
    ]
    type_: tuple
    isags: int
    link_bonus: BuffList
    full_link_bonuses: list
    equip_condition: tuple = (0, 0, 1, 2)
    base_rarity: int = R.B
    promotion: int = base_rarity

    extra_num: str = ''

    equips: List[Optional[Equip]]

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__()
        CharacterPools.ALL_CODES[cls.code] = cls
        CharacterPools.ALL[cls.name] = cls
        CharacterPools.ALL[cls.__name__] = cls
        if cls.isenemy:
            CharacterPools.ENEMY[cls.name] = cls
        else:
            CharacterPools.ALLY[cls.name] = cls

    def __init__(self, game: 'Game', pos: Union[int, tuple, Pos, str], rarity=None,
                 lvl=1, stat_lvl=None, skill_lvl=None, equips=None,
                 link=0, full_link_bonus_no=None, affection=0, pledge=False, current_hp=0):
        self.game = game
        self.pos = Pos(pos)
        self.rarity = rarity
        self.lvl = lvl
        self.statlvl = stat_lvl  # 체공방적회치
        if self.statlvl is None:
            self.statlvl = [0, 0, 0, 0, 0, 0]
        self.skillvl = skill_lvl
        if self.skillvl is None:
            self.skillvl = [1, 1, 1, 1, 1]
        while len(self.skillvl) < 5:
            self.skillvl.append(1)
        self.equips = equips
        if self.equips is None:
            self.equips = [None, None, None, None]
        self.link = link
        self.flinkbNO = full_link_bonus_no
        self.affection = affection
        self.pledge = pledge
        if self.code in UNITDATA:
            self.type_, self.isags, lbl, flbl, self.equip_condition, self.base_rarity, self.promotion, self.icon_name\
                = self.get_info()
            self.link_bonus = BuffList(*[Buff(*bi, removable=False) for bi in lbl])
            self.full_link_bonuses = [Buff(*bi, removable=False) if bi else None for bi in flbl]
            if self.rarity is None or self.rarity < self.base_rarity:
                self.rarity = self.base_rarity
            self.stats = UNITDATA[self.code][1]
            self.skills = tuple(map(
                lambda data: tuple(map(
                    lambda eata: MappingProxyType(eata) if eata else None, data
                )) if isinstance(data, list) else MappingProxyType(data) if data else None,
                UNITDATA[self.code][2]
            ))
            if self.skills is None:
                self.skills = tuple(tuple(None for _ in range(5)) for __ in range(2)) + (None, )
        else:
            if self.rarity is None:
                self.rarity = self.base_rarity
        if self.base_rarity > self.promotion:
            raise ValueError(f"승급 가능한 최대 등급이 태생 등급보다 낮습니다. "
                             f"(태생 {list(R)[self.base_rarity].name}급 > 최대 {list(R)[self.promotion].name}승급)")
        if self.rarity >= len(self.stats) or self.stats[self.rarity] is None:
            raise ValueError(f"해당 등급의 스탯이 존재하지 않습니다.")

        self.getOrigStatFuncs = {
            BT.HP: self.get_orig_hp,
            BT.ATK: self.get_orig_atk,
            BT.DEF: self.get_orig_def,
            BT.ACC: self.get_orig_acc,
            BT.EVA: self.get_orig_eva,
            BT.CRIT: self.get_orig_crit,
            BT.SPD: self.get_orig_spd,
        }

        self.baseBuffs = BuffList()
        self.statBuffs = BuffList()
        self.antiOSBuffs = BuffList()
        self.dmgTakeIncBuffs = BuffList()
        self.dmgTakeDecBuffs = BuffList()
        self.dmgGiveIncBuffs = BuffList()
        self.dmgGiveDecBuffs = BuffList()
        self.specialBuffs = BuffList()
        self.proportionBuffs = BuffList()
        self.buff_iter = (self.baseBuffs, self.statBuffs, self.proportionBuffs, self.antiOSBuffs,
                          self.dmgTakeIncBuffs, self.dmgTakeDecBuffs, self.dmgGiveIncBuffs, self.dmgGiveDecBuffs,
                          self.specialBuffs)

        if sum(self.statlvl) > self.lvl * 3:
            print(f'[wre] <!> 경고: 불가능한 스탯 레벨입니다 (스탯 레벨 총합 {sum(self.statlvl)} > {self.lvl * 3})',
                  file=self.stream)

        if self.link > 0:
            self.baseBuffs += self.link_bonus * (self.link / d('100'))
        if self.link >= 500 and self.flinkbNO is not None:
            self.baseBuffs.append(self.full_link_bonuses[self.flinkbNO])
        for ei in range(len(self.equips)):
            e = self.equips[ei]
            if isinstance(e, Sequence):  # (name, rarity, lvl)
                if e[0] in EquipPools.ALL_NAME:
                    e = self.equips[ei] = EquipPools.ALL_NAME[e[0]](e[1], e[2], self)
                else:
                    e = None
            if isinstance(e, Equip):
                e.owner = self
            else:
                continue
            if e.EQUIP_TYPE != self.equip_condition[ei]:
                print(f'[wre] <!> 경고: 장비 슬롯에 맞지 않는 장비입니다 = {ei+1}번 장비 {e}', file=self.stream)
            self.baseBuffs += e.buff

        if self.affection == 200 or self.pledge:
            self.baseBuffs.append(Buff(BT.BUFFLVL, 0, 1, removable=False))

        self.stack_limited_buff_tags = defaultdict(int)

        self.maxhp = self.get_stats()[BT.HP].quantize(d(1))
        self.current_hp_arg_val = current_hp
        if current_hp > 0:
            self.hp = current_hp
        else:
            self.hp = self.maxhp
        self.ap = d(0)

    def random(self, r=100, offset=0):
        return self.game.random.uniform(offset, offset+r)

    @property
    def stream(self):
        return self.game.stream

    @classmethod
    def get_info(cls):
        if cls.code not in UNITDATA:
            return cls.type_, cls.isags, cls.link_bonus, cls.full_link_bonuses, \
                   cls.equip_condition, cls.base_rarity, cls.promotion, cls.icon_name
        info = UNITDATA[cls.code][0]
        type_ = info[:2]
        isags = info[2]
        link_bonus = []
        full_link_bonuses = [None]
        for b in info[3]:
            link_bonus.append((b[0], b[1], d(b[2])))
        for b in info[4]:
            full_link_bonuses.append((b[0], b[1], d(b[2])))
        equip_condition = info[5]
        base_rarity = info[6]
        promotable = info[7]
        icon_name = info[8]
        return type_, isags, link_bonus, full_link_bonuses, equip_condition, base_rarity, promotable, icon_name

    @classmethod
    def get_icon_filename(cls):
        from data.icons import icon_list
        temp = icon_list.get(cls.code)
        return temp if temp else f"TbarIcon_{cls.code}_N"

    def __repr__(self):
        return f"<{self.name}_{self.extra_num}({self.getposx()}, {self.getposy()}, {'E' if self.isenemy else 'A'})>"

    def __str__(self):
        return f"{self.name}_{self.extra_num}"

    def get_type_str(self):
        return f"{CharType.desc[self.type_[0]]} {CharRole.desc[self.type_[1]]}"

    def getpos(self):
        return self.pos

    def getposx(self):
        return self.pos.x()

    def getposy(self):
        return self.pos.y()

    def getposxy(self):
        return self.pos.xy()

    def getposn(self):
        return self.pos.n()

    def get_absolute_y(self):
        if self.isenemy:
            return self.getposy() + 3
        else:
            return self.getposy()

    def measure(self, c):
        return abs(self.get_absolute_y() - c.get_absolute_y())

    def attackable(self, c, skill_no):
        return self.measure(c) <= self.get_skill_range(skill_no)

    def collocated(self):
        return self.game.get_char(self.getposn(), field=self.isenemy) is self

    def isformchanged(self):
        return False

    def skill_no_convert(self, skill_no):
        return skill_no

    def get_skill(self, no, apply_formchange: bool = True):
        if apply_formchange:
            no = self.skill_no_convert(no)
        return self.skills[no // 5][no % 5]

    def get_orig_hp(self):
        return simpl(d(self.stats[self.rarity][0]) + d(self.stats[self.rarity][1])*(self.lvl-1) +
                     self.statlvl[0]*d('8'))

    def get_orig_atk(self):
        return simpl(d(self.stats[self.rarity][2]) + d(self.stats[self.rarity][3])*(self.lvl-1) +
                     self.statlvl[1]*d('1.5'))

    def get_orig_def(self):
        return simpl(d(self.stats[self.rarity][4]) + d(self.stats[self.rarity][5])*(self.lvl-1) +
                     self.statlvl[2]*d('1.25'))

    def get_orig_acc(self):
        return simpl(d(self.stats[self.rarity][8]) + self.statlvl[3]*d('1.5'))

    def get_orig_eva(self):
        return simpl(d(self.stats[self.rarity][9]) + self.statlvl[4]*d('0.4'))

    def get_orig_crit(self):
        return simpl(d(self.stats[self.rarity][7]) + self.statlvl[5]*d('0.4'))

    def get_orig_spd(self):
        return d(self.stats[self.rarity][6])

    def get_orig_res(self):
        return tuple(map(d, self.stats[self.rarity][10:]))

    def get_orig_stats(self) -> Dict[str, d]:
        return {i: self.getOrigStatFuncs[i]() for i in BT.STATS}

    def get_base_stats(self) -> Dict[str, d]:
        base_buff_sum = self.baseBuffs.getSUM()
        orig_stats = self.get_orig_stats()
        return {i: base_buff_sum.calc(i, orig_stats[i], True) for i in BT.STATS}

    def get_stats(self) -> Dict[str, d]:
        tempbuffs = self.calculated_cycled_buff()
        stats = self.get_base_stats()
        stat_buff_sum = self.statBuffs.getSUM()
        if tempbuffs:
            extra_add = self.proportionBuffs.find(opr=0, func=lambda b: b.proportion is None).getSUM()
            extra_mul = self.proportionBuffs.find(opr=1, func=lambda b: b.proportion is None)
            for s in BT.STATS:
                stats[s] = stat_buff_sum.calc(s, extra_add.calc(s, stats[s]), True)
            for pbf in extra_mul:
                if pbf.type in BT.STATS_SET:
                    stats[pbf.type] = pbf.calc(stats[pbf.type])
            for char in {b.owner for b in tempbuffs}:
                char.remove_buff(tag="Prop_", force=True)
            return stats
        else:
            return {i: stat_buff_sum.calc(i, stats[i], True) for i in BT.STATS}

    def calculated_cycled_buff(self) -> List[Buff]:
        history = dict()
        dfs_visited = set()

        def dfs(buffpair):
            if buffpair in dfs_visited:
                return
            dfs_visited.add(buffpair)
            if buffpair not in history:
                history[buffpair] = set()
            for bf in buffpair[0].proportionBuffs.find(func=lambda b: b.proportion):
                bfpair = bf.proportion
                if bfpair not in history[buffpair]:
                    history[buffpair].add(bfpair)
                    dfs(bfpair)

        for bf in self.proportionBuffs.find(func=lambda b: b.proportion):
            bfpair = (self, bf.type)
            if bfpair not in history:
                history[bfpair] = set()
            bfdatapair = bf.proportion
            history[bfpair].add(bfdatapair)
            dfs(bfdatapair)

        recursive_chain = []
        chain_index = dict()
        search_queue = deque([(tuple(), (pair, nextpair)) for pair in history.keys() for nextpair in history[pair]])
        while search_queue:
            chain, next_dest = search_queue.popleft()
            if next_dest in chain_index:
                continue
            if next_dest in chain:
                chain = chain[chain.index(next_dest):]
                recursive_chain.append(chain)
                for pair in recursive_chain[-1]:
                    if pair not in chain_index:
                        chain_index[pair] = set()
                    chain_index[pair].add(chain)
            else:
                chain += (next_dest,)
                for nextnext_dest in history[next_dest[1]]:
                    search_queue.append((chain, (next_dest[1], nextnext_dest)))

        if not recursive_chain:
            return []

        def get_value(__char, __bt):
            __bv = None
            if __bt in BT.STATS_SET:
                __bv = __char.get_base_stats()[__bt]
            elif __bt in BT.ELEMENT_RES:
                __bv = __char.get_orig_res()[BT.ELEMENT_RES.index(__bt)]
            elif __bt == BT.SPD:
                __bv = __char.get_orig_spd()
            elif __bt == BT.AP:
                __bv = __char.ap
            return __bv

        tempbuffs = []
        index: Dict[Tuple['Character', str], int] = {v: i for i, v in enumerate(set(
            pair
            for chain in recursive_chain
            for pairpair in chain
            for pair in pairpair
            if pair[1] in BT_CYCLABLE
        ))}
        pairn = len(index)
        mulv = [1 for _ in range(pairn)]
        basev = [0 for _ in range(pairn)]
        propv = [[0 for _ in range(pairn)] for __ in range(pairn)]
        for (char, bt), idx in index.items():
            if bt == BT.DEFPEN:
                basev[idx] = 1 - char.find_buff(type_=bt, func=lambda b: b.proportion is None).getSUM().calc(bt, 1)
            else:
                mulv[idx] = char.find_buff(type_=bt, opr=1, func=lambda b: b.proportion is None) \
                    .getSUM().calc(bt, 1) - 1
                bv = 0
                if bt in BT.STATS_SET:
                    bv = char.get_base_stats()[bt]
                elif bt in BT.ELEMENT_RES:
                    bv = char.get_orig_res()[BT.ELEMENT_RES.index(bt)]
                elif bt == BT.SPD:
                    bv = char.get_orig_spd()
                elif bt == BT.AP:
                    bv = char.ap
                basev[idx] = char.find_buff(type_=bt, opr=0, func=lambda b: b.proportion is None).getSUM().calc(bt, bv)
            for pbf in char.proportionBuffs.find(type_=bt, func=lambda b: b.proportion):
                if pbf.proportion in index:
                    if (char, pbf.type) == pbf.proportion:
                        mulv[idx] *= 1 + pbf.value
                        if not char.find_buff(tag=f"Prop_{pbf.getID()}_"):
                            tempbuff = Buff(pbf.type, 1, pbf.value, tag=f"Prop_{pbf.getID()}_",
                                            owner=char, do_print=False)
                            char.proportionBuffs.append(tempbuff)
                            tempbuffs.append(tempbuff)
                    else:
                        propv[idx][index[pbf.proportion]] += pbf.value
                        
        for i in range(pairn):
            for j in range(pairn):
                if i == j:
                    propv[i][j] = -1
                else:
                    propv[i][j] *= mulv[i]
            basev[i] *= -mulv[i]
        
        resultv = solve_linear(propv, basev)
        for (char, bt), idx in index.items():
            if not char.find_buff(tag=f"Prop_{char}_{bt}_"):
                tempbuff = Buff(bt, 0, (resultv[idx] + basev[idx]) / mulv[idx], tag=f"Prop_{char}_{bt}_",
                                owner=char, do_print=False)
                char.proportionBuffs.append(tempbuff)
                tempbuffs.append(tempbuff)

        return tempbuffs

    def get_res(self):
        resb = self.find_buff(func=lambda b: b.type in set(BT.ELEMENT_RES)).getSUM()
        return tuple(resb.calc(BT.ELEMENT_RES[i+1], self.get_orig_res()[i], True) for i in range(3))

    def get_res_dmgrate(self, element: int):
        if element == 0:
            return 1
        res = self.get_res()[element - 1]
        if eml := self.find_buff(type_=BT.ELEMENT_MIN[element]):
            res = max(res, eml[-1].value)
        if self.find_buff(type_=BT.ELEMENT_REV[element]):
            res *= -1
        return 1 - res / d(100)

    def get_spd(self):
        return self.find_buff(BT.SPD).getSUM().calc(BT.SPD, self.get_orig_spd(), True)

    def get_aoe(self, targ_pos, skill_no) -> Union[List[Tuple[int, int]], List[Tuple[int, int, NUM_T]]]:
        r = []
        idx = -1
        skill_no -= 1
        lvl = self.skillvl[skill_no % 5]
        temp = self.get_skill(skill_no)['aoe']
        for x in temp:
            if lvl < x[0]:
                break
            idx += 1
        aoetemp = temp[idx]
        if aoetemp[1]:
            for x in aoetemp[2]:
                pt = Pos(targ_pos) + x[:2]
                if pt is None:
                    continue
                if len(x) == 3:
                    r.append(pt.xy() + (d(str(x[2])),))
                else:
                    r.append(pt.xy())
        else:
            for x in aoetemp[2]:
                if len(x) == 3:
                    r.append(x[:2] + (d(str(x[2])),))
                else:
                    r.append(x)
        return r

    def get_skill_atk_rate(self, skill_no=None, value=None):
        if skill_no is not None:
            value = d(self.get_skill(skill_no-1)['atkrate'][self.skillvl[(skill_no-1) % 5]])
        if value is None:
            return 0
        return self.find_buff(BT.SKILL_RATE).getSUM().calc(BT.SKILL_RATE, value, True)

    def get_skill_buff_value(self, skill_no):
        skill_no -= 1
        lvl = self.find_buff(BT.BUFFLVL).getSUM().calc(BT.BUFFLVL, self.skillvl[skill_no % 5], True) - 1
        r = []
        for x in self.get_skill(skill_no)['buff']:
            if isinstance(x, str):
                r.append(d(x))
            elif isinstance(x, tuple):
                r.append(d(x[0]) + d(x[1]) * lvl)
            else:
                raise TypeError(f"잘못된 타입 : {type(x).__name__!r}")
        return r

    def get_skill_range(self, skill_no):
        return self.find_buff(BT.RANGE).getSUM().calc(
            BT.RANGE, 
            d(self.get_skill(skill_no-1)['range'][self.skillvl[(skill_no-1) % 5]]),
            True
        )

    def get_skill_cost(self, skill_no):
        return self.get_skill(skill_no-1)['apcost'][self.skillvl[(skill_no-1) % 5]]

    def get_skill_element(self, skill_no):
        return self.get_skill(skill_no-1)['element'][self.skillvl[(skill_no-1) % 5]]

    def judge_hit(self, obj: 'Character', acc_bonus: int = 0):
        mystats = self.get_stats()
        myacc = mystats[BT.ACC] + acc_bonus
        mycrit = mystats[BT.CRIT]
        objeva = obj.get_stats()[BT.EVA]
        if self.random() >= myacc - objeva:
            return d('0')
        if self.random() <= mycrit:
            return d('1.5')
        else:
            return d('1')

    def judge_active(self, chance: NUM_T = 100):
        chance = self.specialBuffs.getSUM().calc(BT.ACTIVE_RATE, chance, True)
        return self.random() <= chance
        # True = 발동 성공
        # False = 발동 실패

    def judge_resist_buff(self, buff, chance: NUM_T = 100, print_p=False):
        active_p = 0
        active_chances = []
        if buff.efftype == BET.DEBUFF and (buff.type != BT.ACTIVE_RESIST or not self.isenemy):
            for b in self.specialBuffs.find(type_=BT.ACTIVE_RESIST):
                if b.opr:  # 효과 저항 (독립시행)
                    active_chances.append(b.value)
                else:      # 효과 저항 (기본 확률 증감)
                    active_p -= b.value
        remove_p = 0
        remove_flag = False
        remove_chances = []
        if buff.type == BT.REMOVE_BUFF:
            for b in self.specialBuffs.find(type_=BT.REMOVE_BUFF_RESIST):
                if b.opr:
                    remove_chances.append(b.value)
                else:
                    remove_p -= b.value
                    remove_flag = True

        def m(p):
            if p > 1:
                return 1
            elif p < 0:
                return 0
            else:
                return p
        total_p = 100
        if remove_chances:
            for c in active_chances:
                total_p *= m((chance + active_p + c) / 100)
            for c in remove_chances:
                total_p *= m((chance + active_p + remove_p + c) / 100)
        else:
            if active_chances:
                for c in active_chances:
                    total_p *= m((chance + active_p + c) / 100)
                if remove_flag:
                    total_p *= m((chance + active_p + remove_p) / 100)
            else:
                total_p *= m((chance + active_p + remove_p) / 100)
        if print_p:
            print(f"[tmp] {buff.type} ({buff.efftype}) / "
                  f"버프 발동 확률 = {total_p}%", file=self.stream)
        return self.random() > total_p
        # True = 저항 성공
        # False = 저항 실패

    def calc_damage(self, obj: 'Character', rate: Tuple[NUM_T, NUM_T], element: int = 0, wr: NUM_T = 0):
        # rate = [스킬 계수, 범위 스킬 계수]
        # 기본 공격력 + 공벞 + 스킬 계수 + 치명타
        damage = self.get_stats()[BT.ATK] * self.get_skill_atk_rate(value=rate[0])
        # 자신 대타입 피증/피감 (합연산)
        if antiosb := self.find_buff(objtype := BT.ANTI_OS[obj.type_[0]]):
            damage = antiosb.getSUM().calc(objtype, damage, True)
        hprate = [1, self.hp / self.maxhp, obj.hp / obj.maxhp, 1 - self.hp / self.maxhp, 1 - obj.hp / obj.maxhp]
        # 적 받피감 (체력 비례 포함) (합연산)
        dmgdectemp = 0
        if not self.find_buff(type_=BT.IGNORE_BARRIER_DMGDEC):
            for b in obj.dmgTakeDecBuffs:
                dmgdectemp += damage - b.calc(damage, hprate[0 if b.data is None else b.data.type_] * -1)
        # 자신 주는 피해 증가/감소 (체력 비례 포함) (합연산)
        dmginctemp = 0
        for b in self.dmgGiveDecBuffs:
            dmginctemp += b.calc(damage, hprate[0 if b.data is None else b.data.type_] * -1) - damage
        for b in self.dmgGiveIncBuffs:
            dmginctemp += b.calc(damage, hprate[0 if b.data is None else b.data.type_]) - damage
        damage += dmginctemp - dmgdectemp

        if element == 0:
            # 물리 피해
            objdef = obj.get_stats()[BT.DEF]
            # 적 방어력
            if dpb := self.find_buff(BT.DEFPEN):
                objdef = dpb.getSUM().calc(BT.DEFPEN, objdef, True)
                # 방관 (합연산)
            damage -= objdef
        else:
            damage *= obj.get_res_dmgrate(element)

        for dtib in obj.dmgTakeIncBuffs:
            # 상대 받피증 (곱연산)
            if dtib.data is None or dtib.data.element == 0:
                # 물리 피해 증가
                damage = dtib.calc(damage, hprate[0 if dtib.data is None else dtib.data.type_])
            else:
                # 속성 피해 증가
                damage = dtib.calc(
                    damage, obj.get_res_dmgrate(dtib.data.element))

        damage *= rate[1]
        # 범위 공격 피해량 감소

        # 피해 최소화
        if minib := self.find_buff(type_=BT.MINIMIZE_DMG):
            if minib[-1].value >= damage:
                print(f"[amd] <{self}>의 피해 최소화 발동.", file=self.stream)
                damage = 1

        # 광역 피해 분산/집중
        wrd = 0
        wri = 0
        for b in obj.find_buff(BT.WIDE_TAKEDMG):
            wrd -= b.value * wr
        for b in self.find_buff(BT.WIDE_GIVEDMG):
            wri += b.value * (1 - wr)
        damage *= (1 + wrd) * (1 + wri)
        
        return simpl(damage)

    def give_damage(self, dmg, direct=False, ignore_barrier=False):
        if not direct:
            if self.find_buff(type_=BT.IMMUNE_DMG):
                print(f"[adi] <{self}> - 피해 무효 발동.", file=self.stream)
                self.game.battle_log.append((self, -2))
                return -2
            if not ignore_barrier:
                for b in self.find_buff(type_=BT.BARRIER, func=lambda b: not b.expired):
                    if dmg > b.value:
                        print(f"[bar] <{self}> - 방어막 {{ {b.value} }} 흡수됨.", file=self.stream)
                        self.game.battle_log.append((self, -1, b.value, b))
                        dmg -= b.value
                        b.value = 0
                        b.expired = True
                    else:
                        print(f"[bar] <{self}> - 방어막 {{ {dmg} }} 흡수됨.", file=self.stream)
                        self.game.battle_log.append((self, -1, dmg, b))
                        b.value -= dmg
                        return -1
        dmg = d(dmg).quantize(d(1))
        self.hp -= dmg
        if direct:
            print(f"[dmg] <{self}> - {{ {dmg} }} 피해를 입음.", file=self.stream)
        self.game.battle_log.append((self, dmg))
        return dmg

    def give_buff(self,
                  type_: str,
                  opr: int,
                  value: NUM_T,
                  round_: int = MAX,
                  count: int = MAX,
                  count_trig: Set[str] = None,
                  efft: int = BET.NORMAL,
                  max_stack: int = 0,
                  removable: bool = True,
                  tag: Optional[str] = None,
                  data: Optional[Data] = None,
                  proportion: Optional[tuple] = None,
                  desc: Optional[str] = None,
                  force: bool = False,
                  chance: NUM_T = 100,
                  made_by: Optional['Character'] = None,
                  do_print: bool = True):
        if made_by is None:
            made_by = inspect.currentframe().f_back.f_locals.get('self', None)
        return self.game.give_buff(self, type_, opr, value, round_, count, count_trig, efft, max_stack,
                                   removable, tag, data, proportion, desc, force, chance, made_by, do_print)

    def find_buff(self, type_=None, efft=None, tag=None, func=None, id_=None, val_sign=None, opr=None):
        result = BuffList()
        for bl in self.buff_iter:
            result += bl.find(type_, efft, tag, func, id_, val_sign, opr)
        return result

    def remove_buff(self, type_=None, efft=None, tag=None, func=None, id_=None, val_sign=None, opr=None,
                    limit=MAX, force=False, log=True, **kwargs):
        result = BuffList()
        for bl in self.buff_iter:
            result += bl.remove(type_, efft, tag, func, id_, val_sign, opr, limit-len(result), force)
        for b in result:
            if log and b.do_print:
                print(f"[brm] <{self}> - 버프 제거됨: [{b}]", file=self.stream)
            if self.stack_limited_buff_tags[b.tag] > 0:
                self.stack_limited_buff_tags[b.tag] -= 1
        return result

    def buff_update(self, tt=TR.DUMMY, args=None):
        result = BuffList()
        for bl in self.buff_iter:
            result += bl.update(tt, args)
        for b in result:
            if b.type == BT.INSTANT_DMG and self.hp > 0:
                element_rate = 1 if b.data is None or b.data.element == 0 \
                    else (1 - self.get_res()[b.data.element] / 100)
                if b.opr:
                    self.give_damage(
                        b.value * b.data.subject.get_stats()[BT.ATK] * element_rate,
                        True
                    )
                else:
                    self.give_damage(b.value * element_rate, True)
                self.dead_judge_process()
            if b.do_print:
                print(f"[brm] <{self}> - 버프 제거됨: [{b}]", file=self.stream)
        return result

    def dead_judge_process(self,
                           hit_value: Optional[int] = None,
                           damage_value: Optional[int] = None,
                           attacker: Optional['Character'] = None,
                           attacker_skill_no: Optional[int] = None,
                           attacker_follow: Optional['Character'] = None):
        if self.hp <= 0:
            self.trigger(TR.DEAD)
            for x in BasicData.passive_order:
                if c := self.game.get_char(x, field=self.isenemy):
                    if c is not self:
                        c.trigger(TR.ALLY_DEAD, {"subject": self})
                if c := self.game.get_char(x, field=not self.isenemy):
                    c.trigger(TR.ENEMY_DEAD)
            if self.hp <= 0:  # 전투속행 안 터짐
                self.trigger(TR.INCAPABLE)
                for x in BasicData.passive_order:
                    if c := self.game.get_char(x, field=self.isenemy):
                        c.trigger(TR.ALLY_KILLED, {"target": self})
                if attacker is not None:
                    if attacker_follow is None:
                        attacker.trigger(TR.KILL, {"skill_no": attacker_skill_no})
                    else:
                        attacker_follow.trigger(TR.KILL, {"skill_no": attacker_skill_no})
        elif hit_value is None or damage_value is None:
            return
        elif hit_value > 0 and damage_value > 0:
            self.trigger(TR.GET_HIT,
                         {"subject": attacker, "element": attacker.get_skill_element(attacker_skill_no)})
        elif hit_value == 0:
            self.trigger(TR.EVADE)

    def trigger(self, trigtype=TR.DUMMY, args=None, print_msg=False):
        if trigtype != TR.DUMMY and print_msg:
            print(f"[trg] <{self}> - <{trigtype}> 트리거 작동함.", file=self.stream)
        if (trigtype == TR.ALLY_DEAD or trigtype == TR.ALLY_KILLED) and args == self:
            return
        for eq in self.equips:
            if eq:
                eq.passive(trigtype, args)
        self.buff_update(trigtype, args)
        self.base_passive_before(trigtype, args)
        self.passive(trigtype, args)
        self.base_passive_after(trigtype, args)
        self.extra_passive(trigtype, args)

    def give_ap(self, val: NUM_T):
        if isinstance(val, NUMBER):
            self.ap += val
            if self.ap > 20:
                self.ap = d(20)
            elif self.ap < 0:
                self.ap = d(0)
            self.ap = simpl(self.ap)
        else:
            raise ValueError(f"잘못된 값 : {val}")

    def active(
            self,
            skill_no: int,
            targets: Dict['Character', NUM_T],
            atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
            aoe_len: int):
        buff_values: Sequence[NUM_T] = self.get_skill_buff_value(skill_no)
        wr: NUM_T = 0
        element = self.get_skill_element(skill_no)
        if aoe_len > 1:
            wr = d(len(targets) - 1) / d(aoe_len - 1)
        if skill_no == 1:
            damages = self._active1(targets, atk_rate, buff_values, wr, element)
        elif skill_no == 2:
            damages = self._active2(targets, atk_rate, buff_values, wr, element)
        elif skill_no == 6:
            damages = self._factive1(targets, atk_rate, buff_values, wr, element)
        elif skill_no == 7:
            damages = self._factive2(targets, atk_rate, buff_values, wr, element)
        else:
            damages = dict()
        return damages

    def _active1(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        return {}

    def _active2(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        return {}

    def _factive1(self,
                  targets: Dict['Character', NUM_T],
                  atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                  bv: Sequence[NUM_T],
                  wr: NUM_T,
                  element: int):
        return self._active1(targets, atk_rate, bv, wr, element)

    def _factive2(self,
                  targets: Dict['Character', NUM_T],
                  atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                  bv: Sequence[NUM_T],
                  wr: NUM_T,
                  element: int):
        return self._active2(targets, atk_rate, bv, wr, element)

    def get_passive_active_chance(self, skill_no: int):
        return 100

    def passive(self, trigtype, args=None):
        passives = {
            2: self._passive1,
            3: self._passive2,
            4: self._passive3,
            7: self._fpassive1,
            8: self._fpassive2,
            9: self._fpassive3,
        }
        for i in range(3):
            if self.rarity > i:
                skn = self.skill_no_convert(i + 2)
                if not self.judge_active(self.get_passive_active_chance(skn)):
                    continue
                buff_values = self.get_skill_buff_value(skn+1)
                aoe = self.get_aoe(self.pos, skn+1)
                passives[skn](trigtype, args, aoe, buff_values)

    def get_passive_targets(self,
                            aoe: List[Union[Tuple[int, int], int, 'Pos']],
                            field: Union[NUM_T, bool] = None
                            ) -> List['Character']:
        return sorted(self.game.get_chars(aoe, self.isenemy if field is None else field).values(),
                      key=lambda c: c.getposn())

    def _passive1(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        pass

    def _passive2(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        pass

    def _passive3(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        pass

    def _fpassive1(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        self._passive1(tt, args, targets, bv)

    def _fpassive2(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        self._passive2(tt, args, targets, bv)

    def _fpassive3(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        self._passive3(tt, args, targets, bv)

    def base_passive_before(self, tt, args=None):
        if tt == TR.DEAD:
            if bcbuffs := self.find_buff(BT.BATTLE_CONTINUATION):
                bcb = bcbuffs[-1]
                if bcb.opr:
                    self.hp = bcb.calc(self.maxhp) - self.maxhp
                else:
                    self.hp = bcb.value
                self.remove_buff(id_=bcb.getID(), force=True)
                self.trigger(TR.BATTLE_CONTINUED)
                print(f"[bcn] <{self}> - 전투속행 발동!", file=self.stream)

    def base_passive_after(self, tt, args=None):
        if tt == TR.ROUND_START:
            self.give_ap(self.get_spd())
        elif tt == TR.INCAPABLE:
            self.game.remove_char(self, msg=True)
        elif tt == TR.IDLE:
            if idleb := self.find_buff(tag='Maria_p1_ForceIDLE'):
                self.remove_buff(id_=idleb[-1].getID(), force=True)
        elif tt == TR.WAVE_END:
            self.remove_buff(func=lambda b: b.type != BT.RACON, log=False)
            self.give_ap(-MAX)

    def extra_passive(self, tt, args=None):
        pass

    def move(self, pos):
        self.give_ap(-2)
        if self.game.get_char(pos, field=int(self.isenemy)):
            return False
        self.game.remove_char(self)
        self.pos = Pos(pos)
        self.game.put_char(self)
        self.trigger(TR.MOVE, {"pos": pos})

    def idle(self):
        self.give_ap(-1)
        self.trigger(TR.IDLE)
