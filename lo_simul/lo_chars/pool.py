from .characters import *


class CharacterPools:
    ALL_CODES: Dict[str, Type['Character']]
    ALLY: Dict[str, Union[Type['Character'], str]]
    ENEMY: Dict[str, Union[Type['Character'], str]]
    ALL: Dict[str, Type['Character']]

    @classmethod
    def update(cls):
        cls.ALL_CODES = {}
        cls.ALLY = {}
        cls.ENEMY = {}
        for klass in Character.__subclasses__():
            cls.ALL_CODES[klass.code] = klass
            if klass.isenemy:
                cls.ENEMY[klass.name] = klass
            else:
                cls.ALLY[klass.name] = klass
        """
        cls.ALLY = {
            '라비아타': '3P_Labiata',
            '콘스탄챠': '3P_ConstantiaS2',
            '앨리스': '3P_Alice',
            '바닐라': '3P_Vanilla',
            '티타니아': '3P_Titania',
            '에밀리': 'BR_Emily',
            '골타리온': 'AGS_Goltarion',
            '엘리': 'BR_Ellie',
            '더미(아군)': 'DummyAlly',
        }
        cls.ENEMY = {
            '언더왓쳐 (5-8)': 'UnderWatcher_B05',
            '언더왓쳐 센서 (5-8)': 'UnderWatcherSensor_B05',
            '언더왓쳐 암 (5-8)': 'UnderWatcherArm_B05',
            '언더왓쳐 제네레이터 (5-8)': 'UnderWatcherGenerator_B05',
            '언더왓쳐 (5-8ex)': 'UnderWatcher_TU2',
            '언더왓쳐 센서 (5-8ex)': 'UnderWatcherSensor_TU2',
            '언더왓쳐 암 (5-8ex)': 'UnderWatcherArm_TU2',
            '언더왓쳐 제네레이터 (5-8ex)': 'UnderWatcherGenerator_TU2',
            '폭군 타이런트 (피조물과 설계자)': 'Tyrant_Challenge1',
            '강화형 칙 런쳐 (3-1ex)': 'NightChickMEX_TU3',
            '정예 레기온 (3-1ex)': 'LegionEX_TU',
            '팔랑스 (3-1ex)': 'Phalangites_TU',
            '칙 스나이퍼 (3-1ex)': 'NightChickSP_N',
            '강화형 나이트 칙 (3-1ex)': 'NightChickEX_TU3',
            '나이트 칙 실더 개 (3-1ex)': 'NightChickSI_TU3',
            '나이트 칙 디텍터 (3-1ex)': 'NightChickDE_TU3',
            '엘리트 셀츄리온 (3-1ex)': 'CenturionEX_TU',
            '더미(적군)': 'DummyEnemy',
        }

        for d in (cls.ALLY, cls.ENEMY):
            for c in d:
                d[c] = cls.ALL_CODES[d[c]]
        """

        cls.ALL = {**cls.ALLY, **cls.ENEMY}


CharacterPools.update()
