from __future__ import annotations

import numpy as np

from pathlib import Path
from copy import deepcopy
from typing import Dict, Union, List, Optional, Tuple

from Units.Variables import Parameter
from ReaderWriter.SheetNames import CAPEX
from ReaderWriter.Reader import ECOExcel, read_eco_excel
from Units.Convertor import to_million


class CAPEXTable:
    Rows: Dict[str, Dict[str, str]] = dict()
    Name = ""

    @classmethod
    def get_row_name(cls, param_name: str) -> str:
        return cls.Rows[param_name]["Row"]


class ProductionWellTable(CAPEXTable):
    Name = CAPEX.DrillProdWell
    Rows = {
        "OneObjectPrice": {
            "Sheet": CAPEX.Name,
            "Table": CAPEX.DrillProdWell,
            "Row": "СТОИМОСТЬ ОДНОГО ОБЪЕКТА",
        },
        "NumberOfObjects": {
            "Sheet": CAPEX.Name,
            "Table": CAPEX.DrillProdWell,
            "Row": "ЧИСЛО ВВЕДЕННЫХ ОБЪЕКТОВ",
        },
        "LifeTime": {
            "Sheet": CAPEX.Name,
            "Table": CAPEX.DrillProdWell,
            "Row": "СРОК СЛУЖБЫ",
        },
    }


class InjectionWellTable(CAPEXTable):
    Name = CAPEX.DrillInjeWell
    Rows = {
        "OneObjectPrice": {
            "Sheet": CAPEX.Name,
            "Table": CAPEX.DrillInjeWell,
            "Row": "СТОИМОСТЬ ОДНОГО ОБЪЕКТА",
        },
        "NumberOfObjects": {
            "Sheet": CAPEX.Name,
            "Table": CAPEX.DrillInjeWell,
            "Row": "ЧИСЛО ВВЕДЕННЫХ ОБЪЕКТОВ",
        },
        "LifeTime": {
            "Sheet": CAPEX.Name,
            "Table": CAPEX.DrillInjeWell,
            "Row": "СРОК СЛУЖБЫ",
        },
    }


class WellMechanizationTable(CAPEXTable):
    Name = CAPEX.WellMechanization
    Rows = {
        "OneObjectPrice": {
            "Sheet": CAPEX.Name,
            "Table": CAPEX.WellMechanization,
            "Row": "СТОИМОСТЬ ОДНОГО ОБЪЕКТА",
        },
        "NumberOfObjects": {
            "Sheet": CAPEX.Name,
            "Table": CAPEX.WellMechanization,
            "Row": "ЧИСЛО ВВЕДЕННЫХ ОБЪЕКТОВ",
        },
        "LifeTime": {
            "Sheet": CAPEX.Name,
            "Table": CAPEX.WellMechanization,
            "Row": "СРОК СЛУЖБЫ",
        },
    }


class OilTransportationTable(CAPEXTable):
    Name = CAPEX.OilTransportation
    Rows = {
        "OneObjectPrice": {
            "Sheet": CAPEX.Name,
            "Table": CAPEX.OilTransportation,
            "Row": "СТОИМОСТЬ ОДНОГО ОБЪЕКТА",
        },
        "NumberOfObjects": {
            "Sheet": CAPEX.Name,
            "Table": CAPEX.OilTransportation,
            "Row": "ЧИСЛО ВВЕДЕННЫХ ОБЪЕКТОВ",
        },
        "LifeTime": {
            "Sheet": CAPEX.Name,
            "Table": CAPEX.OilTransportation,
            "Row": "СРОК СЛУЖБЫ",
        },
    }


class BoosterPumpingTable(CAPEXTable):
    Name = CAPEX.BoosterPumping
    Rows = {
        "OneObjectPrice": {
            "Sheet": CAPEX.Name,
            "Table": CAPEX.BoosterPumping,
            "Row": "СТОИМОСТЬ ОДНОГО ОБЪЕКТА",
        },
        "NumberOfObjects": {
            "Sheet": CAPEX.Name,
            "Table": CAPEX.BoosterPumping,
            "Row": "ЧИСЛО ВВЕДЕННЫХ ОБЪЕКТОВ",
        },
        "LifeTime": {
            "Sheet": CAPEX.Name,
            "Table": CAPEX.BoosterPumping,
            "Row": "СРОК СЛУЖБЫ",
        },
    }


