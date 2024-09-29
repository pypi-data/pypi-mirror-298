import traceback
from datetime import date, datetime

from kalib.dataclasses import dataclass
from kalib.datastructures import json
from kalib.internals import Who, class_of, sourcefile
from kalib.text import Str


def format_exception(exception):
    def trim(x):
        return tuple(i.rstrip() for i in x)

    def select_primitives_only(exception):
        if (args := getattr(exception, 'args', None)):
            result = []
            for item in args:
                if not item:
                    continue

                if isinstance(item, list | set):
                    item = tuple(item)  # noqa: PLW2901

                elif isinstance(item, date | datetime):
                    item = item.isoformat()  # noqa: PLW2901

                elif isinstance(item, bytes | float | int | str | tuple):
                    ...

                else:
                    try:
                        item = json.dumps(item)  # noqa: PLW2901
                    except Exception:  # noqa: S112, BLE001
                        continue

                result.append(item)

            if result:
                return json.dumps(result)

    cls = class_of(exception)

    data = {
        'exception' : cls.__name__,
        'module'    : cls.__module__,
        'name'      : Who(cls),
        'source'    : sourcefile(cls),
        'arguments' : select_primitives_only(exception),
        'message'   : Str(exception).strip() or None}

    return dataclass.dict({
        'verbose'   : f'{data["name"]}({data["arguments"] or ""}) {data["message"] or ""}',
        'traceback' : '\n'.join(trim(traceback.format_exception(exception)))})
