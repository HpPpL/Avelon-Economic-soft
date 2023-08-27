from typing import Any, Callable
from Units.Variables import Parameter


def to_million(method_to_decorate: Callable) -> Callable:
    def wrapper(self: Any, *args: Any) -> Parameter:
        value: Parameter = method_to_decorate(self, *args)
        value.units[0].change_view("млн.руб")
        return value

    return wrapper