class PowerSupplyTable(CAPEXTable):
    Name = CAPEX.PowerSupply
    Rows = {
        "OneObjectPrice": {
            "Sheet": CAPEX.Name,
            "Table": CAPEX.PowerSupply,
            "Row": "СТОИМОСТЬ ОДНОГО ОБЪЕКТА",
        },
        "NumberOfObjects": {
            "Sheet": CAPEX.Name,
            "Table": CAPEX.PowerSupply,
            "Row": "ЧИСЛО ВВЕДЕННЫХ ОБЪЕКТОВ",
        },
        "LifeTime": {
            "Sheet": CAPEX.Name,
            "Table": CAPEX.PowerSupply,
            "Row": "СРОК СЛУЖБЫ",
        },
    }


class WaterSupplyTable(CAPEXTable):
    Name = CAPEX.WaterSupply
    Rows = {
        "OneObjectPrice": {
            "Sheet": CAPEX.Name,
            "Table": CAPEX.WaterSupply,
            "Row": "СТОИМОСТЬ ОДНОГО ОБЪЕКТА",
        },
        "NumberOfObjects": {
            "Sheet": CAPEX.Name,
            "Table": CAPEX.WaterSupply,
            "Row": "ЧИСЛО ВВЕДЕННЫХ ОБЪЕКТОВ",
        },
        "LifeTime": {
            "Sheet": CAPEX.Name,
            "Table": CAPEX.WaterSupply,
            "Row": "СРОК СЛУЖБЫ",
        },
    }


class RoadsTable(CAPEXTable):
    Name = CAPEX.Roads
    Rows = {
        "OneObjectPrice": {
            "Sheet": CAPEX.Name,
            "Table": CAPEX.Roads,
            "Row": "СТОИМОСТЬ ОДНОГО ОБЪЕКТА",
        },
        "NumberOfObjects": {
            "Sheet": CAPEX.Name,
            "Table": CAPEX.Roads,
            "Row": "ЧИСЛО ВВЕДЕННЫХ ОБЪЕКТОВ",
        },
        "LifeTime": {
            "Sheet": CAPEX.Name,
            "Table": CAPEX.Roads,
            "Row": "СРОК СЛУЖБЫ",
        },
    }


class RPSTable(CAPEXTable):
    Name = CAPEX.ReservoirPressureSupport
    Rows = {
        "OneObjectPrice": {
            "Sheet": CAPEX.Name,
            "Table": CAPEX.ReservoirPressureSupport,
            "Row": "СТОИМОСТЬ ОДНОГО ОБЪЕКТА",
        },
        "NumberOfObjects": {
            "Sheet": CAPEX.Name,
            "Table": CAPEX.ReservoirPressureSupport,
            "Row": "ЧИСЛО ВВЕДЕННЫХ ОБЪЕКТОВ",
        },
        "LifeTime": {
            "Sheet": CAPEX.Name,
            "Table": CAPEX.ReservoirPressureSupport,
            "Row": "СРОК СЛУЖБЫ",
        },
    }


class EcologyTable(CAPEXTable):
    Name = CAPEX.Ecology
    Rows = {
        "OneObjectRate": {
            "Sheet": CAPEX.Name,
            "Table": CAPEX.Ecology,
            "Row": "РАЗМЕР СТАВКИ В ДОЛЯХ",
        },
        "LifeTime": {
            "Sheet": CAPEX.Name,
            "Table": CAPEX.DrillProdWell,
            "Row": "СРОК СЛУЖБЫ",
        },
    }


class OtherTable(CAPEXTable):
    Name = CAPEX.Others
    Rows = {
        "OneObjectRate": {
            "Sheet": CAPEX.Name,
            "Table": CAPEX.Others,
            "Row": "РАЗМЕР СТАВКИ В ДОЛЯХ",
        },
        "LifeTime": {
            "Sheet": CAPEX.Name,
            "Table": CAPEX.DrillProdWell,
            "Row": "СРОК СЛУЖБЫ",
        },
    }


