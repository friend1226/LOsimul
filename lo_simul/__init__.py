from .lo_enum import *
from .lo_imports import *
from .lo_system import *
from .lo_char_base import *
from .lo_chars import *
from .lo_equips import *
from .lo_mod import *

import traceback
modloader = ModLoader()
path = modloader.get_path()
classes, errors = modloader.load()
for fn in errors:
    with open(os.path.join(path, fn.rpartition('.')[0]+'.log'), 'w', encoding='utf-8') as f:
        f.writelines(traceback.format_exception(type(errors[fn]), errors[fn], errors[fn].__traceback__))
pool.CharacterPools.update()
EquipPools.update()
del traceback
