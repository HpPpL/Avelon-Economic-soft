import numpy as np

from typing import Dict, List, Union, Optional, Tuple
from copy import deepcopy
from pathlib import Path


from ReaderWriter.Reader import ECOExcel, read_eco_excel
from ReaderWriter.SheetNames import Tax
from Models.CAPEX import CAPEXPacket
from Models.Production import ProdModel
from Models.Markets import MarketPacket
from Models.OPEX import OPEXPacket
from Units.Variables import Parameter
from Units.Convertor import to_million


class TaxTable:
    Rows: Dict[str, Dict[str, str]] = dict()
    Name = ""


class PropertyTaxTable(TaxTable):
    Name = Tax.Property
    Rows = {
        "Rate": {
            "Sheet": Tax.Name,
            "Table": Tax.Property,
            "Row": "СТАВКА",
        },
    }


class MineralExtractionTable(TaxTable):
    Name = Tax.MineralExtraction
    Rows = {
        "Rate": {
            "Sheet": Tax.Name,
            "Table": Tax.MineralExtraction,
            "Row": "СТАВКА",
        },
        "PriceRatio": {
            "Sheet": Tax.Name,
            "Table": Tax.MineralExtraction,
            "Row": "Коэффициент цен (КЦ)",
        },
    }


class InsurancePremiumsTable(TaxTable):
    Name = Tax.InsurancePremiums
    Rows = {
        "Rate": {
            "Sheet": Tax.Name,
            "Table": Tax.InsurancePremiums,
            "Row": "СТАВКА",
        },
        "Base": {
            "Sheet": Tax.Name,
            "Table": Tax.InsurancePremiums,
            "Row": "БАЗА",
        },
    }


class InsuranceAccidentTable(TaxTable):
    Name = Tax.InsuranceAccident
    Rows = {
        "Rate": {
            "Sheet": Tax.Name,
            "Table": Tax.InsuranceAccident,
            "Row": "СТАВКА",
        },
        "Base": {
            "Sheet": Tax.Name,
            "Table": Tax.InsuranceAccident,
            "Row": "БАЗА",
        },
    }


class LandPaymentTable(TaxTable):
    Name = Tax.LandPayment
    Rows = {
        "Rate": {
            "Sheet": Tax.Name,
            "Table": Tax.LandPayment,
            "Row": "СТАВКА",
        },
        "Base": {
            "Sheet": Tax.Name,
            "Table": Tax.LandPayment,
            "Row": "БАЗА",
        },
    }


class IncomePaymentTable:
    Name = Tax.Income
    Link: Optional[str] = None
    Rows = {
        "Rate": {
            "Sheet": Tax.Name,
            "Table": Tax.Income,
            "Row": "СТАВКА",
        },
    }


TaxList: List[
    Union[
        TaxTable,
        IncomePaymentTable,
        MineralExtractionTable,
        PropertyTaxTable,
    ]
] = [
    PropertyTaxTable(),
    MineralExtractionTable(),
    InsurancePremiumsTable(),
    InsuranceAccidentTable(),
    LandPaymentTable(),
    IncomePaymentTable(),
]


class PropertyTax:
    _Base = "Налоговая база"
    _TaxRate = "Налоговая ставка"
    _Payment = "Налоговые платежи"

    def __init__(
        self,
        name: str,
        tax_rate: Parameter,
        multiplier: Union[float, int] = 1,
    ) -> None:
        self.Name: str = name
        self.TaxRate = tax_rate
        self.multiplier = multiplier

    def payment(self, capex_model: CAPEXPacket) -> Parameter:
        base = capex_model.residual_value()
        base.value = np.round(base.value, 2)
        return base * self.TaxRate * self.multiplier

    def report(self, capex_model: CAPEXPacket) -> Dict[str, Parameter]:
        results = dict()
        base = capex_model.residual_value()
        results[self._Base] = base
        results[self._TaxRate] = self.TaxRate
        results[self._Payment] = self.payment(capex_model)
        return results


class BaseTax:
    _Base = "Налоговая база"
    _TaxRate = "Налоговая ставка"
    _Payment = "Налоговые платежи"

    def __init__(
        self,
        name: str,
        base: Parameter,
        tax_rate: Parameter,
        multiplier: Union[float, int] = 1,
    ) -> None:
        self.Name: str = name
        self.Base = base
        self.TaxRate = tax_rate
        self.multiplier = multiplier

    @to_million
    def payment(self) -> Parameter:
        return self.Base * self.TaxRate * self.multiplier

    def report(self) -> Dict[str, Parameter]:
        results = dict()
        results[self._Base] = self.Base
        results[self._TaxRate] = self.TaxRate
        results[self._Payment] = self.payment()
        return results


