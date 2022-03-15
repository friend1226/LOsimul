from RestrictedPython import compile_restricted, safe_globals
from RestrictedPython.Eval import default_guarded_getiter, default_guarded_getitem
from RestrictedPython.Guards import guarded_iter_unpack_sequence, safer_getattr
from RestrictedPython.PrintCollector import PrintCollector


class ModLoader:
    __compile_restricted = staticmethod(compile_restricted)
    __SAFE_GLOBALS = safe_globals

    import lo_simul
    import os

    # __PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'mod')
    __PATH = os.path.join(os.path.abspath('.'), 'mod')

    __LOSIMUL_GLOBALS = {k: v for k, v in vars(lo_simul).items()
                         if not (k.startswith('__') or
                                 k in {'os', 'sys', 'inspect', 'pickle', 'gzip'})}

    __SAFE_GLOBALS['__metaclass__'] = type
    __SAFE_GLOBALS['_getiter_'] = default_guarded_getiter
    __SAFE_GLOBALS['_getitem_'] = default_guarded_getitem
    __SAFE_GLOBALS['_iter_unpack_sequence_'] = guarded_iter_unpack_sequence
    __SAFE_GLOBALS['getattr'] = safer_getattr
    __SAFE_GLOBALS['_print_'] = PrintCollector

    __FUNCNAME = {
        'active1': '_active1',
        'active2': '_active2',
        'factive1': '_factive1',
        'factive2': '_factive2',
        'fpassive1': '_fpassive1',
        'fpassive2': '_fpassive2',
        'fpassive3': '_fpassive3',
        'passive1': '_passive1',
        'passive2': '_passive2',
        'passive3': '_passive3',
    }

    __CHARACTER = lo_simul.Character
    __EQUIP = lo_simul.Equip

    del lo_simul, os

    def get_path(self):
        return self.__PATH

    def set_path(self, path):
        self.__PATH = path

    def load(self):
        import os
        loc = {}
        errors = {}
        if os.path.isdir(self.__PATH):
            for fn in os.listdir(self.__PATH):
                if fn.endswith('.log'):
                    continue
                with open(os.path.join(self.__PATH, fn), 'r', encoding='utf-8') as f:
                    code = f.read()
                try:
                    tloc = {}
                    bytecode = self.__compile_restricted(source=code, filename=fn, mode='exec')
                    exec(bytecode, self.__SAFE_GLOBALS | self.__LOSIMUL_GLOBALS | {"__name__": fn}, tloc)
                except Exception as ex:
                    errors[fn] = ex
                else:
                    loc.update(tloc)
            for klass in loc.values():
                if issubclass(klass, self.__CHARACTER):
                    for fnc in self.__FUNCNAME:
                        if getattr(klass, fnc, None):
                            setattr(klass, self.__FUNCNAME[fnc], getattr(klass, fnc))
                            delattr(klass, fnc)
        del os
        return loc, errors


del compile_restricted, safe_globals, default_guarded_getitem, default_guarded_getiter, \
    guarded_iter_unpack_sequence, safer_getattr, PrintCollector
