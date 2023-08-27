from __future__ import annotations

from ReaderWriter.SheetNames import OPEX
from typing import Dict, Union, List, Optional, Tuple

from Units.Variables import Parameter
from copy import deepcopy
from pathlib import Path
from ReaderWriter.Reader import read_eco_excel, ECOExcel
from Models.CAPEX import CAPEXPacket


class OPEXTable:
    Rows: Dict[str, Dict[str, str]] = dict()
    Name = ""
    Link: Optional[str] = None


class ProdWellTable(OPEXTable):
    Name = OPEX.ProdWells
    Rows = {
        "Price": {
            "Sheet": OPEX.Name,
            "Table": OPEX.ProdWells,
            "Row": "БАЗОВАЯ ЦЕНА",
        },
        "Scalar": {
            "Sheet": OPEX.Name,
            "Table": OPEX.ProdWells,
            "Row": "БАЗОВЫЙ СКАЛЯР ЗАТРАТ",
        },
        "Number": {
            "Sheet": OPEX.Name,
            "Table": OPEX.ProdWells,
            "Row": "БАЗОВОЕ КОЛИЧЕСТВО",
        },
    }


class InjWellsTable(OPEXTable):
    Name = OPEX.InjWells
    Rows = {
        "Price": {
            "Sheet": OPEX.Name,
            "Table": OPEX.InjWells,
            "Row": "БАЗОВАЯ ЦЕНА",
        },
        "Scalar": {
            "Sheet": OPEX.Name,
            "Table": OPEX.InjWells,
            "Row": "БАЗОВЫЙ СКАЛЯР ЗАТРАТ",
        },
        "Number": {
            "Sheet": OPEX.Name,
            "Table": OPEX.InjWells,
            "Row": "БАЗОВОЕ КОЛИЧЕСТВО",
        },
    }


class PreparationOilTable(OPEXTable):
    Name = OPEX.OilPreparation
    Rows = {
        "Price": {
            "Sheet": OPEX.Name,
            "Table": OPEX.OilPreparation,
            "Row": "БАЗОВАЯ ЦЕНА",
        },
        "Scalar": {
            "Sheet": OPEX.Name,
            "Table": OPEX.OilPreparation,
            "Row": "БАЗОВЫЙ СКАЛЯР ЗАТРАТ",
        },
        "Number": {
            "Sheet": OPEX.Name,
            "Table": OPEX.OilPreparation,
            "Row": "БАЗОВОЕ КОЛИЧЕСТВО",
        },
    }


class CollectionOilTable(OPEXTable):
    Name = OPEX.CollectionOil
    Rows = {
        "Price": {
            "Sheet": OPEX.Name,
            "Table": OPEX.CollectionOil,
            "Row": "БАЗОВАЯ ЦЕНА",
        },
        "Scalar": {
            "Sheet": OPEX.Name,
            "Table": OPEX.CollectionOil,
            "Row": "БАЗОВЫЙ СКАЛЯР ЗАТРАТ",
        },
        "Number": {
            "Sheet": OPEX.Name,
            "Table": OPEX.CollectionOil,
            "Row": "БАЗОВОЕ КОЛИЧЕСТВО",
        },
    }


class WaterInjectionTable(OPEXTable):
    Name = OPEX.WaterInjection
    Rows = {
        "Price": {
            "Sheet": OPEX.Name,
            "Table": OPEX.WaterInjection,
            "Row": "БАЗОВАЯ ЦЕНА",
        },
        "Scalar": {
            "Sheet": OPEX.Name,
            "Table": OPEX.WaterInjection,
            "Row": "БАЗОВЫЙ СКАЛЯР ЗАТРАТ",
        },
        "Number": {
            "Sheet": OPEX.Name,
            "Table": OPEX.WaterInjection,
            "Row": "БАЗОВОЕ КОЛИЧЕСТВО",
        },
    }


class MechanizedOilTable(OPEXTable):
    Name = OPEX.MechanizedOil
    Rows = {
        "Price": {
            "Sheet": OPEX.Name,
            "Table": OPEX.MechanizedOil,
            "Row": "БАЗОВАЯ ЦЕНА",
        },
        "Scalar": {
            "Sheet": OPEX.Name,
            "Table": OPEX.MechanizedOil,
            "Row": "БАЗОВЫЙ СКАЛЯР ЗАТРАТ",
        },
        "Number": {
            "Sheet": OPEX.Name,
            "Table": OPEX.MechanizedOil,
            "Row": "БАЗОВОЕ КОЛИЧЕСТВО",
        },
    }


