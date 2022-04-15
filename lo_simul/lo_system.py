from .lo_enum import *
from .lo_imports import *

import heapq as h
import bisect as bs

if TYPE_CHECKING:
    from .lo_char import Character


class Game:
    def __init__(self):
        self.__field = [
            [[None, None, None], 
             [None, None, None], 
             [None, None, None]],
            [[None, None, None], 
             [None, None, None], 
             [None, None, None]],
        ]
        self.__characters = set()
        self.__character_types = [defaultdict(int), defaultdict(int)]
        self.round = 0
        self.wave = 0
        self.__impacts = deque()
        self.__stream = sys.stdout
        self.__random = random.Random()
        self.battle_log = []
        # battle_log에서, index가 큰 요소가 나중에 추가된 로그이며, 각 요소는 다음 셋 중 하나이다.
        # D.BattleLogInfo: 웨이브/라운드 시작/종료 또는 캐릭터가 행동함
        # Buff 객체: 버프가 추가됨
        # tuple: 피해 정보; 0번은 피해받은 캐릭터, 1번은 데미지(양수=데미지, 0=회피, -1=방어막, -2=피해무효)
        #                   (추가 정보는 해당 코드 참고 바람)

    @property
    def enemy_all_down(self):
        return not any(any(self.__field[1][i]) for i in range(3))

    @property
    def random(self):
        return self.__random

    @property
    def stream(self):
        return self.__stream
    
    @stream.setter
    def stream(self, stream):
        self.__stream = stream
    
    def put_char(self, c, field=None):
        fi, x, y = int(field if field is not None else c.isenemy), c.getposx(), c.getposy()
        if self.__field[fi][x][y] is not None:
            self.remove_char(self.get_char(x, y, field=fi))
        self.__field[fi][x][y] = c
        self.__characters.add(c)
        c.extra_num = chr(ord('A') + self.__character_types[fi][type(c)])
        self.__character_types[fi][type(c)] += 1

    def put_from_file(self, filename, field):
        from .lo_char import CharacterPools
        with open(filename, 'r', encoding='utf-8') as f_:
            temp_ = json.load(f_)
            for i in range(9):
                if (cha := self.get_char(i, field=field)) is not None:
                    self.remove_char(cha, field=field)
            for i, cinf in enumerate(temp_):
                if len(cinf) > 0:
                    self.put_char(CharacterPools.ALL_CODES[cinf['code']](
                        self,
                        i,
                        **cinf["args"]
                    ), field=field)
        del CharacterPools
    
    def get_char(self, x, y=None, field=0) -> Optional['Character']:
        try:
            p = Pos(x, y)
        except ValueError:
            return None
        return self.__field[field][p.x()][p.y()]
    
    def remove_char(self, c, field=None, msg=False):
        ce = int(c.isenemy) if field is None else field
        cp = c.getpos()
        target = self.__field[ce][cp.x()][cp.y()]
        if target == c:
            self.__field[ce][cp.x()][cp.y()] = None
            self.__characters.remove(c)
            self.__character_types[ce][type(c)] -= 1
            if msg:
                print(f"[rmv] <{c}> - 전장에서 제거됨", file=self.stream)
        else:
            raise ValueError(f"{c}라는 캐릭터가 없음")
    
    def trigger(self, trigtype=TR.DUMMY, ally_pos=None, enemy_pos=None):
        if trigtype == TR.DUMMY and self.enemy_all_down:
            self.wave_end()
        if ally_pos is None:
            ally_pos = BasicData.passive_order
        if enemy_pos is None:
            enemy_pos = BasicData.passive_order
        for i in ally_pos:
            if c := self.get_char(i):
                c.trigger(trigtype)
        for i in enemy_pos:
            if c := self.get_char(i, field=1):
                c.trigger(trigtype)

    def get_chars(self, aoe: Iterable[Union[Pos, Tuple[int, int], int]] = None, field=0) \
            -> Dict[Tuple[int, int], 'Character']:
        result = dict()
        if aoe is None:
            aoe = BasicData.prange_all_abs
        for i in aoe:
            try:
                p = Pos(i).xy()
            except ValueError:
                continue
            if temp := self.get_char(p, field=field):
                result[p] = temp
        return result

    def get_targets(self, aoe, ignore_protect=False, field=0) -> \
            Dict[Tuple[int, int], Tuple[Optional[str], 'Character']]:
        chars = self.get_chars(aoe, field)
        result: Dict[Tuple[int, int], Tuple[Optional[str], 'Character']] = {i: (None, chars[i]) for i in chars}
        # (x, y) : (보호 타입(없으면 None), 피격당하는(보호하는) 캐릭터)
        if not ignore_protect:
            # TODO : 해당 공략 참고하여 재작성 하였음; https://arca.live/b/lastorigin/45197071
            tarprot: Dict['Character', Set[Tuple['Character', int]]] = dict()
            # 지정 보호 시전자 : {(보호 대상, 버프id), ...}
            # 시전자는 HP가 많은 순서대로 보호 실행, 이때 대상은 HP가 적은 순서대로, 보호받지 않은 대상 선택
            colprot: List[Set[Tuple['Character', int]]] = [set(), set(), set()]
            # 열 번호 : {(열 보호 시전자, 버프id), ...}
            # HP가 가장 많은 시전자 선택
            rowprot: List[Optional['Character']] = [None, None, None]
            # 행 번호 : 행 보호 시전자
            # 앞에 있는 시전자 선택
            for i in range(9):
                c = self.get_char(i, field=field)
                if c is None:
                    continue
                if tarb := c.find_buff(BT.TARGET_PROTECT):
                    for tb in tarb:
                        if (pc := tb.data.target) == c:
                            continue
                        elif tarprot.get(pc):
                            tarprot[pc].add((c, tb.getID()))
                        else:
                            tarprot[pc] = {(c, tb.getID())}
                if colb := c.find_buff(BT.COLUMN_PROTECT):
                    colprot[c.getposy()].add((c, colb[-1].getID()))
                if c.find_buff(BT.ROW_PROTECT):
                    if (prevc := rowprot[c.getposx()]) is None or (prevc.getposy() < c.getposy() ^ field):
                        # 자신보다 앞에 있는 행 보호 시전자(열 번호가 아군의 경우 크면, 적의 경우 작으면)가 있는 경우
                        rowprot[c.getposx()] = c

            # 행 보호
            for i in range(3):
                if rowprot[i]:
                    # 현재 행에 행 보호 시전자 존재
                    protected = False  # 실제 보호 여부
                    for j in (range(rowprot[i].getposy()) if field == 0 else range(rowprot[i].getposy() + 1, 3)):
                        # 아군의 경우 0부터 (자신 열 번호)-1까지
                        # 적군의 경우 (자신 열 번호)+1부터 2까지
                        if result.get((i, j)) is not None:
                            result[(i, j)] = (BT.ROW_PROTECT, rowprot[i])
                            protected = True
                    if protected and rowprot[i].getposxy() in result:
                        result[rowprot[i].getposxy()] = (BT.ROW_PROTECT, rowprot[i])

            # 열 보호
            for i in range(3):
                if colprot[i]:
                    colpc = max(colprot[i], key=lambda j: (j[0].hp, j[1]))[0]
                    # HP가 가장 많은 시전자 선택
                    protected = False  # 실제 보호 여부
                    for j in range(3):
                        if (foo := result.get((j, i))) is not None and foo[0] is None and foo[1] is not colpc:
                            # (j, i)에 피격자가 존재하고, 아무 보호를 받지 않으며, 자신이 아닐때
                            result[(j, i)] = (BT.COLUMN_PROTECT, colpc)
                            protected = True
                    if protected and colpc.getposxy() in result and result[colpc.getposxy()][0] != BT.ROW_PROTECT:
                        #            ㄴ> 행/열 보호를 받는 행/열 보호기라는 특수 케이스
                        result[colpc.getposxy()] = (BT.COLUMN_PROTECT, colpc)

            # 지정 보호
            for targc in sorted(tarprot.keys(), key=lambda cc: -cc.hp):
                in_attack = targc.getposxy() in result
                if in_attack and result[targc.getposxy()][0] == BT.TARGET_PROTECT:
                    continue
                # HP가 큰 순으로 정렬
                targtpool = list(filter(lambda tt: tt[0].getposxy() in result and result[tt[0].getposxy()][0] is None,
                                        sorted(tarprot[targc], key=lambda t: (t[0].hp, -t[1]))))
                # 아직 보호를 받지 못한 피격자들을 HP가 적은 순으로 정렬
                if not targtpool:
                    continue
                targt = min(targtpool, key=lambda tp: (tp[0].hp, -tp[1]))[0]  # 보호 대상자
                result[targt.getposxy()] = (BT.TARGET_PROTECT, targc)
                if in_attack:
                    result[targc.getposxy()] = (BT.TARGET_PROTECT, targc)
                # TODO : 지정 보호가 제대로 작동하는지 확인
        return result

    def use_skill(self,
                  subjc: 'Character',
                  skill_no: int,
                  objpos: Union[int, Pos]):
        self._use_skill(subjc, skill_no, objpos)
    
    def _use_skill(self,
                   subjc: 'Character',
                   skill_no: int,
                   objpos: Union[int, Pos],
                   catkr: Optional[NUM_T] = None,
                   follow: Optional['Character'] = None,
                   coop: Optional[int] = None,
                   impact: int = 0):
        if self.enemy_all_down:
            return
        if catkr is not None:
            print(f"[acc] ~~~ <{subjc}> 행동 ~~~ (반격)", file=self.stream)
        elif follow is not None:
            print(f"[acf] ~~~ <{subjc}> 행동 ~~~ (지원공격)", file=self.stream)
        elif coop is not None:
            print(f"[aco] ~~~ <{subjc}> 행동 ~~~ (협동공격)", file=self.stream)
        elif impact != 0:
            print(f"[aci] ~~~ <{subjc}> 행동 ~~~ (착탄)", file=self.stream)
        else:
            self.battle_log.append(D.BattleLogInfo(TR.ACT, f"{self.wave}-{self.round}-{subjc}행동",
                                                   self.random.getstate()))
            print(f"[act] ~~~ <{subjc}> 행동 ~~~", file=self.stream)
        if skill_no == 3:
            subjc.move(objpos)
            print(f"[mov] <{subjc}> - {objpos}번 위치로 이동함.", file=self.stream)
            return
        elif skill_no == 4:
            subjc.idle()
            print(f"[idl] <{subjc}> - 대기.", file=self.stream)
            return
        elif impact == 0:
            impact_turn = subjc.get_skill(skill_no-1, True)['impact'][subjc.skillvl[(skill_no-1) % 5]]
            if impact_turn >= 0:
                self.__impacts.append([impact_turn,
                                       (subjc, skill_no, objpos, catkr, follow, coop, impact_turn)])
                print(f"[imp] <{subjc}> - {impact_turn}턴 이후 착탄 예약됨.", file=self.stream)
                return
        if catkr is not None:
            skill_no = 1
        skill_no = subjc.skill_no_convert(skill_no)
        if not (catkr or follow or coop or impact):
            subjc.give_ap(-subjc.get_skill_cost(skill_no))
        skill_idx = skill_no - 1
        skillvl_val = subjc.skillvl[skill_idx % 5]
        fn = int(subjc.isenemy)
        isatk = bool(subjc.get_skill(skill_idx)['isattack'] & (1 << skillvl_val))
        tf = fn ^ isatk
        grid = subjc.get_skill(skill_idx)['isgrid'] & (1 << skillvl_val)
        ignp = subjc.get_skill(skill_idx)['isignoreprot'] & (1 << skillvl_val)
        if not grid and self.get_char(objpos, field=tf) is None:
            return  # 필드형 스킬이 아닌데 땅을 목표로 공격함.
        aoe = subjc.get_aoe(objpos, skill_no)
        aoetemp = {i[:2]: i[2] for i in aoe}
        targets = self.get_targets(aoe, ignp|(not isatk), field=tf)
        targ_atkr: Dict['Character', NUM_T] = {i[1]: 1 for i in targets.values()}
        targ_aoe_rate: Dict['Character', NUM_T] = {i[1]: aoetemp[p] for p, i in targets.items()}
        temp_protect_types: Dict['Character', str] = dict()
        for ptemp, ctemp in targets.items():
            prottype, protchar = ctemp
            if temp_protect_types.get(protchar) is None:
                temp_protect_types[protchar] = prottype
            elif prottype:
                if prottype == BT.TARGET_PROTECT or \
                        (prottype == BT.COLUMN_PROTECT and temp_protect_types[protchar] == BT.ROW_PROTECT):
                    temp_protect_types[protchar] = prottype
        for ptemp, ctemp in targets.items():
            if ctemp[0] == temp_protect_types[ctemp[1]] and ctemp[0] is not None:
                targ_aoe_rate[ctemp[1]] = aoetemp[ptemp]

        targ_hits: Dict['Character', NUM_T] = dict()
        ishit = False
        if isatk:
            if catkr is None and follow is None:
                subjc.trigger(TR.ATTACK)
                for t in targ_atkr:
                    t.trigger(TR.GET_ATTACKED)
            for t in targ_atkr:
                h_ = subjc.judge_hit(t, subjc.get_skill(skill_idx)['accbonus'][skillvl_val])
                if h_ > 0:
                    ishit = True
                targ_hits[t] = h_
                targ_atkr[t] *= h_
            if ishit and catkr is None and follow is None:
                subjc.trigger(TR.HIT)
        else:
            for t in targ_atkr:
                targ_hits[t] = 1

        atkr = subjc.get_skill_atk_rate(skill_no)
        for t in targ_atkr:
            targ_atkr[t] *= atkr
        damages: Dict['Character', NUM_T]
        if follow is None or coop is None:
            damages = subjc.active(
                skill_no, 
                targ_hits, 
                dict(zip(targ_atkr.keys(), zip(targ_atkr.values(), targ_aoe_rate.values()))), 
                len(aoe)
            )
            if damages is None:
                damages = dict()
        else:
            damages = {
                t: (subjc.calc_damage(t,
                                      targ_atkr[t],
                                      subjc.get_skill_element(skill_no),
                                      d(len(targets) - 1) / d(len(aoe) - 1) if len(aoe) > 1 else 0)
                    if targ_hits[t] > 0 else 0)
                for t in targ_atkr
            }
        for t in damages:
            damages[t] = t.give_damage(damages[t])
            # -1 = 방어막
            # -2 = 피해 무효
            if catkr is None:
                print(f"[dmg] <{t}> - <{subjc}>의 공격으로 {{ {simpl(damages[t])} }} 피해를 입음." +
                      (' (치명타)' if targ_hits[t] > 1 else ''), file=self.stream)
            elif follow is not None:
                print(f"[dmg] <{t}> - <{subjc}>의 지원공격으로 {{ {simpl(damages[t])} }} 피해를 입음." +
                      (' (치명타)' if targ_hits[t] > 1 else ''), file=self.stream)
            elif coop is not None:
                print(f"[dmg] <{t}> - <{subjc}>의 협동공격으로 {{ {simpl(damages[t])} }} 피해를 입음." +
                      (' (치명타)' if targ_hits[t] > 1 else ''), file=self.stream)
            else:
                print(f"[dmg] <{t}> - <{subjc}>의 반격으로 {{ {simpl(damages[t])} }} 피해를 입음." +
                      (' (치명타)' if targ_hits[t] > 1 else ''), file=self.stream)
        
        for t in damages:
            t.dead_judge_process(targ_hits[t], damages[t], subjc, skill_no, follow)

        self.trigger()
        
        if catkr or follow:
            return

        subjc.trigger(TR.AFTER_SKILL)
            
        counters = {t: t.find_buff(BT.COUNTER_ATTACK) for t in damages if t.attackable(subjc, 1) and t.hp > 0}
        if any(counters.values()):
            catkc = max(counters, key=lambda c: c.get_stats()[BT.ATK])
            catkr = counters[catkc][-1].value
            if coop:
                countobjpos = coop
            else:
                countobjpos = subjc.getposn()
            self._use_skill(catkc, 1, countobjpos, catkr=catkr)
            catkc.trigger(TR.AFTER_COUNTER)

        if ishit and (coopb := subjc.find_buff(BT.COOP_ATTACK)):
            coopb = coopb[-1]
            coopc, coopsk = coopb.data
            if grid:
                cooptarg = random.choice(list(damages.keys()))
            else:
                cooptarg = self.get_char(targets[Pos(objpos).xy()][1], field=tf)
            self._use_skill(coopc, coopsk, cooptarg.getposn(), coop=subjc.getposn())

        if followers := subjc.find_buff(BT.FOLLOW_ATTACK):
            followc = max(map(lambda b: b.data.attacker, followers), key=lambda c: c.get_stats()[BT.ATK])
            if grid:
                followtarg = random.choice(list(damages.keys()))
            else:
                followtarg = self.get_char(targets[Pos(objpos).xy()][1], field=tf)
            if followc.attackable(followtarg, 1):
                self._use_skill(followc, 1, followtarg.getposn(), follow=subjc)

    def use_impact_skills(self):
        tempskills = []
        for _ in range(len(self.__impacts)):
            isinfo = self.__impacts.popleft()
            if isinfo[1][0].hp <= 0:
                continue
            isinfo[0] -= 1
            if isinfo[0] < 0:
                h.heappush(tempskills, (-isinfo[1][0].get_spd(),) + isinfo[1])
            else:
                self.__impacts.append(isinfo)
        while tempskills:
            sk = h.heappop(tempskills)
            if sk[1].hp <= 0:
                continue
            self.use_skill(*sk[1:])

    def give_buff(self,
                  target: 'Character',
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
                  desc: Optional[str] = None,
                  force: bool = False,
                  chance: NUM_T = 100,
                  made_by: Optional['Character'] = None):
        """
        :param target: Character
        :param type_: BT.type_name
        :param opr: "+" = 0, "*" = 1
        :param value: NUM_T
        :param round_: int (=MAX)
        :param count: int (=MAX)
        :param count_trig: Set[str]
        :param efft: BET.BUFF/DEBUFF/ETC (=ETC)
        :param max_stack: int (=0=no limit)
        :param removable: bool
        :param tag: str
        :param data: NamedTuple in Datas
        :param desc: str
        :param force: bool
        :param chance: number between 0 and 100
        :param made_by: Character giving this buff
        """
        if made_by is None:
            made_by = inspect.currentframe().f_back.f_locals.get('self', None)
        buff = Buff(type_, opr, value, round_, count, count_trig, efft, max_stack, removable, tag, data, desc,
                    target, made_by)
        # 최대 중첩
        if 0 < max_stack <= target.stack_limited_buff_tags[tag]:
            target.remove_buff(tag=tag, force=True, limit=1)
        # 효과 저항 / 강화 해제 관련 메커니즘은 다음을 참고함
        # https://arca.live/b/lastorigin/47046451
        if not force:
            if efft != BET.NORMAL:
                for immune_buff in target.find_buff(type_=BT.IMMUNE_BUFF):
                    if buff.issatisfy(**immune_buff.data):
                        print(f"[bim] <{target}> - 버프 무효됨: [{buff}]", file=self.stream)
                        return None
                if target.judge_resist_buff(buff, chance):
                    print(f"[brs] <{target}> - 버프 저항함: [{buff}]" +
                          ("" if chance == 100 else f" ({chance}% 확률)"), file=self.stream)
                    return None
        if type_ == BT.REMOVE_BUFF:
            if data is not None:
                target.remove_buff(**data._asdict())
        elif type_ in BT.STATS_SET:
            target.statBuffs.append(buff)
        elif type_ == BT.AP:
            target.give_ap(value)
        elif type_ == BT.FORCE_MOVE:
            pass  # 밀기/당기기
        elif type_ in BT.ANIT_OS_SET:
            target.antiOSBuffs.append(buff)
        elif type_ == BT.TAKEDMGINC:
            target.dmgTakeIncBuffs.append(buff)
        elif type_ == BT.TAKEDMGDEC:
            target.dmgTakeDecBuffs.append(buff)
        elif type_ == BT.GIVEDMGINC:
            target.dmgGiveIncBuffs.append(buff)
        elif type_ == BT.GIVEDMGDEC:
            target.dmgGiveDecBuffs.append(buff)
        else:
            target.specialBuffs.append(buff)
        print(f"[bad] <{target}> - 버프 추가됨: [{buff}]" + ("" if chance == 100 else f" ({chance}% 확률)"),
              file=self.stream)
        if max_stack > 0:
            target.stack_limited_buff_tags[tag] += 1
        self.battle_log.append(buff)
        return buff

    def wave_start(self):
        if len(self.__characters) == 0:
            return
        self.battle_log.append(D.BattleLogInfo(TR.WAVE_START, f"{self.wave}웨이브시작", self.random.getstate()))
        self.wave += 1
        self.round = 0
        print(f"[wst] ============= {self.wave} 웨이브 시작 ================================================",
              file=self.stream)
        self.trigger(TR.WAVE_START)
        self.round_start()

    def wave_end(self):
        if len(self.__characters) == 0:
            return
        self.battle_log.append(D.BattleLogInfo(TR.WAVE_END, f"{self.wave}웨이브종료", self.random.getstate()))
        print(f"[wed] ============= {self.wave} 웨이브 종료 ================================================",
              file=self.stream)
        self.trigger(TR.WAVE_END)
        self.round = 0

    def round_start(self):
        if len(self.__characters) == 0:
            return
        self.battle_log.append(D.BattleLogInfo(TR.ROUND_START, f"{self.wave}-{self.round}라운드시작",
                                               self.random.getstate()))
        self.trigger(TR.ROUND_START)
        if self.round == 0:
            while True:
                characters = self.get_act_order()
                if characters[-1][1] >= 10:
                    break
                for c in characters:
                    c[0].give_ap(c[0].get_spd())
        self.round += 1
        print(f"[rst] ============= {self.wave}-{self.round} 라운드 시작 "
              f"================================================",
              file=self.stream)

    def round_end(self):
        if len(self.__characters) == 0:
            return
        self.use_impact_skills()
        self.battle_log.append(D.BattleLogInfo(TR.ROUND_START, f"{self.wave}-{self.round}라운드종료",
                                               self.random.getstate()))
        self.trigger(TR.ROUND_END)

    def go_next_round(self):
        if self.round > 0:
            self.round_end()
        self.round_start()

    def get_act_order(self, skill_uses: Dict['Character', Sequence[int]] = None):
        if skill_uses is None:
            skill_uses = dict()
        order = deque()
        for c in self.__characters:
            order.append(
                (c.ap, c.get_spd(), -BasicData.act_order_idx[c.isenemy*9+c.getposn()], c)
            )
        res = []
        while order:
            ap, spd, actord, char = order.popleft()
            bs.insort_left(res, (ap, spd, actord, char))
            if (skn := skill_uses.get(char)) and len(skn) > 0:
                skill_cost = char.get_skill_cost(char.skill_no_convert(skn[0]))
                if (newap := ap - skill_cost) >= 10:
                    order.append((newap, spd, actord, char))
                    del skn[0]
        return [(char, ap, spd, BasicData.act_order_revidx[-actord]) for ap, spd, actord, char in res]

    def get_act_order_str(self, skill_uses: Dict['Character', Sequence[int]] = None):
        order = self.get_act_order(skill_uses)
        restxt = ""
        for i, x in enumerate(order):
            restxt += f"#{len(order)-i} {x[0]} " \
                      f"({'적군' if x[0].isenemy else '아군'} {BasicData.keypad[x[3]]}번 자리)\n" \
                      f"AP = {x[1]} / 행동력 = {x[2]}\n\n"
        return restxt.rstrip()


