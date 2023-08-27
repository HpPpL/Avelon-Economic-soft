import numpy as np

from Units.Units import (
    MassUnits,
    VolumeUnits,
    RubUnit,
    USDUnit,
    Unit,
    PercentUnit,
    UnitStack,
    OneUnit,
    SquareUnits,
    TimeUnit,
)
from copy import deepcopy
from typing import Union, Dict, List

Choice: Dict[str, List[Union[str, float]]] = {
    "cent": ["cent"],
    "USD": ["USD", "дол", "долл"],
    "тыс.USD": [
        "тыс.USD",
        "тыс. USD",
        "тыс USD",
        "тыс.дол",
        "тыс. дол",
        "тыс дол",
        "тыс.долл",
        "тыс. долл",
        "тыс долл",
        "тыс.дол.",
        "тыс. дол.",
        "тыс дол.",
        "тыс.долл.",
        "тыс. долл.",
        "тыс долл.",
    ],
    "млн.USD": [
        "млн.USD",
        "млн. USD",
        "млн USD",
        "млн.дол",
        "млн. дол",
        "млн дол",
        "млн.долл",
        "млн. долл",
        "млн долл",
        "млн.дол.",
        "млн. дол.",
        "млн дол.",
        "млн.долл.",
        "млн. долл.",
        "млн долл.",
    ],
    "млрд.USD": [
        "млрд.USD",
        "млрд. USD",
        "млрд USD",
        "млрд.дол",
        "млрд. дол",
        "млрд дол",
        "млрд.долл",
        "млрд. долл",
        "млрд долл",
        "млрд.дол.",
        "млрд. дол.",
        "млрд дол.",
        "млрд.долл.",
        "млрд. долл.",
        "млрд долл.",
    ],
    "трлн.USD": [
        "трлн.USD",
        "трлн. USD",
        "трлн USD",
        "трлн.дол",
        "трлн. дол",
        "трлн дол",
        "трлн.долл",
        "трлн. долл",
        "трлн долл",
        "трлн.дол.",
        "трлн. дол.",
        "трлн дол.",
        "трлн.долл.",
        "трлн. долл.",
        "трлн долл.",
    ],
    "коп": ["коп", "коп."],
    "руб": ["руб", "руб."],
    "тыс.руб": [
        "тыс.руб",
        "тыс. руб",
        "тыс руб",
        "тыс.руб.",
        "тыс. руб.",
        "тыс руб.",
    ],
    "млн.руб": [
        "млн.руб",
        "млн. руб",
        "млн руб",
        "млн.руб.",
        "млн. руб.",
        "млн руб.",
    ],
    "млрд.руб": [
        "млрд.руб",
        "млрд. руб",
        "млрд руб",
        "млрд.руб.",
        "млрд. руб.",
        "млрд руб.",
    ],
    "трлн.руб": [
        "трлн.руб",
        "трлн. руб",
        "трлн руб",
        "трлн.руб.",
        "трлн. руб.",
        "трлн руб.",
    ],
    "мл": ["мл"],
    "л": ["л"],
    "барр": ["барр"],
    "м3": ["м3"],
    "тыс.м3": ["тыс.м3", "тыс. м3", "тыс м3"],
    "млн.м3": ["млн.м3", "млн. м3", "млн м3"],
    "млрд.м3": ["млрд.м3", "млрд. м3", "млрд м3"],
    "мг": ["мг"],
    "г": ["г"],
    "кг": ["кг"],
    "т": ["т", "т."],
    "тыс.т": ["тыс.т", "тыс. т", "тыс т"],
    "млн.т": ["млн.т", "млн. т", "млн т"],
    "млрд.т": ["млрд.т", "млрд. т", "млрд т"],
    "единиц": ["шт", "штук", "ед", "единиц", np.NaN, "операц.", "операц"],
    "доли ед.": ["доли ед.", "доли. ед.", "доли ед", "доли.ед.", "доля ед"],
    "%": ["%"],
    "га": ["га"],
    "м2": ["м2"],
    "год": ["год"],
    "месяц": ["месяц"],
}


def choose_true_name(string: str) -> str:
    for key in Choice.keys():
        if string in Choice[key]:
            return key

    raise KeyError()


def choose_unit(string: str, exponent: Union[float, int] = 1) -> Unit:
    target = [
        MassUnits,
        VolumeUnits,
        RubUnit,
        USDUnit,
        PercentUnit,
        OneUnit,
        SquareUnits,
        TimeUnit,
    ]
    for main_unit in target:
        if string in main_unit.factor.keys():
            unit = deepcopy(main_unit)
            unit.change_view(string)
            unit.exponent = exponent
            return unit


def define_unit(string: str) -> UnitStack:
    string = string.lower()
    if "/" in string:
        dimension = string.split("/")
        str_numerator = choose_true_name(dimension[0].strip())
        str_denominator = choose_true_name(dimension[1].strip())
        numerator = choose_unit(str_numerator)
        denominator = choose_unit(str_denominator, -1)
        unit_stack = UnitStack()
        unit_stack.append(numerator)
        unit_stack.append(denominator)
        return unit_stack
    else:
        str_numerator = choose_true_name(string.strip())
        numerator = choose_unit(str_numerator)
        unit_stack = UnitStack()
        unit_stack.append(numerator)
        return unit_stack
