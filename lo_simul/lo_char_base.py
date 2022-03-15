from .lo_enum import *
from .lo_imports import *
from .lo_system import *
from .lo_equips import *


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

    extra_num: str = ''

    def __init__(self, game: 'Game', pos: Union[int, tuple, Pos], rarity=None,
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
            self.type_, self.isags, lbl, flbl, self.equip_condition, self.base_rarity, self.icon_name = self.get_info()
            self.link_bonus = BuffList(*[Buff(*bi, removable=False) for bi in lbl])
            self.full_link_bonuses = [Buff(*bi, removable=False) if bi else None for bi in flbl]
            if self.rarity is None or self.rarity < self.base_rarity:
                self.rarity = self.base_rarity
            self.stats = UNITDATA[self.code][1][self.rarity]
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
        self.buff_iter = (self.baseBuffs, self.statBuffs, self.antiOSBuffs,
                          self.dmgTakeIncBuffs, self.dmgTakeDecBuffs, self.dmgGiveIncBuffs, self.dmgGiveDecBuffs,
                          self.specialBuffs)

        if self.link > 0:
            self.baseBuffs += self.link_bonus * (self.link / d('100'))
        if self.link == 500 and self.flinkbNO is not None:
            self.baseBuffs.append(self.full_link_bonuses[self.flinkbNO])
        for ei in range(len(self.equips)):
            e = self.equips[ei]
            if e is None:
                continue
            elif isinstance(e, Equip):
                e.owner = self
            elif isinstance(e, Sequence):  # (name, rarity, lvl)
                e = self.equips[ei] = EquipPools.ALL_NAME[e[0]](e[1], e[2], self)
            if e.EQUIP_TYPE != self.equip_condition[ei]:
                print(f'[-@-] <!> 경고: 장비 슬롯에 맞지 않는 장비입니다 = {ei+1}번 장비 {e}')
            self.baseBuffs += e.buff

        if self.affection == 200 or self.pledge:
            self.baseBuffs.append(Buff(BT.BUFFLVL, 0, 1, removable=False))

        self.stack_limited_buff_tags = defaultdict(int)

        self.maxhp = self.get_stats()[BT.HP].quantize(d(1))
        if current_hp > 0:
            self.hp = current_hp
        else:
            self.hp = self.maxhp
        self.ap = d(0)

    @classmethod
    def get_info(cls):
        if cls.code not in UNITDATA:
            return cls.type_, cls.isags, cls.link_bonus, cls.full_link_bonuses, \
                   cls.equip_condition, cls.base_rarity, cls.icon_name
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
        icon_name = info[7]
        return type_, isags, link_bonus, full_link_bonuses, equip_condition, base_rarity, icon_name

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
        return simpl(d(self.stats[0]) + d(self.stats[1])*(self.lvl-1) + self.statlvl[0]*d('8'))

    def get_orig_atk(self):
        return simpl(d(self.stats[2]) + d(self.stats[3])*(self.lvl-1) + self.statlvl[1]*d('1.5'))

    def get_orig_def(self):
        return simpl(d(self.stats[4]) + d(self.stats[5])*(self.lvl-1) + self.statlvl[2]*d('1.25'))

    def get_orig_acc(self):
        return simpl(d(self.stats[8]) + self.statlvl[3]*d('1.5'))

    def get_orig_eva(self):
        return simpl(d(self.stats[9]) + self.statlvl[4]*d('0.4'))

    def get_orig_crit(self):
        return simpl(d(self.stats[7]) + self.statlvl[5]*d('0.4'))

    def get_orig_spd(self):
        return d(self.stats[6])

    def get_orig_res(self):
        return tuple(map(d, self.stats[10:]))

    def get_orig_stats(self) -> Dict[str, d]:
        return {i: self.getOrigStatFuncs[i]() for i in BT.STATS}

    def get_base_stats(self) -> Dict[str, d]:
        base_buff_sum = self.baseBuffs.getSUM()
        orig_stats = self.get_orig_stats()
        return {i: base_buff_sum.calc(i, orig_stats[i]) for i in BT.STATS}

    def get_stats(self) -> Dict[str, d]:
        stat_buff_sum = self.statBuffs.getSUM()
        base_stats = self.get_base_stats()
        return {i: stat_buff_sum.calc(i, base_stats[i]) for i in BT.STATS}

    def get_res(self):
        resb = self.find_buff(func=lambda b: b.type in set(BT.ELEMENT_RES)).getSUM()
        return tuple(resb.calc(BT.ELEMENT_RES[i+1], self.get_orig_res()[i]) for i in range(3))

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
        return self.find_buff(BT.SPD).getSUM().calc(BT.SPD, self.get_orig_spd())

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

    def get_skill_atk_rate(self, skill_no):
        return self.find_buff(BT.SKILL_RATE).getSUM().calc(
            BT.SKILL_RATE, 
            d(self.get_skill(skill_no-1)['atkrate'][self.skillvl[(skill_no-1) % 5]])
        )

    def get_skill_buff_value(self, skill_no):
        skill_no -= 1
        lvl = self.find_buff(BT.BUFFLVL).getSUM().calc(BT.BUFFLVL, self.skillvl[skill_no % 5]) - 1
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
            d(self.get_skill(skill_no-1)['range'][self.skillvl[(skill_no-1) % 5]])
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
        if random.random()*100 >= myacc - objeva:
            return d('0')
        if random.random()*100 <= mycrit:
            return d('1.5')
        else:
            return d('1')

    def judge_active(self, chance: NUM_T):
        chance = self.specialBuffs.getSUM().calc(BT.ACTIVE_RATE, chance)
        return random.random()*100 <= chance

    def judge_active_resist(self):
        addp = d('100')
        mulp = d('1')
        for b in self.specialBuffs.find(type_=BT.ACTIVE_RESIST):
            if b.value < 0:
                addp += b.value
            else:
                mulp *= (d('1') - b.value/d('100'))
        addp *= mulp
        return random.random()*100 >= addp
        # True = 저항 성공
        # False = 저항 실패

    def calc_damage(self, obj: 'Character', rate: Tuple[NUM_T, NUM_T], element: int = 0, wr: NUM_T = 0):
        # rate = [스킬 계수, 범위 스킬 계수]
        # 기본 공격력 + 공벞 + 스킬 계수 + 치명타
        damage = self.get_stats()[BT.ATK] * rate[0]
        # 자신 대타입 피증/피감 (합연산)
        if antiosb := self.find_buff(objtype := BT.ANTI_OS[obj.type_[0]]):
            damage = antiosb.getSUM().calc(objtype, damage)
        hprate = [1, self.hp / self.maxhp, obj.hp / obj.maxhp, 1 - self.hp / self.maxhp, 1 - obj.hp / obj.maxhp]
        # 적 받피감 (체력 비례 포함) (합연산)
        dmgdectemp = 0
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
                objdef = dpb.getSUM().calc(BT.DEFPEN, objdef)
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
                print(f"[X@X] <{self}>의 피해 최소화 발동.")
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

    def give_damage(self, dmg, direct=False):
        if not direct:
            if self.find_buff(type_=BT.IMMUNE_DMG):
                print(f"[X@X] <{self}> - 피해 무효 발동.")
                return -2
            for b in self.find_buff(type_=BT.BARRIER, func=lambda b: not b.expired):
                if dmg > b.value:
                    print(f"[X@X] <{self}> - 방어막 {{ {b.value} }} 흡수됨.")
                    dmg -= b.value
                    b.value = 0
                    b.expired = True
                else:
                    print(f"[X@X] <{self}> - 방어막 {{ {dmg} }} 흡수됨.")
                    b.value -= dmg
                    return -1
        dmg = d(dmg).quantize(d(1))
        self.hp -= dmg
        if direct:
            print(f"[XXX] <{self}> - {{ {dmg} }} 피해를 입음.")
        return dmg

    def give_buff(self,
                  _type: str,
                  opr: int,
                  value: NUM_T,
                  _round: int = MAX,
                  count: int = MAX,
                  count_trig: Set[str] = None,
                  efft: int = BET.ETC,
                  max_stack: int = 0,
                  removable: bool = True,
                  tag: Optional[str] = None,
                  data: Optional[Data] = None,
                  desc: Optional[str] = None,
                  force: bool = False):
        """

        :param _type: BT.type_name
        :param opr: "+" = 0, "*" = 1
        :param value: NUM_T
        :param _round: int (=MAX)
        :param count: int (=MAX)
        :param count_trig: Set[str]
        :param efft: BET.BUFF/DEBUFF/ETC (=ETC)
        :param max_stack: int (=0=no limit)
        :param removable: bool
        :param tag: str
        :param data: NamedTuple in Datas
        :param desc: str
        :param force: bool
        """
        buff = Buff(_type, opr, value, _round, count, count_trig, efft, max_stack, removable, tag, data, desc)
        # 최대 중첩
        if 0 < buff.max_stack <= self.stack_limited_buff_tags[buff.tag]:
            self.remove_buff(tag=buff.tag, force=True, limit=1)
        for immune_buff in self.find_buff(type_=BT.IMMUNE_BUFF):
            if buff.issatisfy(**immune_buff.data):
                print(f"[!@!] <{self}> - 버프 무효됨: [{buff}]")
                return
        if (self.type_ != BT.ACTIVE_RESIST or not self.isenemy) and buff.efftype == BET.DEBUFF and not force:
            if self.judge_active_resist():
                print(f"[!@!] <{self}> - 버프 저항함: [{buff}]")
                return
        if buff.type in BT.STATS_SET:
            self.statBuffs.append(buff)
        elif buff.type == BT.AP:
            self.give_ap(buff.value)
        elif buff.type == BT.FORCE_MOVE:
            pass  # 밀기/당기기
        elif buff.type in BT.ANIT_OS_SET:
            self.antiOSBuffs.append(buff)
        elif buff.type == BT.TAKEDMGINC:
            self.dmgTakeIncBuffs.append(buff)
        elif buff.type == BT.TAKEDMGDEC:
            self.dmgTakeDecBuffs.append(buff)
        elif buff.type == BT.GIVEDMGINC:
            self.dmgGiveIncBuffs.append(buff)
        elif buff.type == BT.GIVEDMGDEC:
            self.dmgGiveDecBuffs.append(buff)
        elif buff.type == BT.REMOVE_BUFF:
            self.remove_buff(**buff.data._asdict())
        else:
            self.specialBuffs.append(buff)
        print(f"[!!!] <{self}> - 버프 추가됨: [{buff}]")
        if buff.max_stack > 0:
            self.stack_limited_buff_tags[buff.tag] += 1

    def find_buff(self, type_=None, efft=None, tag=None, func=None, id_=None, val_sign=None):
        result = BuffList()
        for bl in self.buff_iter:
            result += bl.find(type_, efft, tag, func, id_, val_sign)
        return result

    def remove_buff(self, type_=None, efft=None, tag=None, func=None, id_=None, val_sign=None, limit=MAX, force=False,
                    log=True):
        result = BuffList()
        for bl in self.buff_iter:
            result += bl.remove(type_, efft, tag, func, id_, val_sign, limit-len(result), force)
        for b in result:
            if log:
                print(f"[-@-] <{self}> - 버프 제거됨: [{b}]")
            if self.stack_limited_buff_tags[b.tag] > 0:
                self.stack_limited_buff_tags[b.tag] -= 1
        return result

    def buff_update(self, tt=TR.DUMMY, args=None):
        result = BuffList()
        for bl in self.buff_iter:
            result += bl.update(tt, args)
        for b in result:
            if b.type == BT.INSTANT_DMG and self.hp > 0:
                element_rate = 1 if b.data.element == 0 else (1 - self.get_res()[b.data.element] / 100)
                if b.opr:
                    self.give_damage(
                        b.value * b.data.subject.get_stats()[BT.ATK] * element_rate,
                        True
                    )
                else:
                    self.give_damage(b.value * element_rate, True)
                self.dead_judge_process()
            print(f"[-@-] <{self}> - 버프 제거됨: [{b}]")
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
                        c.trigger(TR.ALLY_DEAD, self)
                if c := self.game.get_char(x, field=not self.isenemy):
                    c.trigger(TR.ENEMY_DEAD)
            if self.hp <= 0:  # 전투속행 안 터짐
                self.trigger(TR.INCAPABLE)
                for x in BasicData.passive_order:
                    if c := self.game.get_char(x, field=self.isenemy):
                        c.trigger(TR.ALLY_KILLED, self)
                if attacker is not None:
                    if attacker_follow is None:
                        attacker.trigger(TR.KILL, attacker_skill_no)
                    else:
                        attacker_follow.trigger(TR.KILL, attacker_skill_no)
        elif hit_value > 0 and damage_value > 0:
            self.trigger(TR.GET_HIT, attacker.get_skill_element(attacker_skill_no))
        elif hit_value == 0:
            self.trigger(TR.EVADE)

    def trigger(self, trigtype=TR.DUMMY, args=None, print_msg=False):
        if trigtype != TR.DUMMY and print_msg:
            print(f"[-] <{self}> - <{trigtype}> 트리거 작동함.")
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
        pass

    def _active2(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        pass

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

    def get_passive_funcs(self):
        return [self._passive1, self._passive2, self._passive3]

    def passive(self, trigtype, args=None):
        tempf = self.get_passive_funcs()
        for i in range(3):
            if self.rarity > i:
                buff_values = self.get_skill_buff_value(i + 3)
                aoe = self.get_aoe(self.pos, i + 3)
                tempf[i](trigtype, args, aoe, buff_values)

    def get_passive_targets(self,
                            aoe: List[Union[Tuple[int, int], int, 'Pos']],
                            field: Union[NUM_T, bool] = None
                            ) -> List['Character']:
        temp = self.game.get_chars(aoe, self.isenemy if field is None else field)
        return sorted(temp.values(), key=lambda c: c.getposn())

    def _passive1(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        pass

    def _passive2(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        pass

    def _passive3(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        pass

    def _fpassive1(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        self._passive1(tt, args, targets, bv)

    def _fpassive2(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
        self._passive2(tt, args, targets, bv)

    def _fpassive3(self, tt: str, args: Any, targets: List[Tuple[int, int]], bv: List[NUM_T]):
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
                print(f"[!@!] <{self}> - 전투속행 발동!")

    def base_passive_after(self, tt, args=None):
        if tt == TR.ROUND_START:
            self.give_ap(self.get_spd())
        elif tt == TR.INCAPABLE:
            self.game.remove_char(self, True)
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
        self.trigger(TR.MOVE, pos)

    def idle(self):
        self.give_ap(-1)
        self.trigger(TR.IDLE)