class Buff:
    __id = 0
    attrs = ('type', 'opr', 'value', 'round',
             'count', 'count_triggers', 'efftype',
             'max_stack', 'removable', 'tag', 'data',
             'desc', 'owner')

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance.__id = cls.__id
        cls.__id += 1
        return instance

    def __init__(self,
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
                 desc: Optional[str] = None,
                 owner: Optional['Character'] = None,
                 made_by: Optional['Character'] = None,
                 game: Optional[Game] = None):
        self.type: str = type_
        self.opr: int = opr
        # 0 = '+', 1 = '*'
        # BT_NOVAL에 속하는 (값이 필요 없는) 버프의 경우 아무 값이나 넣어도 됩니다.
        # BT.ACTIVE_RESIST의 경우
        # "효과 저항 감소" 로직(기본 확률 증감)으로는 0,
        # "효과 저항"      로직(독립시행)으로는 1을 입력하세요.
        self.value: NUM_T = value
        self.round: int = round_
        self.count: int = count
        self.count_triggers: Set[str] = set() if count_trig is None else count_trig
        self.efftype: int = efft
        self.max_stack: int = max_stack
        self.removable: bool = removable
        self.tag: Optional[str] = tag
        self.data: Optional[Data] = data
        self.desc: Optional[str] = desc
        self.owner = owner
        self.made_by = made_by
        self.game = game
        self.expired = False

        self.random = None
        if self.owner:
            self.random = self.owner.random
        elif self.game:
            def custom_random(self, r=100, offset=0):
                return self.game.random.uniform(offset, offset + r)
            self.random = custom_random

        if self.type == BT.IMMUNE_DMG:
            self.count_triggers.add(TR.GET_HIT)
            self.count = self.value
        elif self.type == BT.BATTLE_CONTINUATION:
            self.count_triggers.add(TR.BATTLE_CONTINUED)
            self.count = 1
        elif self.type == BT.INSTANT_DMG:
            self.expired = True

    def getID(self):
        return self.__id

    def __copy__(self):
        return self

    def __deepcopy__(self):
        return Buff(**{a: getattr(self, a) for a in self.attrs}) 

    def __mul__(self, other):
        if isinstance(other, NUMBER):
            r = deepcopy(self)
            r.value *= other
            return r
        else:
            raise TypeError(f"잘못된 타입 : {type(other)}")

    def __imul__(self, other):
        if isinstance(other, NUMBER):
            self.value *= other
            return self
        else:
            raise TypeError(f"잘못된 타입 : {type(other)}")

    def __str__(self):
        result = ''
        if self.tag in GIMMICKS:
            result += f"[{self.desc if self.desc else self.tag}] : "
        elif self.desc:
            result += f"{self.desc} : "
        if isinstance(self.data, D.FDmgInfo):
            if self.data.element == 0 and self.type == BT.INSTANT_DMG:
                result += f"{self.data.subject}의 공격력의 {simpl(self.value*100):+}% 고정 피해"
            else:
                result += f"추가 {E.desc[self.data.element]} 피해 {simpl(self.value*100):+}%"
        elif isinstance(self.data, D.DmgHPInfo) and self.data.type_:
            result += f"{'대상' if self.data.type_-1 % 2 else '자신'}의 HP%가 " \
                      f"{'낮을' if self.data.type_-1 // 2 else '높을'}수록 {self.type} {simpl(self.value*100):+}%"
        else:
            if self.type == BT.ACTIVE_RESIST:
                if self.opr:
                    result += "효과 저항"
                else:
                    result += "효과 적용 확률"
            else:
                result += self.type
            if self.type not in BT_NOVAL:
                if self.opr:
                    result += f' {simpl(self.value * (1 if self.type == BT.ACTIVE_RESIST else 100)):+}%'
                else:
                    result += f' {simpl(self.value):+}' + \
                        ('%' if self.type in {
                            BT.EVA, BT.CRIT, BT.ACC, BT.ACTIVE_RESIST, BT.ACTIVE_RATE, *BT.ELEMENT_RES, BT.SKILL_RATE
                        } else '')
            elif self.type == BT.TARGET_PROTECT or self.type == BT.PROVOKED:
                result += f" ({self.data.target if self.data else None})"
            elif self.type == BT.FOLLOW_ATTACK:
                result += f" ({self.data.attacker if self.data else None})"
            elif self.type == BT.COOP_ATTACK:
                result += f" ({self.data.attacker if self.data else None} - " \
                          f"{self.data.skill_no if self.data else None}번 스킬)"
        result += ' '
        if self.round > 99:
            result += '(99+라운드, '
        else:
            result += f'({self.round}라운드, '
        if self.count > 99:
            result += '99+횟수) '
        else:
            result += f'{self.count}횟수) '
        result += f'{{{BET.desc[self.efftype]}}}'
        if not self.removable:
            result += " <해제 불가>"
        return result

    def __repr__(self):
        result = f"<Buff no.{self.__id:04d} desc={self.desc} " + self.type
        result += f'{"*" if self.opr else "+"}{simpl(self.value)} '
        if self.round > 99:
            result += '(99+라운드, '
        else:
            result += f'({self.round}라운드, '
        if self.count > 99:
            result += '99+횟수) '
        else:
            result += f'{self.round}횟수) '
        result += f'[{BET.desc[self.efftype]}]'
        if not self.removable:
            result += " 해제불가"
        if self.expired:
            result += " expired"
        result += '>'
        return result
    
    def calc(self, v, extra_rate=None):
        if extra_rate is None:
            extra_rate = d('1')
        if self.opr:
            if self.type == BT.DEFPEN:
                r = (d('1')-extra_rate*self.value)*v
            elif self.type == BT.DOT_DMG:
                r = self.value*extra_rate*v
            else:
                r = (d('1')+extra_rate*self.value)*v
        else:
            r = v+self.value*extra_rate
        return simpl(r)

    def trigger(self, tt, args=None):
        self.base_passive(tt, args)
        self.passive(tt, args)

    def base_passive(self, tt, args=None):
        if tt == TR.ROUND_END:
            self.round -= 1
        elif self.tag == G.PHOSPHIDE and tt == TR.GET_HIT and args.element == E.FIRE:
            self.owner.give_buff(BT.INSTANT_DMG, 0, d('.5'), efft=BET.DEBUFF,
                                 data=D.FDmgInfo(subject=args.attack), desc=G.PHOSPHIDE_DESC)
        if tt in self.count_triggers:
            self.count -= 1

    def passive(self, tt, args=None):
        pass
    
    def issatisfy(self, type_=None, efft=None, tag=None, func=None, id_=None, val_sign=None, chance=100, **kwargs):
        if self.random and self.random() > chance:
            return False
        if id_:
            if self.getID() != id_:
                return False
        if val_sign is not None:
            if self.value == 0:
                if val_sign != 0:
                    return False
            else:
                if self.value / abs(self.value) != val_sign:
                    return False
        if type_:
            if isinstance(type_, str) and self.type != type_:
                return False
            if isinstance(type_, Iterable) and self.type not in type_:
                return False
        if efft:
            if self.efftype != efft:
                return False
        if tag:
            if self.tag is None or not self.tag.startswith(tag):
                return False
        if func:
            if not (hasattr(func, '__call__') and func(self)):
                return False
        return True


