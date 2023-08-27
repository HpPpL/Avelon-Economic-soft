from __future__ import annotations

from typing import Dict, Union, List
from ReaderWriter.SheetNames import Benefits
from ReaderWriter.Reader import ECOExcel
from Units.Variables import Parameter
from copy import deepcopy


class ProdTable:
    Name = Benefits.Initial

    Rows = {
        "Oil": {
            "Sheet": Benefits.Name,
            "Table": Benefits.Initial,
            "Row": "Базовая добыча нефти",
        },
        "OilDensity": {
            "Sheet": Benefits.Name,
            "Table": Benefits.Initial,
            "Row": "Плотность нефти",
        },
        "Scalar": {
            "Sheet": Benefits.Name,
            "Table": Benefits.Initial,
            "Row": "СКАЛЯР ДОБЫЧИ",
        },
    }


class ProdModel:
    Sensitivity = [0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3]

    _BaseOil = "Базовая добыча нефти"
    _Scalar = "Скаляр"
    _Oil = "Добыча нефти"
    _OilDensity = "Плотность"

    def __init__(
        self,
        name: str,
        oil: Parameter,
        # liquid: Parameter,
        # water: Parameter,
        oil_density: Parameter,
        # water_density: Parameter,
        scalar: Parameter,
        multi_oil: Union[float, int] = 1,
        # multi_liquid: Union[float, int] = 1,
        # multi_water: Union[float, int] = 1,
    ) -> None:
        self.Name = name
        self.Oil = oil
        # self.liquid = liquid
        # self.water = water
        self.OilDensity = oil_density
        # self.water_density = water_density
        self.Scalar = scalar
        self.Multiplier = multi_oil
        # self.multi_liquid = multi_liquid
        # self.multi_water = multi_water

    @property
    def oil_prod(self) -> Parameter:
        return self.Oil * self.Multiplier * self.Scalar

    """
    @property
    def liq_prod(self) -> Parameter:
        return self.liquid * self. multi_liquid
    
    @property
    def water_prod(self) -> Parameter:
        return self.liquid * self.multi_liquid
    """

    def risk_analysis(
        self,
        sensitivity: List[Union[float, int]] = None,
    ) -> Dict[Union[float, int], ProdModel]:

        if not sensitivity:
            sensitivity = self.Sensitivity

        results = dict()

        for multi in sensitivity:
            new = deepcopy(self)
            new.Multiplier = multi
            results[multi] = new

        return results

    def report(self) -> Dict[str, Parameter]:
        results = dict()
        results[self._BaseOil] = self.Oil
        results[self._Scalar] = self.Scalar
        results[self._OilDensity] = self.OilDensity
        results[self._Oil] = self.oil_prod
        return results


class ProdGenerator:
    Oil = "Oil"
    OilDensity = "OilDensity"
    Scalar = "Scalar"

    @classmethod
    def get_production(cls, eco_excel: ECOExcel, table: ProdTable) -> ProdModel:
        name = table.Name
        oil = eco_excel.get_param(table.Rows[cls.Oil])
        oil_density = eco_excel.get_param(table.Rows[cls.OilDensity])
        scalar = eco_excel.get_param(table.Rows[cls.Scalar])
        return ProdModel(name, oil, oil_density, scalar)
