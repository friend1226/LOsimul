from ..lo_char import *


class Peregrinus(Character):
    _id = 239
    name = "페레그리누스"
    code = "PECS_Peregrinus"
    group = Group.BISMARK
    isenemy = False
    isags = True

    def isformchanged(self):
        return bool(self.find_buff(type_=BT.GIMMICK, tag=G.PEREGRINUS_HUMAN))

    def skill_idx_convert(self, skill_idx):
        if skill_idx < 3 and self.isformchanged():
            return skill_idx + 5
        return skill_idx

    def _active1(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        desc = "꿰뚫는 깃털"
        for t in targets:
            if targets[t] > 0:
                if targets[t] > 1:
                    t.give_buff(BT.TAKEDMGINC, 1, bv[0], overlap_type=BOT.INSTANCE, desc=desc)
                t.give_buff(BT.DEF, 1, bv[1], efft=BET.DEBUFF, round_=3, desc=desc)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _active2(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        desc = "질풍격"
        for t in targets:
            if targets[t] > 0:
                self.give_buff(BT.IGNORE_BARRIER_DMGDEC, 0, 1, efft=BET.BUFF, overlap_type=BOT.INSTANCE, desc=desc)
                self.give_buff(BT.SKILL_RATE, 0, bv[0] / 100, proportion=(self, BT.EVA), efft=BET.BUFF, overlap_type=BOT.INSTANCE,
                               desc=desc)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _passive1(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START:
            desc = "팔콘 폼"
            self.give_buff(BT.CRIT, 0, bv[0], max_stack=5, efft=BET.BUFF, desc=desc, tag=G.PEREGRINUS_FALCON+"_CRIT")
            self.give_buff(BT.EVA, 0, bv[1], max_stack=5, efft=BET.BUFF, desc=desc, tag=G.PEREGRINUS_FALCON+"_EVA")
        elif tt == TR.WAVE_START:
            self.give_buff(BT.GIMMICK, 0, 1, desc=G.PEREGRINUS_READY, tag=G.PEREGRINUS_READY)
        elif tt == TR.IDLE and self.find_buff(type_=BT.GIMMICK, tag=G.PEREGRINUS_READY):
            self.give_buff(BT.GIMMICK, 0, 1, desc=G.PEREGRINUS_HUMAN, tag=G.PEREGRINUS_HUMAN)

    def _passive2(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START:
            desc = "위대한 하피의 왕"
            self.give_buff(BT.ATK, 1, bv[0], round_=1, efft=BET.BUFF, desc=desc)
            self.give_buff(BT.SPD, 1, bv[1], round_=1, efft=BET.BUFF, desc=desc)
            self.give_buff(BT.SKILL_RATE, 0, bv[0] / 100, proportion=(self, BT.EVA), round_=1, efft=BET.BUFF, desc=desc)

    def _passive3(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START:
            desc = "뛰어난 적응력"
            falcon = self.find_buff(type_=BT.EVA, tag=G.PEREGRINUS_FALCON).count
            human = self.find_buff(type_=BT.WIDE_GIVEDMG, tag=G.PEREGRINUS_HUMAN).count
            if falcon:
                self.give_buff(BT.AP, 0, bv[0]*(falcon+1)/2, efft=BET.BUFF, desc=desc)
            if human:
                self.give_buff(BT.ATK, 1, bv[0]*human/5, efft=BET.BUFF, round_=1, desc=desc)

    def _factive1(self,
                  targets: Dict['Character', NUM_T],
                  atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                  bv: Sequence[NUM_T],
                  wr: NUM_T,
                  element: int):
        desc = "페레그린 킥"
        for t in targets:
            if targets[t] > 0:
                t.give_buff(BT.EVA, 0, bv[0], efft=BET.DEBUFF, round_=3, desc=desc)
                if t.find_buff(type_={BT.ROW_PROTECT, BT.COLUMN_PROTECT}, func=lambda b: b.efft != BET.DEBUFF):
                    t.give_buff(BT.TAKEDMGINC, 1, bv[1], overlap_type=BOT.INSTANCE, desc=desc)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _factive2(self,
                  targets: Dict['Character', NUM_T],
                  atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                  bv: Sequence[NUM_T],
                  wr: NUM_T,
                  element: int):
        desc = "하피 왕의 숨결"
        if any(targets.values()):
            self.give_buff(BT.DEFPEN, 0, bv[0], efft=BET.BUFF, overlap_type=BOT.INSTANCE, desc=desc)
        for t in targets:
            if targets[t] > 0:
                t.give_buff(BT.REMOVE_BUFF, 0, 1, desc=desc, data=D.BuffCond(type_=BT.BARRIER, efft=BET.BUFF))
                t.give_buff(BT.WIDE_TAKEDMG, 1, bv[1]*len(self.game.get_chars(field=not self.isenemy))/9,
                            round_=1, efft=BET.DEBUFF, desc=desc)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}

    def _fpassive1(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.AFTER_SKILL:
            if args["skill_no"] == 7:
                self.give_buff(BT.REMOVE_BUFF, 0, 1, desc="휴먼 폼 모드 해제",
                               data=D.BuffCond(type_=BT.GIMMICK, tag=G.PEREGRINUS_HUMAN))
                self.give_buff(BT.REMOVE_BUFF, 0, 1, desc="모드 전환 종료",
                               data=D.BuffCond(type_=BT.GIMMICK, tag=G.PEREGRINUS_READY))
        elif tt == TR.ROUND_START:
            self.give_buff(BT.WIDE_GIVEDMG, 1, bv[0], max_stack=5, efft=BET.BUFF,
                           desc=G.PEREGRINUS_HUMAN, tag=G.PEREGRINUS_HUMAN)