BaseCapexList: List[Union[CAPEXTable, EcologyTable, OtherTable]] = [
    ProductionWellTable(),
    InjectionWellTable(),
    WellMechanizationTable(),
    OilTransportationTable(),
    BoosterPumpingTable(),
    PowerSupplyTable(),
    WaterSupplyTable(),
    RoadsTable(),
    RPSTable(),
    EcologyTable(),
    OtherTable(),
]


class CostPoint:

    _OneObjectPrice = "Ставка"
    _NumberOfObjects = "Количество"
    _LifeTime = "Срок службы"
    _Investments = "Инвестиции"
    _Depreciation = "Амортизация"
    _ResidualValue = "Остаточная стоимость"
    _PriceOnTheBalance = "Цена объектов на балансе"
    _OnTheBalance = "Количество объектов на балансе"

    Sensitivity = [0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3]

    def __init__(
        self,
        name: str,
        one_object_price: Parameter,
        number_of_objects: Parameter,
        life_time: Parameter,
        multiplier: Union[float, int] = 1,
    ):
        self.Name = name
        self.OneObjectPrice = one_object_price
        self.NumberOfObjects = number_of_objects
        self.__LT = life_time
        self.LifeTime = float(life_time.value[0])
        self.CostMultiplier = multiplier

    def price_on_balance(self) -> Parameter:
        lt = int(np.ceil(self.LifeTime))
        on_balance = self.investments()
        new_values = on_balance.value
        for pid, point in enumerate(new_values):
            if pid >= len(new_values) - lt:
                break
            elif point != 0:
                new_values[pid + lt] -= point
            else:
                pass
        on_balance.value = new_values
        return on_balance.cumsum()

    def on_balance(self) -> Parameter:

        lt = int(np.ceil(self.LifeTime))
        new = deepcopy(self.NumberOfObjects)
        new_values = new.value
        for pid, point in enumerate(new_values):
            if pid >= len(new_values) - lt:
                break
            elif point != 0:
                new_values[pid + lt] -= point
            else:
                pass

        new = deepcopy(self.NumberOfObjects)
        new.value = new_values.cumsum()
        return new

    @to_million
    def investments(self) -> Parameter:
        return self.OneObjectPrice * self.NumberOfObjects * self.CostMultiplier

    @to_million
    def depreciation(self) -> Parameter:
        on_balance = self.price_on_balance()
        payments = on_balance / self.LifeTime
        return payments

    @to_million
    def residual_value(self) -> Parameter:
        investments = self.investments()
        depreciation = self.depreciation()
        flow = investments - depreciation
        return flow.cumsum()

    def risk_analysis(
        self, sensitivity: List[Union[float, int]] = None
    ) -> Dict[Union[float, int], CostPoint]:
        if not sensitivity:
            sensitivity = self.Sensitivity

        results = dict()

        for variant in sensitivity:
            new = deepcopy(self)
            new.CostMultiplier = variant
            results[variant] = new

        return results

    def report(self) -> Dict[str, Parameter]:
        results = dict()
        results[self._OneObjectPrice] = self.OneObjectPrice
        results[self._NumberOfObjects] = self.NumberOfObjects
        results[self._LifeTime] = self.__LT
        results[self._Investments] = self.investments()
        results[self._Depreciation] = self.depreciation()
        results[self._ResidualValue] = self.residual_value()
        results[self._PriceOnTheBalance] = self.price_on_balance()
        results[self._OnTheBalance] = self.on_balance()

        return results


class ProdWellCostPoint(CostPoint):
    pass


class InjWellCostPoint(CostPoint):
    pass


