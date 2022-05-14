EDIT = 0

if EDIT:
    import os
    codes = []
    for filename in os.listdir(os.path.split(__file__)[0]):
        name = filename.rpartition('.')[0]
        if name == '' or name.startswith('__'):
            continue
        codes.append(f"    from .{name} import {name}\n")
    with open(__file__, 'r', encoding='utf-8') as f:
        origcodes = f.readlines()
    index = 0
    while True:
        if origcodes[index].startswith('if __name__'):
            break
        index += 1
    del origcodes[index+1:]
    origcodes.extend(codes)
    origcodes[0] = "EDIT = 0\n"
    with open(__file__, 'w', encoding='utf-8') as f:
        f.writelines(origcodes)
    del os

del EDIT

if __name__ != "__main__":
    from .Alice import Alice
    from .Cerestia import Cerestia
    from .Constantia import Constantia
    from .DummyAlly import DummyAlly
    from .DummyEnemy import DummyEnemy
    from .EliteCenturion1 import EliteCenturion1
    from .Ellie import Ellie
    from .Emily import Emily
    from .EratoOld import EratoOld
    from .Fotia import Fotia
    from .Goltarion import Goltarion
    from .Labiata import Labiata
    from .LegionEX1 import LegionEX1
    from .Lise import Lise
    from .LRL import LRL
    from .NightChickDetector3 import NightChickDetector3
    from .NightChickEX3 import NightChickEX3
    from .NightChickModifiedEX3 import NightChickModifiedEX3
    from .NightChickShielder3 import NightChickShielder3
    from .NightChickSniper1 import NightChickSniper1
    from .OrangeAde import OrangeAde
    from .Peregrinus import Peregrinus
    from .Phalangites1 import Phalangites1
    from .Rhea import Rhea
    from .Silky import Silky
    from .Titania import Titania
    from .TyrantChallenge1 import TyrantChallenge1
    from .UnderWatcher1 import UnderWatcher1
    from .UnderWatcher2 import UnderWatcher2
    from .UnderWatcherArm1 import UnderWatcherArm1
    from .UnderWatcherArm2 import UnderWatcherArm2
    from .UnderWatcherGenerator1 import UnderWatcherGenerator1
    from .UnderWatcherGenerator2 import UnderWatcherGenerator2
    from .UnderWatcherSensor1 import UnderWatcherSensor1
    from .UnderWatcherSensor2 import UnderWatcherSensor2
    from .Vanilla import Vanilla
