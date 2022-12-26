from ..lo_char import *


class Ellie(Character):
    _id = 230
    name = "엘리"
    code = "BR_Ellie"
    group = Group.AGENCY_080
    isenemy = False
    is21squad = False
    
    def _active1(self, 
                 targets: Dict['Character', NUM_T], 
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]], 
                 bv: Sequence[NUM_T], 
                 wr: NUM_T,
                 element: int):
        desc = "테이저 니들"
        for t in targets:
            if targets[t] > 0:
                t.give_buff(BT.AP, 0, bv[0], efft=BET.DEBUFF, desc=desc)
                t.give_buff(BT.ROOTED, 0, 1, efft=BET.DEBUFF, round_=2, desc=desc, overlap_type=BOT.RENEW)
                if t.get_stats(BT.SPD) > self.get_stats(BT.SPD):
                    t.give_buff(BT.AP, 0, bv[1], efft=BET.DEBUFF, desc=desc)
        return {t: (self.calc_damage(t, atk_rate[t], element=element, wr=wr) if targets[t] > 0 else 0) for t in targets}
    
    def _active2(self, 
                 targets: Dict['Character', NUM_T], 
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]], 
                 bv: Sequence[NUM_T], 
                 wr: NUM_T,
                 element: int):
        desc = "방호 모드"
        self.give_buff(BT.COUNTER_ATTACK, 1, bv[0], efft=BET.BUFF, round_=3, desc=desc, overlap_type=BOT.RENEW)
        self.give_buff(BT.IMMUNE_DMG, 0, 1, efft=BET.BUFF, round_=3, desc=desc)
        for t in targets:
            t.give_buff(BT.BARRIER, 0, bv[1], efft=BET.BUFF, round_=3,
                        max_stack=1, tag="Ellie_A2_BARRIER", overlap_type=BOT.UPDATE)
            t.give_buff(BT.ACTIVE_RESIST, 1, bv[2], efft=BET.BUFF, round_=3,
                        max_stack=1, tag="Ellie_A2_BARRIER", overlap_type=BOT.UPDATE)
    
    def _passive1(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ROUND_START:
            desc = "노블레스 오블리주"
            self.give_buff(BT.COLUMN_PROTECT, 0, 1, round_=1, efft=BET.BUFF, desc=desc, overlap_type=BOT.RENEW)
            self.give_buff(BT.TAKEDMGDEC, 1, bv[0], round_=1, desc=desc)
            if self.find_buff(BT.TAKEDMGDEC, efft=BET.BUFF):
                self.give_buff(BT.REMOVE_BUFF, 0, 1, data=D.BuffCond(type_=BT.TAKEDMGDEC, efft=BET.BUFF))
                self.give_buff(BT.REMOVE_BUFF_RESIST, 1, bv[1], round_=1, desc=desc)
            if self.find_buff(BT.RACON):
                self.give_buff(BT.ACC, 0, bv[2], round_=1, efft=BET.BUFF)
    
    def _passive2(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        desc = "편안한 티타임"
        if tt == TR.ROUND_START:
            for t in self.get_passive_targets(targets):
                t.give_buff(BT.WIDE_TAKEDMG, 1, bv[0], round_=1, efft=BET.BUFF, desc=desc)
                if t.type_[1] != CharRole.DEFENDER:
                    t.give_buff(BT.TARGET_PROTECT, 0, 1, data=D.TargetProtect(target=self), round_=1, efft=BET.BUFF,
                                desc=desc)
        elif tt == TR.AFTER_SKILL:
            if args.get("skill_no") == 2:
                for t in self.get_passive_targets(targets):
                    t.give_buff(BT.WIDE_TAKEDMG, 1, bv[0], count=2 if self.find_buff(BT.RACON) else 1, 
                                count_trig={TR.GET_HIT, }, efft=BET.BUFF, desc=desc, overlap_type=BOT.UPDATE)
        elif tt == TR.GET_HIT:
            for t in self.get_passive_targets(targets):
                t.give_buff(BT.ATK, 1, bv[1], round_=2, efft=BET.BUFF, 
                            max_stack=3, tag="Ellie_P2_ATK", overlap_type=BOT.UPDATE)

    def _passive3(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.WAVE_START:
            allys = self.game.get_chars(field=self.isenemy)
            if len(allys) == 5:
                self.give_buff(BT.RACON, 0, 1, overlap_type=BOT.RENEW, desc="정보 공유")
            dxs = (-1, 0, 1, 0)
            dys = (0, -1, 0, 1)
            adjacent = set(temppos for dx, dy in zip(dxs, dys) if (temppos := self.pos + (dx, dy)))
            adjacent.difference_update(set(allys.keys()))
            if len(adjacent) >= 4:
                self.give_buff(BT.MARKED, 0, 1, round_=1,
                               overlap_type=BOT.RENEW, desc="tous pour un")
            elif len(adjacent) >= 2:
                self.give_buff(BT.MARKED, 0, 1, efft=BET.BUFF, round_=1,
                               overlap_type=BOT.RENEW, desc="un pour tous")
            self.give_buff(BT.MINIMIZE_DMG, 0, bv[0] * (d('1.5') if self.hp_rate else 1), 
                           round_=1, efft=BET.BUFF, overlap_type=BOT.RENEW, desc="차분한 한 모금")
