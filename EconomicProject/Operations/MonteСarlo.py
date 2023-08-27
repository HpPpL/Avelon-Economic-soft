from __future__ import annotations


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Union, Tuple, List, Dict, Optional, Tuple
    from pathlib import Path

from copy import deepcopy
from random import uniform

import numpy as np
import pandas as pd

from Models import NPV


class RawMonteCarloResults:
    def __init__(
        self,
        em: NPV.EconomicModel,
    ) -> None:
        self.Number = 0
        self.__init_capex_results(em)
        self.__init_opex_results(em)
        self.__init_market_results(em)
        self.Production: List[Union[float, int]] = []
        self.NPV: List[Union[float, int]] = list()

    def __init_capex_results(self, em: NPV.EconomicModel) -> None:
        self.CAPEX: Dict[str, List[Union[float, int]]] = dict()
        for key in em.CAPEX.keys():
            self.CAPEX[key] = []

    def __init_opex_results(self, em: NPV.EconomicModel) -> None:
        self.OPEX: Dict[str, List[Union[float, int]]] = dict()
        for key in em.OPEX.keys():
            self.OPEX[key] = []

    def __init_market_results(self, em: NPV.EconomicModel) -> None:
        self.Market: Dict[str, List[Union[float, int]]] = dict()
        for key in em.Market.keys():
            self.Market[key] = []

    def shape(self) -> tuple[int, int]:
        second_dimension = len(self.CAPEX.keys())
        second_dimension += len(self.OPEX.keys())
        second_dimension += len(self.Market.keys())
        second_dimension += 1  # Production
        return self.Number, second_dimension

    def to_dataframe(self) -> pd.DataFrame:
        main_head = ["CAPEX"] * len(self.CAPEX.keys())
        main_head.extend(["OPEX"] * len(self.OPEX.keys()))
        main_head.extend(["Market"] * len(self.Market.keys()))
        main_head.append("Production")

        bottom_head = list(self.CAPEX.keys())
        bottom_head.extend(self.OPEX.keys())
        bottom_head.extend(self.Market.keys())
        bottom_head.append("Oil")

        header = [main_head, bottom_head]

        results_value = np.zeros(self.shape())

        i = 0
        for key, value in self.CAPEX.items():
            results_value[:, i] = value
            i += 1

        for key, value in self.OPEX.items():
            results_value[:, i] = value
            i += 1

        for key, value in self.Market.items():
            results_value[:, i] = value
            i += 1

        results_value[:, i] = self.Production

        df = pd.DataFrame(
            results_value,
            columns=header,
            index=list(range(self.Number)),
        )

        df["NPV"] = self.NPV

        return df

    def to_monte_carlo_results(self) -> MonteCarloResults:
        df = self.to_dataframe()
        return MonteCarloResults(df)


class MonteCarloResults:
    def __init__(self, df: pd.DataFrame) -> None:
        self.__df = df

    def to_excel(self, link: Union[Path, str]) -> None:
        self.__df.to_excel(link)

    def sort(self) -> None:
        self.__df.sort_values(by="NPV", inplace=True)

    def npv(self) -> np.ndarray:
        results: np.ndarray = self.__df["NPV"].values
        return results

    def clustering(self, number=10) -> Tuple[Tuple[str, ...], np.ndarray]:
        npv = self.__df["NPV"].values

        point = np.linspace(min(npv), max(npv), number)
        results = []
        str_n = []

        for ind, i in enumerate(point[:-1]):
            if ind < len(point) - 2:
                pattern = np.where((npv >= i) & (npv < point[ind + 1]))
            else:
                pattern = np.where((npv >= i) & (npv <= point[ind + 1]))
            results.append(len(npv[pattern]))
            str_n.append(f"{round(i)}:{round(point[ind + 1])}")

        return tuple(str_n), np.array(results)


class MonteCarlo:
    Sensitivity = (-0.1, 0.1)

    def __init__(self) -> None:
        self.Sensitivity = self.Sensitivity

    def monte_carlo(
        self,
        em: NPV.EconomicModel,
        sensitivity: Union[
            Tuple[Union[float, int], ...],
            List[Union[float, int]],
        ] = None,
        number: int = 1000,
    ) -> MonteCarloResults:

        if sensitivity is None:
            sensitivity = self.Sensitivity

        sensitivity = (1 + sensitivity[0], 1 + sensitivity[1])

        em = deepcopy(em)

        results = RawMonteCarloResults(em)
        results.Number = number
        for i in range(number):

            for name, capex in em.CAPEX.items():
                multy = uniform(sensitivity[0], sensitivity[1])
                results.CAPEX[name].append(multy)
                capex.CostMultiplier = multy

            for name, opex in em.OPEX.items():
                multy = uniform(sensitivity[0], sensitivity[1])
                results.OPEX[name].append(multy)
                opex.CostMultiplier = multy

            for name, opex in em.Market.items():
                multy = uniform(sensitivity[0], sensitivity[1])
                results.Market[name].append(multy)
                opex.CostMultiplier = multy

            multy = uniform(sensitivity[0], sensitivity[1])
            results.Production.append(multy)
            em.Production.Multiplier = multy

            results.NPV.append(em.npv().get())

        return results.to_monte_carlo_results()
