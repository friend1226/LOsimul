from ..lo_char import *


class RocCGeneratorChallenge2(Character):
    id_ = "RocCGenerator_Challenge2"
    name = "재생 애너지 컨덴서"
    code = "RocCGenerator_Challenge2"
    group = Group.PARASITE
    isenemy = True
    isags = True
    
    def _active1(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        desc = "전하 충전"
        for t in targets:
            if t.type_ == (CT.FLY, CR.ATTACKER) and t.isags:
                t.give_buff(BT.ATK, 1, d('.06'), efft=BET.BUFF, round_=99,
                            max_stack=5, tag=f"{self.code}_A1_ATK", desc=desc)
                t.give_buff(BT.AP, 0, 1, efft=BET.BUFF, desc=desc)
        return {}
    
    def _active2(self,
                 targets: Dict['Character', NUM_T],
                 atk_rate: Dict['Character', Tuple[NUM_T, NUM_T]],
                 bv: Sequence[NUM_T],
                 wr: NUM_T,
                 element: int):
        desc = "실드 충전"
        for t in targets:
            if t.isags:
                t.give_buff(BT.BARRIER, 0, 5000, efft=BET.BUFF, round_=3, desc=desc, overlap_type=BOT.RENEW)
        return {}
    
    def _passive1(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.ALLY_DEAD:
            self.give_buff(BT.BATTLE_CONTINUATION, 1, 1, round_=1, desc="자동 수복", overlap_type=BOT.RENEW)
    
    def _passive2(self, tt: str, args: Optional[Dict[str, Any]], targets: List[Tuple[int, int]], bv: List[NUM_T]):
        if tt == TR.BATTLE_CONTINUED:
            self.give_buff(BT.INABILLITY_ACT, 0, 1, round_=4, desc="복원 대기", overlap_type=BOT.RENEW)
