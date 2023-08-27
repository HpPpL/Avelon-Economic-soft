from __future__ import annotations

from typing import Dict, Union, List, Iterator, Generator
from copy import deepcopy


class Unit:
    SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
    SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")

    def __init__(
        self,
        factor: Dict[str, Union[float, int]],
        isu: str,
        name: str,
        view: str = None,
    ) -> None:
        self.exponent = 1
        self.name: str = name
        self.factor: Dict[str, Union[float, int]] = factor
        self.ISU: str = isu

        if view:
            self.view: str = view
        else:
            self.view = isu

        self.__check()

    def __lt__(self, other: Unit) -> bool:
        s1 = str(other)
        s2 = self.__str__()
        return s1 < s2

    def __gt__(self, other: Unit) -> bool:
        s1 = str(other)
        s2 = self.__str__()
        return s1 > s2

    def __check(self) -> None:
        if self.ISU not in self.factor.keys():
            raise ValueError("Еденица СИ не указана")
        if self.factor[self.ISU] != 1:
            raise ValueError("Не верная еденица СИ")
        if self.view not in self.factor.keys():
            raise ValueError("Еденица СИ не указана")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Unit):
            return NotImplemented
        first_check = other.factor == self.factor
        second_check = other.exponent == self.exponent
        return first_check & second_check

    def __getitem__(self, key: str) -> Union[float, int]:
        if key in self.factor.keys():
            return self.factor[key]
        else:
            raise KeyError(
                f"Ожидался один из: {list(self.factor.keys())}. " f"Получен: '{key}'"
            )

    def __str__(self) -> str:
        if self.exponent != 1:
            return f"{self.view}^{self.exponent}"
        else:
            return f"{self.view}"

    def for_str_units(self) -> str:
        if self.exponent not in (1, -1):
            exponent = str(self.exponent).translate(self.SUP)
            return f"{self.view}{exponent}"
        else:
            return f"{self.view}"

    @property
    def multiplier(self) -> Union[float, int]:
        multiplier = self.factor[self.view]
        return multiplier ** self.exponent

    def change_view(self, new: str) -> None:
        if new in self.factor.keys():
            self.view = new
        else:
            raise ValueError()


MassUnits = Unit(
    {
        "мг": 10 ** -6,
        "г": 10 ** -3,
        "кг": 1,
        "т": 10 ** 3,
        "тыс.т": 10 ** 6,
        "млн.т": 10 ** 9,
        "млрд.т": 10 ** 12,
    },
    "кг",
    "Mass",
)

VolumeUnits = Unit(
    {
        "мл": 10 ** -6,
        "л": 10 ** -3,
        "барр": 0.158987,
        "м3": 1,
        "тыс.м3": 10 ** 3,
        "млн.м3": 10 ** 6,
        "млрд.м3": 10 ** 9,
    },
    "м3",
    "Volume",
)

SquareUnits = Unit(
    {
        "м2": 1,
        "га": 10 ** 4,
    },
    "м2",
    "Square",
)

RubUnit = Unit(
    {
        "коп": 0.01,
        "руб": 1,
        "тыс.руб": 10 ** 3,
        "млн.руб": 10 ** 6,
        "млрд.руб": 10 ** 9,
        "трлн.руб": 10 ** 12,
    },
    "руб",
    "Rub",
)

USDUnit = Unit(
    {
        "cent": 0.01,
        "USD": 1,
        "тыс.USD": 10 ** 3,
        "млн.USD": 10 ** 6,
        "млрд.USD": 10 ** 9,
        "трлн.USD": 10 ** 12,
    },
    "USD",
    "USD",
)

PercentUnit = Unit(
    {
        "доли ед.": 1,
        "%": 0.01,
    },
    "доли ед.",
    "доли ед.",
)

OneUnit = Unit(
    {
        "единиц": 1,
    },
    "единиц",
    "единиц",
)

TimeUnit = Unit(
    {"год": 1, "месяц": 12},
    "год",
    "год",
)


def get_units(name: str) -> Unit:
    if name.lower() in ["mass"]:
        return deepcopy(MassUnits)
    elif name.lower() in ["volume"]:
        return deepcopy(VolumeUnits)
    elif name.upper() in ["RUB"]:
        return deepcopy(RubUnit)
    elif name.upper() in ["USD"]:
        return deepcopy(USDUnit)
    elif name.lower() in ["percent"]:
        return deepcopy(PercentUnit)
    elif name.lower() in ["square"]:
        return deepcopy(SquareUnits)
    else:
        raise KeyError()


class UnitStack:
    def __init__(self) -> None:
        self.__units: Dict[str, Unit] = dict()

    def __getitem__(self, item: int) -> Unit:
        return list(self.__units.values())[item]

    def __setitem__(self, key: int, value: Unit) -> None:
        keyword = list(self.__units.keys())[key]
        self.__units[keyword] = value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, UnitStack):
            return NotImplemented

        return self.keys() == other.keys()

    def __iter__(self) -> Iterator[Unit]:
        for unit in self.__units.values():
            yield unit

    def __str__(self) -> str:
        results = []
        for uid, unit in enumerate(self.__units.values()):
            if uid == 0:
                results.append(str(unit))
            else:
                if unit.exponent < 0:
                    results.append("/")
                else:
                    results.append("*")
                results.append(unit.for_str_units())

        return "".join(results)

    def keys(self) -> List[str]:
        return list(self.__units.keys())

    def values(self) -> List[Unit]:
        return deepcopy(list(self.__units.values()))

    def append(self, unit: Unit) -> None:
        if unit.name not in self.__units.keys():
            self.__units[unit.name] = unit
        else:
            pass

    def extend(self, unit_stack: UnitStack) -> None:
        for unit in unit_stack.values():
            self.append(unit)

    def remove(self, unit_name: str) -> None:
        if unit_name in self.__units.keys():
            self.__units.pop(unit_name)
        else:
            pass

    def mul(self, other: UnitStack) -> None:
        for unit in other.values():
            if unit.name in self.keys():
                if unit.ISU != "доли ед.":
                    self.__units[unit.name].exponent += unit.exponent
                    if self.__units[unit.name].exponent == 0:
                        self.remove(unit.name)
            else:
                if unit.ISU != "доли ед.":
                    new_unit = deepcopy(unit)
                    self.append(new_unit)

    def truediv(self, other: UnitStack) -> None:
        for unit in other.values():
            if unit.name in self.keys():
                if unit.ISU != "доли ед.":
                    self.__units[unit.name].exponent -= unit.exponent
                    if self.__units[unit.name].exponent == 0:
                        self.remove(unit.name)
            else:
                if unit.ISU != "доли ед.":
                    new_unit = deepcopy(unit)
                    new_unit.exponent = -new_unit.exponent
                    self.append(new_unit)

    @property
    def multiplier(self) -> Union[float, int]:
        multiplier = 1.0
        for name, unit in self.__units.items():
            multiplier *= unit.multiplier
        return multiplier

    @property
    def exponent(self) -> Union[float, int]:
        exponent = 1.0
        for name, unit in self.__units.items():
            exponent *= unit.exponent
        return exponent

    def it_is_addition(self, other: UnitStack) -> None:

        if list(other.keys()) != list(self.__units.keys()):
            raise ValueError
        if other.exponent != self.exponent:
            raise ValueError

    @property
    def is_percent(self) -> bool:
        return [PercentUnit] == list(self.__units.values())