class BuffList:
    def __init__(self, *buffs: Buff):
        self.buffs = deque(buffs)
    
    def __iter__(self):
        return self.buffs.__iter__()

    def __getitem__(self, idx):
        return self.buffs[idx]
    
    def __len__(self):
        return len(self.buffs)

    def __bool__(self):
        return len(self.buffs) > 0
    
    def __add__(self, other: 'BuffList'):
        r = BuffList(*self.buffs)
        for b in other:
            r.append(b)
        return r
    
    def __iadd__(self, other: 'BuffList'):
        for b in other:
            self.append(b)
        return self

    def __mul__(self, other):
        if isinstance(other, NUMBER):
            r = BuffList(*self.buffs)
            for _ in range(len(r.buffs)):
                b = r.popleft()
                b *= other
                r.append(b)
            return r
        else:
            raise TypeError(f"잘못된 타입 : {type(other)}")

    def __imul__(self, other):
        if isinstance(other, NUMBER):
            for _ in range(len(self.buffs)):
                b = self.popleft()
                b *= other
                self.append(b)
            return self
        else:
            raise TypeError(f"잘못된 타입 : {type(other)}")

    def __str__(self):
        result = []
        for b in self.buffs:
            result.append(str(b))
        return f'{len(result)}개의 버프:\n' + '\n'.join(result)

    @property
    def count(self):
        return len(self)
    
    def append(self, buff):
        if buff is None:
            return
        self.buffs.append(buff)
    
    def appendleft(self, buff):
        if buff is None:
            return
        self.buffs.appendleft(buff)
    
    def pop(self):
        return self.buffs.pop()
    
    def popleft(self):
        return self.buffs.popleft()

    def union(self, other: 'BuffList'):
        while other:
            self.append(other.popleft())
        return self
    
    def update(self, tt=TR.DUMMY, args=None, except_condition: Callable[[Buff], bool] = lambda b: False):
        removed = BuffList()
        immunedmg_activated = False
        battlecontinue_activated = False
        for i in range(len(self.buffs)):
            b = self.buffs.popleft()
            if except_condition(b):
                self.buffs.append(b)
                continue
            if (immunedmg_activated and b.type == BT.IMMUNE_DMG and tt == TR.GET_HIT) or \
                    (battlecontinue_activated and b.type == BT.BATTLE_CONTINUATION and tt == TR.BATTLE_CONTINUED):
                continue
            b.trigger(tt, args)
            if b.owner is not None and b.type == BT.DOT_DMG and tt == TR.ROUND_END and b.owner.hp > 0:
                element_rate = 1 if b.data.element == 0 else (1 - b.owner.get_res()[b.data.element] / 100)
                b.owner.give_damage(b.value * element_rate, True)
            if b.round > 0 and b.count > 0 and not (tt == TR.DUMMY and b.expired):
                self.buffs.append(b)
            else:
                if b.type == BT.IMMUNE_DMG and tt == TR.GET_HIT:
                    immunedmg_activated = True
                elif b.type == BT.BATTLE_CONTINUATION and tt == TR.BATTLE_CONTINUED:
                    battlecontinue_activated = True
                removed.append(b)
        return removed

    def find(self, type_=None, efft=None, tag=None, func=None, id_=None, val_sign=None, **kwargs):
        result = BuffList()
        if type_ or efft or tag or func or id_:
            for b in self.buffs:
                if b.issatisfy(type_, efft, tag, func, id_, val_sign):
                    result.append(b)
        return result

    def remove(self, type_=None, efft=None, tag=None, func=None, id_=None, val_sign=None, limit=MAX, force=False):
        result = BuffList()
        if type_ or efft or tag or func or id_:
            for _ in range(len(self.buffs)):
                if limit <= 0:
                    break
                b = self.buffs.popleft()
                if not(b.removable or force):
                    self.buffs.append(b)
                    continue
                if (b.removable or force) and b.issatisfy(type_, efft, tag, func, id_, val_sign):
                    result.append(b)
                    limit -= 1
                else:
                    self.buffs.append(b)
        return result
    
    def getSUM(self):
        return BuffSUM(self)


