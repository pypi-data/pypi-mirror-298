import logging as syslog
import traceback
import typing
from argparse import Namespace
from collections import OrderedDict, defaultdict
from dataclasses import dataclass
from functools import partial, wraps
from hashlib import md5
from inspect import stack
from logging import CRITICAL, DEBUG, ERROR, INFO, NOTSET, WARNING
from logging import Logger as BaseLogger
from os import getenv, sep
from pathlib import Path
from sys import _getframe, argv, getrefcount
from time import time
from typing import ClassVar
from weakref import ref

from kalib._internal import to_bytes
from kalib.descriptors import cache, pin, prop
from kalib.internals import (
    Nothing,
    Who,
    class_of,
    get_module_from_path,
    is_class,
    is_function,
    is_iterable,
    its_imported_module_name,
    stackoffset,
    stacktrace,
    trim_module_path,
    unique,
)
from kalib.misc import toml_read
from kalib.text import Str

DEPRECATE = INFO - 6
VERBOSE   = INFO - 3
NOTICE    = INFO + 5

CUSTOM_LEVELS = {
    CRITICAL  : 'CRIT',
    DEPRECATE : 'DEPR',
    NOTICE    : 'NOTE',
    NOTSET    : 'NONE',
    VERBOSE   : 'VERB',
    WARNING   : 'WARN',
}

CUSTOM_NAMES = {
    CRITICAL  : 'Critical',
    DEPRECATE : 'Deprecate',
    NOTICE    : 'Notice',
    NOTSET    : 'NotSet',
    VERBOSE   : 'Verbose',
    WARNING   : 'Warning',
}


DEDUP_ORDER_SIZE = 2 ** 16
DEFAULT_LOG_CONFIG = 'logging.toml'


def stack_length():
    result = 0
    f = _getframe(1)
    while f:
        result += 1
        f = f.f_back
    return result


def extract_options_from_kwargs(func=None, /, **fields):
    if func is None:
        return partial(extract_options_from_kwargs, **fields)

    elif not fields:
        return func

    fieldset = set(fields)
    Options = dataclass(kw_only=True)(type(  # noqa: N806
        'Options', (), {
            '__annotations__': {k: class_of(v) for k, v in fields.items()},
            **fields}))

    @wraps(func)
    def wrapper(self, *args, **kw):
        kw['options'] = Options(**{
            key: kw.pop(key) for key in fieldset & set(kw)
        } if kw else {})
        return func(self, *args, **kw)

    wrapper.Options = Options
    return wrapper


def format_function_args(args, kw):

    def a():
        return repr(args)[1:-1].rstrip(',')

    def k():
        return ','.join(f'{k}={Who.Is(v)}' for k, v in kw.items())

    if args and kw:
        return f'{a()}, {kw!r}'

    elif args:
        return f'{a()}'

    elif kw:
        return f'{kw!r}'

    return ''


class NumericOrSetter:
    def __init__(self, instance, attribute, value):
        self.instance  = instance
        self.attribute = attribute
        self.value     = value

    def __int__(self):
        return int(self.value)

    def __radd__(self, something):
        if isinstance(something, class_of(self)):
            return self.value + something.value

        elif isinstance(something, float | int):
            return self.value + something

        msg = (
            f'{Who(something)} can add only self or numeric, '
            f'not ({Who(something)}) {something!r}')
        raise TypeError(msg)

    __add__ = __radd__

    def __call__(self, value):
        setattr(self.instance, self.attribute,
            getattr(self.instance, self.attribute) + value)
        return self.instance

    def __repr__(self):
        return f'<{Who(self)}[{id(self):x}]={self.value!r}>'