class EcologyCAPEX:

    _OneObjectPrice = "Ставка"
    _NumberOfObjects = "Количество"
    _LifeTime = "Срок службы"
    _Investments = "Инвестиции"
    _Depreciation = "Амортизация"
    _ResidualValue = "Остаточная стоимость"
    _PriceOnTheBalance = "Цена объектов на балансе"
    _OnTheBalance = "Количество объектов на балансе"

    Sensitivity = [0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3]

    def __init__(
        self,
        name: str,
        rate: Parameter,
        life_time: Parameter,
        multiplier: Union[float, int] = 1,
    ):
        self.Name = name
        self.Rate = rate
        self.__LT = life_time
        self.LifeTime = float(life_time.value[0])
        self.CostMultiplier = multiplier

    def price_on_balance(self, other_costs: Parameter) -> Parameter:
        lt = int(np.ceil(self.LifeTime))
        on_balance = self.investments(other_costs)
        new_values = on_balance.value
        for pid, point in enumerate(new_values):
            if pid >= len(new_values) - lt:
                break
            elif point != 0:
                new_values[pid + lt] -= point
            else:
                pass
        on_balance.value = new_values
        return on_balance.cumsum()

    def on_the_balance(self, other_costs: Parameter) -> Parameter:

        lt = int(np.ceil(self.LifeTime))
        new = deepcopy(other_costs)
        new_values = new.value
        for pid, point in enumerate(new_values):
            if pid >= len(new_values) - lt:
                break
            elif point != 0:
                new_values[pid + lt] -= point
            else:
                pass

        new = deepcopy(other_costs)
        new.value = new_values.cumsum()
        return new

    @to_million
    def investments(self, other_costs: Parameter) -> Parameter:
        return other_costs * self.Rate * self.CostMultiplier

    @to_million
    def depreciation(self, other_costs: Parameter) -> Parameter:
        on_balance = self.price_on_balance(other_costs)
        payments = on_balance / self.LifeTime
        return payments

    @to_million
    def residual_value(self, other_costs: Parameter) -> Parameter:
        investments = self.investments(other_costs)
        depreciation = self.depreciation(other_costs)
        flow = investments - depreciation
        return flow.cumsum()

    def risk_analysis(
        self, sensitivity: List[Union[float, int]] = None
    ) -> Dict[Union[float, int], Union[EcologyCAPEX, OtherCAPEX]]:
        if not sensitivity:
            sensitivity = self.Sensitivity

        results = dict()

        for variant in sensitivity:
            new = deepcopy(self)
            new.CostMultiplier = variant
            results[variant] = new

        return results

    def report(self, other_costs: Parameter) -> Dict[str, Parameter]:
        results = dict()
        results[self._OneObjectPrice] = other_costs
        results[self._NumberOfObjects] = self.Rate
        results[self._LifeTime] = self.__LT
        results[self._Investments] = self.investments(other_costs)
        results[self._Depreciation] = self.depreciation(other_costs)
        results[self._ResidualValue] = self.residual_value(other_costs)
        results[self._PriceOnTheBalance] = self.price_on_balance(other_costs)
        results[self._OnTheBalance] = self.on_the_balance(other_costs)

        return results


class OtherCAPEX(EcologyCAPEX):
    pass