class BuffSUM:
    def __init__(self, buffs: BuffList):
        self.values = dict([(i, [d('0'), d('1')]) for i in bufftypes])
        for b in buffs:
            self.values[b.type][b.opr] += b.value

    def calc(self, t, v=d(1), opr_order=True, extra_rate=None):
        b = self.values[t]
        if extra_rate is None:
            extra_rate = d('1')
        if t == BT.DEFPEN:
            if opr_order:
                r = (v - b[0]) * (1 - (b[1] - 1) * extra_rate)
            else:
                r = v * (1 - (b[1] - 1) * extra_rate) - b[0]
        else:
            if opr_order:
                r = (v + b[0]) * (1 + (b[1] - 1) * extra_rate)
            else:
                r = v * (1 + (b[1] - 1) * extra_rate) + b[0]
        return simpl(r)
    
    def __add__(self, other: 'BuffSUM'):
        r = deepcopy(self)
        for b in self.values:
            self.values[b][0] += other.values[b][0]
            self.values[b][1] += other.values[b][1] - 1
        return r
    
    def __mul__(self, other):
        r = deepcopy(self)
        if isinstance(other, BuffSUM):
            for b in self.values:
                self.values[b][0] *= other.values[b][1]
                self.values[b][1] *= other.values[b][1]
                self.values[b][0] += other.values[b][0]
        elif isinstance(other, NUMBER):
            for b in self.values:
                self.values[b][0] *= other
                self.values[b][1] *= other
        else:
            raise ValueError(f"잘못된 타입 : {type(other)}")
        return r