class MineralExtractionTax:

    _Base = "Налоговая база"
    _TaxRate = "Налоговая ставка"
    _Payment = "Налоговые платежи"
    _PriceRatio = "Коэффициент цен (КЦ)"

    def __init__(
        self,
        name: str,
        tax_rate: Parameter,
        price_ratio: Parameter,
        multiplier: Union[float, int] = 1,
    ) -> None:
        self.Name: str = name
        self.TaxRate = tax_rate
        self.PriceRatio = price_ratio
        self.multiplier = multiplier

    @to_million
    def payment(self, production: ProdModel) -> Parameter:
        base = production.oil_prod
        return base * self.TaxRate * self.PriceRatio * self.multiplier

    def report(self, production: ProdModel) -> Dict[str, Parameter]:
        results = dict()
        base = production.oil_prod
        results[self._Base] = base
        results[self._TaxRate] = self.TaxRate
        results[self._PriceRatio] = self.PriceRatio
        results[self._Payment] = self.payment(production)
        return results


class IncomeTax:

    _Base = "Налоговая база"
    _TaxRate = "Налоговая ставка"
    _Payment = "Налоговые платежи"

    def __init__(
        self,
        name: str,
        tax_rate: Parameter,
        multiplier: Union[float, int] = 1,
    ) -> None:
        self.Name: str = name
        self.TaxRate = tax_rate
        self.multiplier = multiplier

    @staticmethod
    def get_tax_base(dirty_base: Parameter) -> Parameter:
        db = dirty_base.value
        db[db < 0] = 0
        new = deepcopy(dirty_base)
        new.value = db
        return new

    @to_million
    def payment(self, base: Parameter) -> Parameter:
        base = self.get_tax_base(base)
        return base * self.TaxRate * self.multiplier

    def report(self, base: Parameter) -> Dict[str, Parameter]:
        results = dict()
        results[self._Base] = base
        results[self._TaxRate] = self.TaxRate
        results[self._Payment] = self.payment(base)
        return results


class TaxPacket:
    def __init__(self, multiplier: Union[float, int] = 1):
        self.Taxes: Dict[str, Union[BaseTax]] = dict()
        self.PropertyTax: Optional[PropertyTax] = None
        self.ExtractionTax: Optional[MineralExtractionTax] = None
        self.Income: Optional[IncomeTax] = None
        self.CostMultiplier = multiplier

    def __getitem__(self, key: str) -> Union[BaseTax]:
        return self.Taxes[key]

    def __setitem__(
        self,
        key: str,
        value: Union[BaseTax],
    ) -> None:
        self.Taxes[key] = value

    def items(
        self,
    ) -> List[
        Tuple[
            str,
            Union[
                BaseTax,
                PropertyTax,
                MineralExtractionTax,
                IncomeTax,
            ],
        ]
    ]:
        results: List[
            Tuple[
                str,
                Union[
                    BaseTax,
                    PropertyTax,
                    MineralExtractionTax,
                    IncomeTax,
                ],
            ]
        ] = list()
        for key, value in self.Taxes.items():
            results.append((key, value))

        if self.PropertyTax is not None:
            results.append((self.PropertyTax.Name, self.PropertyTax))

        if self.ExtractionTax is not None:
            results.append((self.ExtractionTax.Name, self.ExtractionTax))

        if self.Income is not None:
            results.append((self.Income.Name, self.Income))

        return results

    def append(self, value: Union[BaseTax]) -> None:
        self.Taxes[value.Name] = value

    def extend(self, values: List[Union[BaseTax]]) -> None:
        for value in values:
            self.Taxes[value.Name] = value

    def remove(self, key: str) -> None:
        self.Taxes.pop(key)

    def income_tax_base(
        self,
        production: ProdModel,
        capex: CAPEXPacket,
        opex: OPEXPacket,
        market: MarketPacket,
    ) -> Parameter:
        results: Dict[str, Parameter] = dict()

        for tax_name, tax in self.Taxes.items():
            results[tax_name] = tax.payment()

        if self.ExtractionTax:
            name = self.ExtractionTax.Name
            results[name] = self.ExtractionTax.payment(production)

        if self.PropertyTax:
            results[self.PropertyTax.Name] = self.PropertyTax.payment(capex)

        benefits = market.benefits(production)

        depreciation = capex.depreciation()
        expenses = opex.expenses(capex)
        other_tax = sum(results.values())
        return benefits - depreciation - expenses - other_tax

    def payment_by_items(
        self,
        production: ProdModel,
        capex: CAPEXPacket,
        opex: OPEXPacket,
        market: MarketPacket,
    ) -> Dict[str, Parameter]:

        results: Dict[str, Parameter] = dict()

        for tax_name, tax in self.Taxes.items():
            results[tax_name] = tax.payment()

        if self.ExtractionTax:
            name = self.ExtractionTax.Name
            results[name] = self.ExtractionTax.payment(production)

        if self.PropertyTax:
            results[self.PropertyTax.Name] = self.PropertyTax.payment(capex)

        if self.Income:
            benefits = market.benefits(production)

            depreciation = capex.depreciation()
            expenses = opex.expenses(capex)
            other_tax = sum(results.values())
            income_base = benefits - depreciation - expenses - other_tax
            results[self.Income.Name] = self.Income.payment(income_base)

        return results

    def payment(
        self,
        production: ProdModel,
        capex: CAPEXPacket,
        opex: OPEXPacket,
        market: MarketPacket,
    ) -> Parameter:
        return sum(self.payment_by_items(production, capex, opex, market).values())

    def report(
        self,
        production: ProdModel,
        capex: CAPEXPacket,
        opex: OPEXPacket,
        market: MarketPacket,
    ) -> Dict[str, Dict[str, Parameter]]:
        results = dict()
        for name, point in self.Taxes.items():
            results[name] = point.report()

        if self.PropertyTax:
            name = self.PropertyTax.Name
            results[name] = self.PropertyTax.report(capex)

        if self.ExtractionTax:
            name = self.ExtractionTax.Name
            results[name] = self.ExtractionTax.report(production)

        if self.Income:
            income_base = self.income_tax_base(production, capex, opex, market)
            results[self.Income.Name] = self.Income.report(income_base)

        return results