class Logger(BaseLogger):

    _instances: ClassVar[dict] = {}

    @pin.cls
    def Catch(cls):
        return Logging.Catch

    @pin.cls
    def digest(cls):
        from kalib.importer import optional
        return optional('xxhash.xxh32_hexdigest', default=lambda x: md5(x).digest())  # noqa: S324

    @pin.root
    def getter(cls):
        func = syslog.getLogger
        if func.__name__ != 'getLogger':
            from kalib.monkey import Monkey
            return Monkey.mapping[func]
        return func

    @classmethod
    def make_for(cls, node):
        if isinstance(node, str):
            name = node
        else:
            node, name = class_of(node), Who(node)

        try:
            logger = cls._instances[name]

        except KeyError:
            logger = cls._instances[name] = cls.getter(name)
            logger.owner = node

        return logger

    def __init__(self, *args, **kw):
        self._owner = None
        self._stack = kw.pop('stack', 0)
        self._shift = kw.pop('shift', 0)
        super().__init__(*args, **kw)

    @pin.root
    def _already_logged(cls):
        return defaultdict(lambda: OrderedDict())

    @pin.root
    def levels(cls):
        """ Return levels dictionary."""

        def make_wrapper(name, level):
            qname = f'{Who(cls, full=False)}.{name}'

            def wrapper(self):
                if self.isEnabledFor(level):
                    def wrapped(*args, **kw):
                        return self.log(level, *args, **kw)
                else:
                    def wrapped(*args, **kw):
                        ...

                wrapped.__name__ = name
                wrapped.__qualname__ = qname
                wrapped.level = level
                return wrapped

            wrapper.__name__ = name
            wrapper.__qualname__ = qname
            return pin(wrapper)

        syslog.setLoggerClass(cls)
        for value, name in CUSTOM_LEVELS.items():
            syslog.addLevelName(value, name)

        for value in DEBUG, VERBOSE, NOTICE, INFO, WARNING, ERROR, CRITICAL:
            name = syslog._levelToName[value].lower()  # noqa: SLF001

            if name == (CUSTOM_NAMES.get(value) or name).lower():
                setattr(cls, name, make_wrapper(name, value))

            else:
                full = CUSTOM_NAMES[value].lower()
                func = make_wrapper(full, value)
                setattr(cls, full, func)
                setattr(cls, name, func)

        result = {
            **{k: v.capitalize() for k, v in syslog._levelToName.items()},  # noqa: SLF001
            **CUSTOM_NAMES,
        }
        levels = {k: result[k] for k in sorted(result)}

        for level, name in levels.items():
            setattr(Logging, name, level)

        cls.Levels = Namespace(
            **{name: level for level, name in levels.items()})

        return dict(levels)

    @pin
    def by_level(self):
        """ Return method by level."""

        @cache
        def wrapper(level):
            if isinstance(level, bool) or level is None:
                level = {
                    True  : Logging.Warning,
                    False : Logging.Info,
                    None  : Logging.Debug,
                }[level]

            elif not isinstance(level, int) or level < 0:
                msg = f'({Who(level)}) {level=} must me positive integer'
                raise TypeError(msg)

            return getattr(
                self, (self.levels.get(level) or self.Levels.Verbose).lower())

        wrapper.__name__ = 'by_level'
        wrapper.__qname__ = f'{Who(self)}.by_level'
        return wrapper

    @property
    def owner(self):
        """ Return owner of logger."""
        if (owner := self._owner) and (owner := owner()):
            return owner

    @owner.setter
    def owner(self, value):
        """ Set owner of logger."""
        try:
            self._owner = ref(value)
        except TypeError:
            self._owner = None

    @property
    def refs(self):
        """ Return number of references to owner."""
        if (owner := self.owner):
            return getrefcount(owner)
        return 0


    @property
    def stack(self):
        return NumericOrSetter(self, 'stack', self._stack)

    @stack.setter
    def stack(self, stack):
        self._stack += stack
        return self

    @property
    def shift(self):
        return NumericOrSetter(self, 'shift', self._shift)

    @shift.setter
    def shift(self, shift):
        self._shift += shift
        return self


    @extract_options_from_kwargs(
        shift   = 0,
        stack   = 0,
        count   = 0,

        once    = None,   # show this line only once, if False — show trace only once
        skip    = None,   # ignore files or sources with objects from this list

        trace   = False,  # show traceback
        context = True,   # with all lines instead selected one
    )
    def log(self, level, msg, *args, **kw):
        """ Log message with level."""

        if not self.isEnabledFor(level):
            return msg

        var = kw.pop('options')

        skip = [__file__]
        if isinstance(var.skip, bytes | str):
            skip.append(var.skip)
        elif is_iterable(var.skip):
            skip.extend(var.skip)

        trace = var.trace
        base_offset = stackoffset(skip)

        if var.once is not None:

            frame = stack()[-base_offset -1]
            frame = f'{frame.filename}:{frame.lineno:d}'
            cache = self._already_logged[frame]

            key = None if var.once else self.digest(to_bytes(f'{msg!a}:{args!a}'))
            already = key in cache

            if not already:
                cache[key] = int(time())
                if len(cache) >= DEDUP_ORDER_SIZE:
                    for _ in range( min(1, DEDUP_ORDER_SIZE - len(cache) + 10  ) ):
                        cache.popitem(last=False)

            elif var.once:
                return msg

            elif trace:
                trace = False

        trace_offset = (self.stack + var.stack) + (stack_length() - base_offset)
        stack_offset = (self.shift + var.shift) + base_offset + 1

        kw.setdefault('extra', {'refs': self.refs})
        kw.setdefault('stack_info', False)
        kw.setdefault('stacklevel', trace_offset)

        method = super().log
        if not trace or len(args) > 1:
            method(level, msg, *args, **kw)
            return msg

        lines = stacktrace(stack_offset * (-1, 1)[bool(var.context)], join=not var.count)
        if lines:
            lines = lines[-var.count:]

        msg = '{0}\n{1}\n{2}: {0}'.format(
                msg, ''.join(lines).rstrip(),
                self.levels.get(level, f'UnknownLevel{level:d}'))
        method(level, msg, *args, **kw)
        return msg

    def deprecate(self, msg, *args, **kw):
        kw.setdefault('once', True)
        kw.setdefault('trace', True)
        kw.setdefault('context', False)
        return self.log(DEPRECATE, msg, *args, **kw)

    def trace(self, msg, *args, **kw):
        kw.setdefault('once', False)
        kw.setdefault('trace', True)
        kw.setdefault('context', False)
        return self.log(WARNING, msg, *args, **kw)

    def fail(self, exception, *args, **kw):

        try:
            from tools.exceptions import format_exception
            e = format_exception(exception)

            title = e.message or 'Unknown exception'
            message = f'{e.traceback}'

        except ImportError:
            def trim(x):
                return tuple(i.rstrip() for i in x)

            title = Str(exception).strip() or 'Unknown exception'
            message = '\n'.join(trim(traceback.format_exception(exception)))

        except Exception as e:  # noqa: BLE001
            msg = f'{exception!r} {e}'
            self.log.warning(msg, *args, **kw)
            return msg

        title = f'{title.rstrip().rstrip(":")}:'
        return self.log(CRITICAL, f'{title}\n{message}', *args, **kw)


