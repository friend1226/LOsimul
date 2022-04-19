__all__ = [
    "Alice",
    "Constantia",
    "DummyAlly",
    "DummyEnemy",
    "EliteCenturion1",
    "Ellie",
    "Emily",
    "Fotia",
    "Goltarion",
    "Labiata",
    "LegionEX1",
    "Lise",
    "NightChickDetector3",
    "NightChickEX3",
    "NightChickModifiedEX3",
    "NightChickShielder3",
    "NightChickSniper1",
    "Phalangites1",
    "Rhea",
    "Titania",
    "TyrantChallenge1",
    "UnderWatcher1",
    "UnderWatcher2",
    "UnderWatcherArm1",
    "UnderWatcherArm2",
    "UnderWatcherGenerator1",
    "UnderWatcherGenerator2",
    "UnderWatcherSensor1",
    "UnderWatcherSensor2",
    "Vanilla",
]

import os
import importlib

path = os.path.join(os.path.split(__file__)[0], '.')
for char_filename in os.listdir(path):
    try:
        if not os.path.isfile(os.path.join(path, char_filename)):
            continue
        name = char_filename.partition(".")[0]
        module = importlib.import_module(f'.{name}', 'lo_simul.characters')
        globals()[name] = getattr(module, name)
    except Exception as e:
        print(e)

    # TODO: 작업은 파일을 나눠서 하고, 배포할 때 코드를 한데 모아서 배포하면 어떨까?

try:
    del char_filename, name, module
except:
    pass
del os, importlib, path
