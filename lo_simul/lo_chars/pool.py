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

        cls.ALL = {**cls.ALLY, **cls.ENEMY}


CharacterPools.update()