class CAPEXPacket:
    Sensitivity = [0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3]

    def __init__(self, multiplier: Union[float, int] = 1):
        self.CostPoints: Dict[str, CostPoint] = dict()
        # self.ProdWell: Optional[ProdWellCostPoint] = None
        # self.InjWell: Optional[InjWellCostPoint] = None
        self.EcoCapex: Optional[EcologyCAPEX] = None
        self.Other: Optional[EcologyCAPEX] = None
        self.CostMultiplier = multiplier

    def __getitem__(self, key: str) -> CostPoint:
        return self.CostPoints[key]

    def __setitem__(self, key: str, value: CostPoint) -> None:
        self.CostPoints[key] = value

    def items(self) -> List[Tuple[str, Union[CostPoint, EcologyCAPEX]]]:
        results: List[Tuple[str, Union[CostPoint, EcologyCAPEX]]] = list()
        for key, value in self.CostPoints.items():
            results.append((key, value))

        if self.EcoCapex is not None:
            results.append((self.EcoCapex.Name, self.EcoCapex))

        if self.Other is not None:
            results.append((self.Other.Name, self.Other))

        return results

    def keys(self) -> Tuple[str, ...]:
        results = list()
        for key, value in self.CostPoints.items():
            results.append(key)

        if self.EcoCapex is not None:
            results.append(self.EcoCapex.Name)

        if self.Other is not None:
            results.append(self.Other.Name)

        return tuple(results)

    def append(self, value: CostPoint) -> None:
        self.CostPoints[value.Name] = value

    def extend(self, values: List[CostPoint]) -> None:
        for value in values:
            self.CostPoints[value.Name] = value

    def remove(self, key: str) -> None:
        self.CostPoints.pop(key)

    def __eco_base(self) -> Parameter:
        results = dict()
        for name_cp, cost_point in self.CostPoints.items():
            results[name_cp] = cost_point.investments()
        return sum(results.values())

    def __other_base(self) -> Parameter:
        results = dict()
        for name_cp, cost_point in self.CostPoints.items():
            results[name_cp] = cost_point.investments()

        if self.EcoCapex:
            eco_base = sum(results.values())
            results[self.EcoCapex.Name] = self.EcoCapex.investments(eco_base)

        return sum(results.values())

    def major_overhaul_base(self) -> Parameter:
        return self.investments().cumsum()

    def investments_by_items(self) -> Dict[str, Parameter]:
        results = dict()
        for name_cp, cost_point in self.CostPoints.items():
            results[name_cp] = cost_point.investments()

        if self.EcoCapex:
            eco_base = sum(results.values())
            results[self.EcoCapex.Name] = self.EcoCapex.investments(eco_base)

        if self.Other:
            other_base = sum(results.values())
            results[self.Other.Name] = self.Other.investments(other_base)

        return results

    def depreciation_by_items(self) -> Dict[str, Parameter]:
        results = dict()
        for name_cp, cost_point in self.CostPoints.items():
            results[name_cp] = cost_point.depreciation()

        if self.EcoCapex:
            eco_base = self.__eco_base()
            results[self.EcoCapex.Name] = self.EcoCapex.depreciation(eco_base)

        if self.Other:
            other_base = self.__other_base()
            results[self.Other.Name] = self.Other.depreciation(other_base)

        return results

    def residual_value_by_items(self) -> Dict[str, Parameter]:
        results = dict()
        for name_cp, cost_point in self.CostPoints.items():
            results[name_cp] = cost_point.residual_value()

        if self.EcoCapex:
            eco_base = self.__eco_base()
            results[self.EcoCapex.Name] = self.EcoCapex.residual_value(eco_base)

        if self.Other:
            other_base = self.__other_base()
            results[self.Other.Name] = self.Other.residual_value(other_base)

        return results

    @to_million
    def investments(self) -> Parameter:
        inv_by_item = self.investments_by_items()
        return sum(inv_by_item.values()) * self.CostMultiplier

    @to_million
    def depreciation(self) -> Parameter:
        dep_by_item = self.depreciation_by_items()
        return sum(dep_by_item.values()) * self.CostMultiplier

    @to_million
    def residual_value(self) -> Parameter:
        res_by_item = self.residual_value_by_items()
        return sum(res_by_item.values()) * self.CostMultiplier

    def risk_analysis(
        self,
        sensitivity: List[Union[int, float]] = None,
    ) -> Dict[Union[float, int], CAPEXPacket]:

        results = dict()

        if not sensitivity:
            sensitivity = self.Sensitivity

        for multi in sensitivity:
            new = deepcopy(self)
            new.CostMultiplier = multi
            results[multi] = new

        return results

    def risk_analysis_by_items(
        self,
        sensitivity: List[Union[int, float]] = None,
    ) -> Dict[str, Dict[Union[float, int], CAPEXPacket]]:

        results = dict()

        if not sensitivity:
            sensitivity = self.Sensitivity

        for name, point in self.CostPoints.items():
            point_results = dict()
            for mylti, var in point.risk_analysis(sensitivity).items():
                new = deepcopy(self)
                var.CostMultiplier = mylti
                new.CostPoints[name] = var
                point_results[mylti] = new
            results[name] = point_results

        if self.EcoCapex:
            point_results = dict()
            for mylti_ec, var_ec in self.EcoCapex.risk_analysis(sensitivity).items():
                new = deepcopy(self)
                var_ec.CostMultiplier = mylti_ec
                new.EcoCapex = var_ec
                point_results[mylti_ec] = new
            results[self.EcoCapex.Name] = point_results

        if self.Other:
            point_results = dict()
            for mylti_o, var_o in self.Other.risk_analysis(sensitivity).items():
                new = deepcopy(self)
                var_o.CostMultiplier = mylti_o
                new.Other = var_o
                point_results[mylti_o] = new
            results[self.Other.Name] = point_results

        return results

    def report(self) -> Dict[str, Dict[str, Parameter]]:
        results = dict()
        for name_cp, cost_point in self.CostPoints.items():
            results[name_cp] = cost_point.report()

        if self.EcoCapex:
            eco_base = self.__eco_base()
            results[self.EcoCapex.Name] = self.EcoCapex.report(eco_base)

        if self.Other:
            other_base = self.__other_base()
            results[self.Other.Name] = self.Other.report(other_base)

        return results


