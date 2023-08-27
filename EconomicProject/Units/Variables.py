from __future__ import annotations

import numpy as np
import pandas as pd

from typing import Union, Tuple
from Units.Units import Unit, UnitStack
from copy import deepcopy


class Parameter:
    def __init__(
        self,
        value: Union[float, int, np.ndarray],
        units: Union[Unit, UnitStack],
        true_mult: bool = True,
    ) -> None:
        units = deepcopy(units)
        if type(units) == Unit:
            unitstack = UnitStack()
            unitstack.append(units)
            self.units: UnitStack = unitstack
        else:
            self.units = units

        if true_mult:
            self.value: Union[float, int, np.ndarray] = value * self.units.multiplier
        else:
            self.value = value

    def __str__(self) -> str:
        return f"{self.value / self.units.multiplier}, {self.units}"

    def __add__(self, other: Union[Parameter, int, float]) -> Parameter:
        if type(other) == Parameter:
            self.units.it_is_addition(other.units)
            new_value = self.value + other.value
        elif type(other) == float:
            new_value = self.value + other
        elif type(other) == int:
            new_value = self.value + other
        else:
            raise TypeError

        new_units = deepcopy(self.units)

        return Parameter(new_value, new_units, true_mult=False)

    def __radd__(self, other: Union[Parameter, int, float]) -> Parameter:
        if type(other) == Parameter:
            self.units.it_is_addition(other.units)
            new_value = self.value + other.value
        elif type(other) == float:
            new_value = self.value + other
        elif type(other) == int:
            new_value = self.value + other
        else:
            raise TypeError

        new_units = deepcopy(self.units)

        return Parameter(new_value, new_units, true_mult=False)

    def __sub__(self, other: Union[Parameter, int, float]) -> Parameter:
        if type(other) == Parameter:
            self.units.it_is_addition(other.units)
            new_value = self.value - other.value
        elif type(other) == float:
            new_value = other - self.value
        elif type(other) == int:
            new_value = other - self.value
        else:
            raise TypeError

        new_units = deepcopy(self.units)

        return Parameter(new_value, new_units, true_mult=False)

    def __mul__(self, other: Union[Parameter, int, float, np.ndarray]) -> Parameter:
        if type(other) == Parameter:

            new_value = self.value * other.value
            new_units = deepcopy(self.units)
            new_units.mul(other.units)

        elif type(other) == float:
            new_value = self.value * other
            new_units = deepcopy(self.units)
        elif type(other) == int:
            new_value = self.value * other
            new_units = deepcopy(self.units)
        elif type(other) == np.ndarray:
            new_value = self.value * other
            new_units = deepcopy(self.units)

        else:
            raise TypeError

        return Parameter(new_value, new_units, true_mult=False)

    def __truediv__(self, other: Union[Parameter, int, float, np.ndarray]) -> Parameter:
        if type(other) == Parameter:

            new_value = self.value / other.value
            new_units = deepcopy(self.units)
            new_units.truediv(other.units)

        elif type(other) == float:
            new_value = self.value / other
            new_units = deepcopy(self.units)

        elif type(other) == int:
            new_value = self.value / other
            new_units = deepcopy(self.units)

        elif type(other) == np.ndarray:
            new_value = self.value / other
            new_units = deepcopy(self.units)

        else:
            raise TypeError

        return Parameter(new_value, new_units, true_mult=False)

    def get(self, it_work: bool = False) -> Union[float, int, np.ndarray]:
        if it_work:
            unit = self.units.values()[0]

            if type(self.value) == np.ndarray:
                max_value = max(self.value)
            else:
                max_value = self.value
            factor_values = list(unit.factor.values())
            delta = np.abs(max_value - np.array(factor_values))
            ind = list(delta).index(min(delta))
            key = list(unit.factor.items())[ind][0]
            unit.change_view(key)
            self.units[0] = unit

        results: Union[float, int, np.ndarray] = self.value / self.units.multiplier
        return results

    def cumsum(self) -> Parameter:
        s = pd.Series(self.value)
        new_value = s.cumsum().values
        new = deepcopy(self)
        new.value = new_value
        return new

    def sum(self) -> Parameter:
        if type(self.value) == np.ndarray:
            mew_val = sum(self.value)
        else:
            mew_val = self.value
        new = deepcopy(self)
        new.value = mew_val
        return new

    def shape(self) -> Tuple[int, ...]:
        if type(self.value) == np.ndarray:
            return self.value.shape
        else:
            return (1,)