class Logging:

    class Mixin:

        @pin.cls
        def log(cls):
            return Logging.get(cls)

        @pin.cls
        def logger(cls):
            log = cls.log
            log.deprecate(f'-> {Who(cls)}.log', shift=-5, stack=5)
            return log

    loggers          : typing.ClassVar[dict] = {}
    path_nodes       : typing.ClassVar[list] = []
    configured_files : typing.ClassVar[list] = []

    @classmethod
    def from_filename(cls, path, **kw):
        """ Return logger for file."""

        reason, short = trim_module_path(path)
        if reason is not None:
            short = short.rsplit('.', 1)[0]

            if short.endswith('__init__'):
                short = short.rsplit(sep, 1)[0]

            return cls.get(short.replace(sep, '.'), **kw)

        if Path(argv[0]).absolute() == Path(path).absolute():
            return cls.get(Path(path).stem, **kw)

    @prop.cls
    def Default(cls):  # noqa: N802
        """ Return default logger for current module."""

        def get_lastframe():
            for frame in stack()[2:]:
                if (
                    f'{cls.__name__}.Default' in
                    repr(frame.code_context or '')
                ):
                    return frame

        if pointer := get_lastframe():
            cls.path_nodes.append(pointer.filename)
            if logger := cls.from_filename(pointer.filename):
                return logger

        return cls.get('<unknown>')

    @pin.root
    def config(cls):
        """ Return logging configuration object."""
        import logging.config as config  # noqa: PLR0402
        return config

    @pin.root
    def Force(cls):  # noqa: N802
        """ Force logging to be enabled."""

        def get():
            result = getenv('LOGGING_FORCE', '')
            if not result or result.lower() == 'false':
                return False

            elif result.isdigit():
                return bool(int(result))

            return bool(result) or False

        if (force := get()):
            LOGGING_FORCE = getenv('LOGGING_FORCE', '')  # noqa: N806
            cls.log.verbose(f'={force} ({LOGGING_FORCE=})', stack=-1)
        return force

    @pin.root
    def Debugging(cls):  # noqa: N802
        """ Force debugging to be enabled."""

        result = getenv('DEBUG', '')
        if not result or result.lower() == 'false':
            return False

        elif result.isdigit():
            return bool(int(result))

        return bool(result) or False

    @pin.root
    def config_path(cls):
        """ Return path to logging configuration file."""

        if (
            (path := getenv('LOGGING', None)) and
            Path(path).is_file()
        ):
            return str(path)
        return getenv('LOGGING_CONFIG', None)


    @pin.cls
    def directories_from_callstack(cls):
        """ Return directories from callstack."""

        seen = set()

        def iterfiles():
            yield __file__
            yield from unique(cls.path_nodes)
            for frame in stack():
                if not Path(frame.filename).is_file():
                    continue
                yield frame.filename

        def iterpath():
            for path in unique(iterfiles()):
                path = str(Path(path).resolve().parent)  # noqa: PLW2901
                if path not in seen:
                    seen.add(path)
                    yield Path(path)

        return tuple(iterpath())

    @classmethod
    def iter_config_files(cls, iterable=None):

        if isinstance(iterable, str):
            iterable = [Path(iterable)]

        seen = set()
        for root in (iterable or cls.directories_from_callstack):
            if root.is_file():
                root = root.parent  # noqa: PLW2901

            last = None
            while True:
                path = (root / DEFAULT_LOG_CONFIG).resolve()
                if last is not None and last == path:
                    break

                if path.is_file() and path not in seen:
                    seen.add(path)
                    yield path

                if str(root) == sep:
                    break
                root = root.parent  # noqa: PLW2901
                last = path

    @classmethod
    def configure(cls, path=None):  # noqa: PLR0912
        """ Configure logging from file."""

        if not path and cls.config_path and cls.configured_files:
            return

        def iterconfigs(path):
            if not path:
                yield from cls.iter_config_files(cls.directories_from_callstack)
            else:
                yield path

        default_logger = cls.log
        for file in unique(iterconfigs(path or cls.config_path)):
            if str(file) in cls.configured_files:
                continue

            if not Path(file).is_file():
                default_logger.error(f"logging file file {file!r} isn't accessible")

            config = dict(toml_read(file))
            if not cls.config_path:
                if config.get('disable_existing_loggers'):
                    default_logger.verbose(
                        f'{file} try to override '
                        f'{config["disable_existing_loggers"]=}')

                config['incremental'] = True
                config['disable_existing_loggers'] = path and not cls.loggers

                loggers = {}

                for name, logger in config.get('loggers', {}).items():
                    if cls.Debugging:
                        logger['level'] = 'DEBUG'

                    if name not in cls.loggers:
                        level = logger['level']
                        msg = f'{file} {level}({syslog.getLevelName(level)}): {name}'
                        default_logger.debug(msg)

                    else:
                        before, after = cls.loggers[name]['level'], logger['level']
                        if before != after:
                            aft = syslog.getLevelName(after)
                            bef = syslog.getLevelName(before)

                            if bef == aft:
                                continue

                            msg = f'{file} {before}({bef}): {name} -> {after}({aft})'
                            if bef > aft:
                                msg = f'{msg} [ignored]'
                            default_logger.info(msg)

                config['loggers'] = loggers
                cls.loggers.update(loggers)

            cls.from_dict(**config)
            cls.configured_files.append(str(file))
            default_logger.info(f'rules applied: {file}')

        return cls

    @classmethod
    def from_dict(cls, **kw):
        cls.config.dictConfig(kw)
        return cls

    @classmethod
    def get(cls, node, configure=True, *args, **kw):  # noqa: ARG003
        if configure:
            cls.configure()

        klass = syslog.getLoggerClass()
        if klass is not Logger:
            from kalib.misc import sourcefile
            cls.log.verbose(
                f'somebody override defined logger {Who(Logger)} '
                f"with {Who(klass)}{sourcefile(klass, 'from %r')}")
            syslog.setLoggerClass(Logger)

        if cls is not node:
            logger = cls.log.make_for(node)
        else:
            logger = syslog.getLogger(Who(node))

        if class_of(logger) is not Logger:
            msg = (
                f"couldn't restore defined logger {Who(Logger)} "
                f'instead override {Who(klass)}')
            raise TypeError(msg)

        if (level := (kw.pop('level', DEPRECATE), DEBUG)[cls.Debugging]):
            logger.setLevel(level)
        return logger

    @pin.root
    def log(cls):
        order = []
        level = ('DEPR', 'NOTSET')[cls.Debugging]

        if not cls.config_path:
            for no, file in enumerate(cls.iter_config_files(__file__)):
                config = dict(toml_read(file))
                config['disable_existing_loggers'] = not bool(no)
                if not no:
                    config['loggers']['root']['level'] = level

                cls.from_dict(**config)
                order.append(str(file))

        logger = cls.get(cls, configure=False, level=DEPRECATE)
        if not cls.config_path and not cls.configured_files:
            logger.verbose(f'autoconfigured from: {", ".join(order)}')
        cls.configured_files.extend(order)
        return logger

    @pin.root
    def logger(cls):
        log = cls.log
        log.deprecate(f'-> {Who(cls)}.log', shift=-5, stack=5)
        return log

    @classmethod
    def Catch(cls, *exceptions, **kw):
        throw = kw.pop('throw', True)
        from kalib.exceptions import format_exception

        def method_wrapper(func):

            def get_logger(exc, args, kw):
                head = (
                    f'.{Who(func)}({format_function_args(args, kw)}) hit '
                    f'{format_exception(exc).verbose}')

                if args:
                    if logger := getattr(args[0], 'log', None):
                        return logger, head
                    if logger := getattr(args[0], 'logger', None):
                        return logger, head
                return cls.Default, head

            @wraps(func)
            def expect(*args, **kw):
                try:
                    return func(*args, **kw)

                except exceptions as e:
                    logger, head = get_logger(e, args, kw)
                    logger.warning(': expected exception')
                    if throw:
                        raise e

                except Exception as e:
                    logger, head = get_logger(e, args, kw)
                    logger.exception(': unexpected exception')
                    raise e

            return expect

        if not exceptions:
            exceptions = (Exception,)

        elif (
            len(exceptions) == 1 and
            (is_function(exceptions[0]) or is_class(exceptions[0]))
        ):
            func = exceptions[0]
            exceptions = (Exception,)
            return method_wrapper(func)

        return method_wrapper

    def from_object(node):
        if logger := getattr(node, 'log', Nothing):
            return logger
        return Logging.get(node)


def injector(func, *args, **kw):  # noqa: ARG001

    if not args:
        for frame in stack():
            if 'getLogger' in repr(frame.code_context or ''):
                if (
                    (result := Logging.from_filename(frame.filename)) or
                    (
                        (result := get_module_from_path(frame.filename)) and
                        (result := Logging.get(get_module_from_path(frame.filename)))
                    )
                ):
                    return result

                if frame.function != '<module>':
                    msg = f'named module, {frame=}'
                    raise NotImplementedError(msg)

        args = (stack()[2].function,)

    if not its_imported_module_name(args[0]):
        name = args[0]
        logger.debug(
            f'incorrect module log name: must be full module path, not {name=}',
            trace=-2, shift=-2, count=1)

    return Logging.get(args, *args[1:], **kw)


Logger.levels  # noqa: B018, add custom levels, set out class instead default
logger = Logging.Default

if Logging.Force:
    from kalib.monkey import Monkey
    Monkey.wrap(syslog, 'getLogger')(injector)
