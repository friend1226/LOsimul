from .lo_enum import *
from .lo_imports import *
from .lo_system import *
from .lo_char import *
from .lo_char import Character
from .lo_equips import *
from .lo_mod import *

lo_variables = set(globals().keys())

import os
import importlib

path = os.path.join(os.path.split(__file__)[0], 'characters')
for char_filename in os.listdir(path):
    try:
        if not os.path.isfile(os.path.join(path, char_filename)):
            continue
        name = char_filename.partition(".")[0]
        module = importlib.import_module(f'.characters.{name}', 'lo_simul')
        variables = {item: vars(module)[item] for item in dir(module)
                     if not (item.startswith('__') or item in lo_variables)}
        klass = type(name, (Character,), variables)
        globals()[name] = klass
        # TODO: 그냥 모듈 안에 클래스로 만들어서 type checking에도 쓰이게끔 할 것
    except Exception as e:
        print(e)

try:
    del char_filename, name, module, variables, klass
except:
    pass
del os, importlib, path

import traceback
modloader = ModLoader()
path = modloader.get_path()
classes, errors = modloader.load()
for fn in errors:
    with open(os.path.join(path, fn.rpartition('.')[0]+'.log'), 'w', encoding='utf-8') as f:
        f.writelines(traceback.format_exception(type(errors[fn]), errors[fn], errors[fn].__traceback__))
EquipPools.update()
try:
    del fn
except NameError:
    pass
del traceback, path, classes, errors, modloader, lo_variables

__version__ = "0b.20220414"