class TaxGenerator:
    Rate = "Rate"
    Base = "Base"
    PriceRatio = "PriceRatio"

    @classmethod
    def get_base_tax(
        cls,
        eco_excel: ECOExcel,
        table: TaxTable,
    ) -> BaseTax:
        name = table.Name
        rate = eco_excel.get_param(table.Rows[cls.Rate])
        base = eco_excel.get_param(table.Rows[cls.Base])
        return BaseTax(name, base, rate)

    @classmethod
    def get_mineral_tax(
        cls,
        eco_excel: ECOExcel,
        table: MineralExtractionTable,
    ) -> MineralExtractionTax:
        name = table.Name
        rate = eco_excel.get_param(table.Rows[cls.Rate])
        price_ratio = eco_excel.get_param(table.Rows[cls.PriceRatio])
        return MineralExtractionTax(name, rate, price_ratio)

    @classmethod
    def get_income_tax(
        cls,
        eco_excel: ECOExcel,
        table: IncomePaymentTable,
    ) -> IncomeTax:
        name = table.Name
        rate = eco_excel.get_param(table.Rows[cls.Rate])
        return IncomeTax(name, rate)

    @classmethod
    def get_property_tax(
        cls,
        eco_excel: ECOExcel,
        table: PropertyTaxTable,
    ) -> PropertyTax:
        name = table.Name
        rate = eco_excel.get_param(table.Rows[cls.Rate])
        return PropertyTax(name, rate)

    @classmethod
    def get_tax_packet(
        cls,
        eco_excel: ECOExcel,
        tables: List[
            Union[
                TaxTable,
                IncomePaymentTable,
                MineralExtractionTable,
                PropertyTaxTable,
            ]
        ],
    ) -> TaxPacket:

        packet = TaxPacket()

        for table in tables:
            if type(table) == IncomePaymentTable:
                income = cls.get_income_tax(eco_excel, table)
                packet.Income = income

            elif type(table) == MineralExtractionTable:
                mineral = cls.get_mineral_tax(eco_excel, table)
                packet.ExtractionTax = mineral

            elif type(table) == PropertyTaxTable:
                prop = cls.get_property_tax(eco_excel, table)
                packet.PropertyTax = prop

            elif isinstance(table, TaxTable):
                base = cls.get_base_tax(eco_excel, table)
                packet.append(base)
            else:
                raise KeyError

        return packet


if __name__ == "__main__":
    link = Path(r"..\Проект_эффективность_нефть_шаблон_типовой.xls")
    ECO = read_eco_excel(link)
    OpexModel = TaxGenerator.get_tax_packet(ECO, TaxList)
    pass