class WFRACKTable(OPEXTable):
    Name = OPEX.WFRACK
    Rows = {
        "Price": {
            "Sheet": OPEX.Name,
            "Table": OPEX.WFRACK,
            "Row": "БАЗОВАЯ ЦЕНА",
        },
        "Scalar": {
            "Sheet": OPEX.Name,
            "Table": OPEX.WFRACK,
            "Row": "БАЗОВЫЙ СКАЛЯР ЗАТРАТ",
        },
        "Number": {
            "Sheet": OPEX.Name,
            "Table": OPEX.WFRACK,
            "Row": "БАЗОВОЕ КОЛИЧЕСТВО",
        },
    }


class ReservoirIsolationTable(OPEXTable):
    Name = OPEX.ReservoirIsolation
    Rows = {
        "Price": {
            "Sheet": OPEX.Name,
            "Table": OPEX.ReservoirIsolation,
            "Row": "БАЗОВАЯ ЦЕНА",
        },
        "Scalar": {
            "Sheet": OPEX.Name,
            "Table": OPEX.ReservoirIsolation,
            "Row": "БАЗОВЫЙ СКАЛЯР ЗАТРАТ",
        },
        "Number": {
            "Sheet": OPEX.Name,
            "Table": OPEX.ReservoirIsolation,
            "Row": "БАЗОВОЕ КОЛИЧЕСТВО",
        },
    }


class MajorOverhaulTable(OPEXTable):
    Name = OPEX.MajorOverhaul
    Rows = {
        "Price": {
            "Sheet": OPEX.Name,
            "Table": OPEX.MajorOverhaul,
            "Row": "БАЗОВАЯ СТАВКА",
        },
        "Scalar": {
            "Sheet": OPEX.Name,
            "Table": OPEX.MajorOverhaul,
            "Row": "БАЗОВЫЙ СКАЛЯР ЗАТРАТ",
        },
        "Number": {
            "Sheet": OPEX.Name,
            "Table": OPEX.MajorOverhaul,
            "Row": "БАЗОВОЕ КОЛИЧЕСТВО",
        },
    }


class OtherTable(OPEXTable):
    Name = OPEX.Others
    Rows = {
        "Price": {
            "Sheet": OPEX.Name,
            "Table": OPEX.Others,
            "Row": "БАЗОВАЯ СТАВКА",
        },
        "Scalar": {
            "Sheet": OPEX.Name,
            "Table": OPEX.Others,
            "Row": "БАЗОВЫЙ СКАЛЯР ЗАТРАТ",
        },
    }


OpexList = [
    ProdWellTable(),
    InjWellsTable(),
    PreparationOilTable(),
    CollectionOilTable(),
    WaterInjectionTable(),
    MechanizedOilTable(),
    WFRACKTable(),
    ReservoirIsolationTable(),
    MajorOverhaulTable(),
    OtherTable(),
]


class CostPoint:
    Sensitivity = [0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3]

    _Price = "Ставка"
    _Base = "Количество"
    _Scalar = "Скаляр"
    _Multiplier = "Множитель"
    _Cost = "Затраты"

    def __init__(
        self,
        name: str,
        price: Parameter,
        scalar: Parameter,
        # number: Parameter,
        # link: str,
        multiplier: Union[float, int] = 1,
    ):
        self.Name = name
        self.Price = price
        self.Scalar = scalar
        # self.Number = number
        self.multiplier = multiplier

    def __get_param_multiplier(self) -> Parameter:
        new = deepcopy(self.Scalar)
        new.value[:] = self.multiplier
        return new

    def cost(self, base: Parameter) -> Parameter:
        return base * self.Price * self.Scalar * self.multiplier

    def risk_analysis(
        self,
        sensitivity: List[Union[float, int]] = None,
    ) -> Dict[Union[float, int], CostPoint]:
        if not sensitivity:
            sensitivity = self.Sensitivity

        results = dict()

        for variant in sensitivity:
            new = deepcopy(self)
            new.multiplier = variant
            results[variant] = new

        return results

    def report(self, base: Parameter) -> Dict[str, Parameter]:
        results = dict()
        results[self._Price] = self.Price
        results[self._Base] = base
        results[self._Scalar] = self.Scalar
        results[self._Multiplier] = self.__get_param_multiplier()
        results[self._Cost] = self.cost(base)
        return results