class CAPEXGenerator:
    OneObjectPrice = "OneObjectPrice"
    NumberOfObjects = "NumberOfObjects"
    LifeTime = "LifeTime"

    OneObjectRate = "OneObjectRate"

    @classmethod
    def get_cost_point(
        cls,
        eco_excel: ECOExcel,
        table: CAPEXTable,
    ) -> CostPoint:
        name = table.Name
        one_object_cost = eco_excel.get_param(table.Rows[cls.OneObjectPrice])
        number_of_object = eco_excel.get_param(
            table.Rows[cls.NumberOfObjects], fill_method="Zero"
        )
        life_time = eco_excel.get_param(table.Rows[cls.LifeTime])
        return CostPoint(name, one_object_cost, number_of_object, life_time)

    @classmethod
    def get_eco_capex(
        cls,
        eco_excel: ECOExcel,
        table: EcologyTable,
    ) -> EcologyCAPEX:
        name = table.Name
        one_object_rate = eco_excel.get_param(table.Rows[cls.OneObjectRate])
        life_time = eco_excel.get_param(table.Rows[cls.LifeTime])
        return EcologyCAPEX(name, one_object_rate, life_time)

    @classmethod
    def get_other_capex(
        cls,
        eco_excel: ECOExcel,
        table: OtherTable,
    ) -> OtherCAPEX:
        name = table.Name
        one_object_rate = eco_excel.get_param(table.Rows[cls.OneObjectRate])
        life_time = eco_excel.get_param(table.Rows[cls.LifeTime])
        return OtherCAPEX(name, one_object_rate, life_time)

    @classmethod
    def get_capex_packet(
        cls,
        eco_excel: ECOExcel,
        tables: List[
            Union[
                CAPEXTable,
                EcologyTable,
                OtherTable,
            ]
        ],
    ) -> CAPEXPacket:

        capex_packet = CAPEXPacket()

        for table in tables:
            # if type(table) == ProductionWellTable:
            #     prod_well = cls.get_cost_point(eco_excel, table)
            #     capex_packet.ProdWell = prod_well

            # elif type(table) == InjectionWellTable:
            #     inj_well = cls.get_cost_point(eco_excel, table)
            #     capex_packet.InjWell = inj_well

            if type(table) == EcologyTable:
                eco_capex = cls.get_eco_capex(eco_excel, table)
                capex_packet.EcoCapex = eco_capex

            elif type(table) == OtherTable:
                other_capex = cls.get_other_capex(eco_excel, table)
                capex_packet.Other = other_capex

            elif isinstance(table, CAPEXTable):
                cost_point = cls.get_cost_point(eco_excel, table)
                capex_packet.append(cost_point)

            else:
                raise KeyError

        return capex_packet


if __name__ == "__main__":
    link = Path(r"..\Проект_эффективность_нефть_шаблон_типовой.xls")
    ECO = read_eco_excel(link)
    CAPEXModel = CAPEXGenerator.get_capex_packet(ECO, BaseCapexList)
    Investment_by_item = CAPEXModel.investments_by_items()
    Depreciation_by_item = CAPEXModel.depreciation_by_items()
    ResidualValue_by_item = CAPEXModel.residual_value_by_items()
    Investment = CAPEXModel.investments()
    Depreciation = CAPEXModel.depreciation()
    ResidualValue = CAPEXModel.residual_value()

    pass