class BaseCostPoint:
    Sensitivity = [0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3]

    _Price = "Ставка"
    _Base = "Количество"
    _Scalar = "Скаляр"
    _Multiplier = "Множитель"
    _Cost = "Затраты"

    def __init__(
        self,
        name: str,
        price: Parameter,
        scalar: Parameter,
        number: Parameter,
        multiplier: Union[float, int] = 1,
    ):

        self.Name = name
        self.Price = price
        self.Scalar = scalar
        self.Number = number
        self.multiplier = multiplier

    def __get_param_multiplier(self) -> Parameter:
        new = deepcopy(self.Scalar)
        new.value[:] = self.multiplier
        return new

    def cost(self) -> Parameter:
        value = self.Number * self.Price * self.Scalar * self.multiplier
        value.units[0].change_view("млн.руб")
        return value

    def risk_analysis(
        self, sensitivity: List[Union[float, int]] = None
    ) -> Dict[Union[float, int], BaseCostPoint]:
        if not sensitivity:
            sensitivity = self.Sensitivity

        results = dict()

        for variant in sensitivity:
            new = deepcopy(self)
            new.multiplier = variant
            results[variant] = new

        return results

    def report(self) -> Dict[str, Parameter]:
        results = dict()
        results[self._Price] = self.Price
        results[self._Base] = self.Number
        results[self._Scalar] = self.Scalar
        results[self._Multiplier] = self.__get_param_multiplier()
        results[self._Cost] = self.cost()
        return results


class OPEXPacket:
    Sensitivity = [0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3]

    def __init__(self, multiplier: Union[float, int] = 1):
        self.CostPoints: Dict[str, BaseCostPoint] = dict()
        self.MajorOverhaul: Optional[CostPoint] = None
        self.Other: Optional[CostPoint] = None
        self.CostMultiplier = multiplier

    def __getitem__(self, key: str) -> Union[CostPoint, BaseCostPoint]:
        return self.CostPoints[key]

    def __setitem__(
        self,
        key: str,
        value: BaseCostPoint,
    ) -> None:
        self.CostPoints[key] = value

    def items(self) -> List[Tuple[str, Union[BaseCostPoint, CostPoint]]]:
        results: List[Tuple[str, Union[BaseCostPoint, CostPoint]]] = list()
        for key, value in self.CostPoints.items():
            results.append((key, value))

        if self.MajorOverhaul is not None:
            results.append((self.MajorOverhaul.Name, self.MajorOverhaul))

        if self.Other is not None:
            results.append((self.Other.Name, self.Other))

        return results

    def keys(self) -> Tuple[str, ...]:
        results = list()
        for key, value in self.CostPoints.items():
            results.append(key)

        if self.MajorOverhaul is not None:
            results.append(self.MajorOverhaul.Name)

        if self.Other is not None:
            results.append(self.Other.Name)

        return tuple(results)

    def append(self, value: BaseCostPoint) -> None:
        self.CostPoints[value.Name] = value

    def extend(self, values: List[BaseCostPoint]) -> None:
        for value in values:
            self.CostPoints[value.Name] = value

    def remove(self, key: str) -> None:
        self.CostPoints.pop(key)

    def __other_base(self, capex: CAPEXPacket) -> Parameter:
        results = dict()
        for name, point in self.CostPoints.items():
            results[name] = point.cost()

        if self.MajorOverhaul:
            mo_base = capex.major_overhaul_base()
            name = self.MajorOverhaul.Name
            results[name] = self.MajorOverhaul.cost(mo_base)

        return sum(results.values())

    def expenses_by_items(self, capex: CAPEXPacket) -> Dict[str, Parameter]:
        results = dict()
        for name, point in self.CostPoints.items():
            results[name] = point.cost()

        if self.MajorOverhaul:
            mo_base = capex.major_overhaul_base()
            name = self.MajorOverhaul.Name
            results[name] = self.MajorOverhaul.cost(mo_base)

        if self.Other:
            other_base = sum(results.values())
            name = self.Other.Name
            results[name] = self.Other.cost(other_base)

        return results

    def expenses(self, capex: CAPEXPacket) -> Parameter:
        return sum(self.expenses_by_items(capex).values()) * self.CostMultiplier

    def risk_analysis(
        self,
        sensitivity: List[Union[int, float]] = None,
    ) -> Dict[Union[float, int], OPEXPacket]:

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
    ) -> Dict[str, Dict[Union[float, int], OPEXPacket]]:

        results = dict()

        if not sensitivity:
            sensitivity = self.Sensitivity

        for name, point in self.CostPoints.items():
            point_results = dict()
            for mylti, var in point.risk_analysis(sensitivity).items():
                new = deepcopy(self)
                var.multiplier = mylti
                new.CostPoints[name] = var
                point_results[mylti] = new
            results[name] = point_results

        if self.MajorOverhaul:
            point_results = dict()
            for mylti_mo, var_mo in self.MajorOverhaul.risk_analysis(
                sensitivity
            ).items():
                new = deepcopy(self)
                var_mo.multiplier = mylti_mo
                new.MajorOverhaul = var_mo
                point_results[mylti_mo] = new
            results[self.MajorOverhaul.Name] = point_results

        if self.Other:
            point_results = dict()
            for mylti_o, var_o in self.Other.risk_analysis(sensitivity).items():
                new = deepcopy(self)
                var_o.multiplier = mylti_o
                new.Other = var_o
                point_results[mylti_o] = new
            results[self.Other.Name] = point_results

        return results

    def report(self, capex: CAPEXPacket) -> Dict[str, Dict[str, Parameter]]:
        results = dict()
        for name, point in self.CostPoints.items():
            results[name] = point.report()

        if self.MajorOverhaul:
            mo_base = capex.major_overhaul_base()
            name = self.MajorOverhaul.Name
            results[name] = self.MajorOverhaul.report(mo_base)

        if self.Other:
            other_base = self.__other_base(capex)
            name = self.Other.Name
            results[name] = self.Other.report(other_base)

        return results


class OPEXGenerator:
    Price = "Price"
    Scalar = "Scalar"
    Number = "Number"

    OneObjectRate = "OneObjectRate"

    @classmethod
    def get_base_cost_point(
        cls,
        eco_excel: ECOExcel,
        table: OPEXTable,
    ) -> BaseCostPoint:
        name = table.Name
        price = eco_excel.get_param(table.Rows[cls.Price])
        scalar = eco_excel.get_param(table.Rows[cls.Scalar])
        number = eco_excel.get_param(table.Rows[cls.Number])
        return BaseCostPoint(name, price, scalar, number)

    @classmethod
    def get_cost_point(
        cls,
        eco_excel: ECOExcel,
        table: OPEXTable,
    ) -> CostPoint:
        name = table.Name
        price = eco_excel.get_param(table.Rows[cls.Price])
        scalar = eco_excel.get_param(table.Rows[cls.Scalar])
        return CostPoint(name, price, scalar)

    @classmethod
    def get_opex_packet(
        cls,
        eco_excel: ECOExcel,
        tables: List[OPEXTable],
    ) -> OPEXPacket:

        packet = OPEXPacket()

        for table in tables:
            if type(table) == MajorOverhaulTable:
                major_overhaul = cls.get_cost_point(eco_excel, table)
                packet.MajorOverhaul = major_overhaul

            elif type(table) == OtherTable:
                other = cls.get_cost_point(eco_excel, table)
                packet.Other = other

            else:
                base_cost_point = cls.get_base_cost_point(eco_excel, table)
                packet.append(base_cost_point)

        return packet


if __name__ == "__main__":
    link = Path(r"..\Проект_эффективность_нефть_шаблон_типовой.xls")
    ECO = read_eco_excel(link)
    OpexModel = OPEXGenerator.get_opex_packet(ECO, OpexList)
    # r_by = OpexModel.expenses_by_items()
    # t = OpexModel.expenses()
    pass
