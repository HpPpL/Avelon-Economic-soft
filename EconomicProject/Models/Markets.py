from __future__ import annotations

from typing import Dict, Union, List, Any, Tuple
from ReaderWriter.Reader import Names, ECOExcel
from ReaderWriter.SheetNames import Benefits, Currency
from Units.Variables import Parameter
from copy import deepcopy
from pathlib import Path
from ReaderWriter.Reader import read_eco_excel
from Models.Production import ProdModel
from Units.Convertor import to_million


class MarketTable(Names):
    Sheet = Benefits.Name
    Name = ""

    Rows = {
        "Price": {
            "Sheet": Benefits.Name,
            "Table": Benefits.Inner,
            "Row": "БАЗОВАЯ ЦЕНА",
        },
        "Scalar": {
            "Sheet": Benefits.Name,
            "Table": Benefits.Inner,
            "Row": "БАЗОВЫЙ СКАЛЯР ВЫГОД",
        },
        "Share": {
            "Sheet": Benefits.Name,
            "Table": Benefits.Initial,
            "Row": "Скорректированная доля реализации на внутреннем рынке",
        },
    }


class InternalMarketTable:
    Table = Benefits.Inner
    Name = Table

    Rows = {
        "Price": {
            "Sheet": Benefits.Name,
            "Table": Benefits.Inner,
            "Row": "БАЗОВАЯ ЦЕНА",
        },
        "Scalar": {
            "Sheet": Benefits.Name,
            "Table": Benefits.Inner,
            "Row": "БАЗОВЫЙ СКАЛЯР ВЫГОД",
        },
        "Share": {
            "Sheet": Benefits.Name,
            "Table": Benefits.Initial,
            "Row": "Скорректированная доля реализации на внутреннем рынке",
        },
        "VAT": {
            "Sheet": Benefits.Name,
            "Table": Benefits.Inner,
            "Row": "Базовая ставка НДС",
        },
        "Transport": {
            "Sheet": Benefits.Name,
            "Table": Benefits.Inner,
            "Row": "Базовая стоимость транспорта до Транснефти",
        },
    }


class ExternalMarketTable:
    Table = Benefits.Outer
    Name = Table

    Rows = {
        "Price": {
            "Sheet": Benefits.Name,
            "Table": Benefits.Outer,
            "Row": "БАЗОВАЯ ЦЕНА",
        },
        "Scalar": {
            "Sheet": Benefits.Name,
            "Table": Benefits.Outer,
            "Row": "БАЗОВЫЙ СКАЛЯР ВЫГОД",
        },
        "Share": {
            "Sheet": Benefits.Name,
            "Table": Benefits.Initial,
            "Row": "Доля реализации на экспорт",
        },
        "ExportTaxRate": {
            "Sheet": Benefits.Name,
            "Table": Benefits.Outer,
            "Row": "Ставка экспортной пошлины",
        },
        "TransportBefore": {
            "Sheet": Benefits.Name,
            "Table": Benefits.Outer,
            "Row": "Базовая стоимость транспорта до Транснефти",
        },
        "TransportFor": {
            "Sheet": Benefits.Name,
            "Table": Benefits.Outer,
            "Row": "Базовая стоимость транспорта по Транснефти",
        },
        "CurrencyRate": {
            "Sheet": Currency.Name,
            "Table": Currency.USD,
            "Row": "БАЗОВЫЙ КУРС ( млн руб. за тыс. дол.)",
        },
    }


MarketsList: List[Union[MarketTable, InternalMarketTable, ExternalMarketTable,]] = [
    InternalMarketTable(),
    ExternalMarketTable(),
]


class BaseMarket:
    Sensitivity = [0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3]

    _Price = "Цена"
    _Share = "Доля"
    _Scalar = "Скаляр"
    _Benefits = "Выгоды"
    _CleanBenefits = "Чистые выгоды"

    def __init__(
        self,
        name: str,
        price: Parameter,
        share: Parameter,
        scalar: Parameter = None,
        currency_rate: Parameter = None,
        multi_benefits: Union[float, int] = 1,
        **kwargs: Any,
    ) -> None:
        self.Name = name
        self.Price = price
        self.Share = share
        self.Scalar = scalar
        self.currency = currency_rate
        self.multiplier = multi_benefits

    @to_million
    def benefits(self, data: ProdModel) -> Parameter:

        oil = data.oil_prod
        sold_oil = oil * self.Share
        money = sold_oil * self.Price

        if self.currency:
            money = money * self.currency

        if self.Scalar:
            money = money * self.Scalar

        return money * self.multiplier

    @to_million
    def clean_benefits(self, data: ProdModel) -> Parameter:
        return self.benefits(data)

    def risk_analysis(
        self,
        sensitivity: List[Union[float, int]] = None,
    ) -> Dict[Union[float, int], BaseMarket]:

        if not sensitivity:
            sensitivity = self.Sensitivity

        results = dict()

        for multi in sensitivity:
            new_model = deepcopy(self)
            new_model.multiplier = multi
            results[multi] = new_model

        return results

    def report(self, data: ProdModel) -> Dict[str, Parameter]:
        results = dict()
        results[self._Price] = self.Price
        results[self._Share] = self.Share
        results[self._Scalar] = self.Scalar
        results[self._Benefits] = self.benefits(data)
        results[self._CleanBenefits] = self.clean_benefits(data)
        return results


class InternalMarketModel(BaseMarket):
    Sensitivity = [0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3]

    _VATRate = "Ставка НДС"
    _VAT = "НДС"
    _TransportRate = "Удельные транспортные расходы"
    _Transport = "Транспортные расходы"

    def __init__(
        self,
        name: str,
        price: Parameter,
        share: Parameter,
        transport_rate: Parameter,
        vat: Parameter,
        scalar: Parameter = None,
        currency_rate: Parameter = None,
        multiplier: Union[float, int] = 1,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            name, price, share, scalar, currency_rate, multiplier, **kwargs
        )

        self.VAT = vat
        self.TransportRate = transport_rate

    @to_million
    def vat(self, data: ProdModel) -> Parameter:
        benefit = self.benefits(data)
        return benefit / (self.VAT + 1) * self.VAT

    @to_million
    def transport(self, data: ProdModel) -> Parameter:
        oil = data.oil_prod
        return oil * self.Share * self.TransportRate

    @to_million
    def clean_benefits(self, data: ProdModel) -> Parameter:

        ben = self.benefits(data)
        vat = self.vat(data)
        tra = self.transport(data)

        return ben - vat - tra

    def report(self, data: ProdModel) -> Dict[str, Parameter]:
        results = dict()
        results[self._Price] = self.Price
        results[self._Share] = self.Share
        results[self._Scalar] = self.Scalar
        results[self._VATRate] = self.VAT
        results[self._VAT] = self.vat(data)
        results[self._TransportRate] = self.TransportRate
        results[self._Transport] = self.transport(data)
        results[self._Benefits] = self.benefits(data)
        results[self._CleanBenefits] = self.clean_benefits(data)
        return results


class ExternalMarketModel(BaseMarket):

    _ExportTaxRate = "Ставка экспортной пошлины"
    _ExportTax = "Экпортная пошлина"
    _InnerTransportRate = "Удельные транспортные расходы на внутренних территориях"
    _InnerTransport = "Транспортные расходы на внутреннем рынке"
    _OuterTransportRate = "Удельные транспортные расходы на внешних территориях"
    _OuterTransport = "Транспортные расходы на внешней территории"

    def __init__(
        self,
        name: str,
        price: Parameter,
        share: Parameter,
        inner_transport_rate: Parameter,
        outer_transport_rate: Parameter,
        export_tax_rate: Parameter,
        currency_rate: Parameter,
        scalar: Parameter = None,
        multiplier: Union[float, int] = 1,
        **kwargs: Any,
    ) -> None:

        super().__init__(
            name, price, share, scalar, currency_rate, multiplier, **kwargs
        )
        self.InnerTransportRate = inner_transport_rate
        self.OuterTransportRate = outer_transport_rate
        self.ExportTaxRate = export_tax_rate

    @to_million
    def benefits(self, data: ProdModel) -> Parameter:

        oil = data.oil_prod
        density_oil = data.OilDensity
        volume_oil = oil / density_oil
        sold_oil = volume_oil * self.Share
        money = sold_oil * self.Price

        if self.currency:
            money = money * self.currency

        if self.Scalar:
            money = money * self.Scalar

        return money * self.multiplier

    @to_million
    def export_tax(self, data: ProdModel) -> Parameter:
        oil = data.oil_prod
        return oil * self.Share * self.ExportTaxRate

    @to_million
    def inner_transport_expenses(self, data: ProdModel) -> Parameter:
        oil = data.oil_prod
        return oil * self.Share * self.InnerTransportRate

    @to_million
    def outer_transport_expenses(self, data: ProdModel) -> Parameter:
        oil = data.oil_prod
        return oil * self.Share * self.OuterTransportRate

    @to_million
    def transport_expenses(self, data: ProdModel) -> Parameter:
        ite = self.inner_transport_expenses(data)
        ote = self.outer_transport_expenses(data)
        return ite + ote

    @to_million
    def clean_benefits(self, data: ProdModel) -> Parameter:
        benefits = self.benefits(data)
        export_tax = self.export_tax(data)
        transport = self.transport_expenses(data)
        return benefits - export_tax - transport

    def report(self, data: ProdModel) -> Dict[str, Parameter]:
        results = dict()
        results[self._Price] = self.Price
        results[self._Share] = self.Share
        results[self._Scalar] = self.Scalar
        results[self._ExportTaxRate] = self.ExportTaxRate
        results[self._ExportTax] = self.export_tax(data)
        results[self._InnerTransportRate] = self.InnerTransportRate
        results[self._InnerTransport] = self.inner_transport_expenses(data)
        results[self._OuterTransportRate] = self.OuterTransportRate
        results[self._OuterTransport] = self.outer_transport_expenses(data)
        results[self._Benefits] = self.benefits(data)
        results[self._CleanBenefits] = self.clean_benefits(data)
        return results


class MarketPacket:
    Sensitivity = [0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3]

    def __init__(self) -> None:
        self.Markets: Dict[str, BaseMarket] = dict()

    def __getitem__(self, key: str) -> BaseMarket:
        return self.Markets[key]

    def __setitem__(self, key: str, value: BaseMarket) -> None:
        self.Markets[key] = value

    def items(self) -> List[Tuple[str, BaseMarket]]:
        results = list()
        for key, value in self.Markets.items():
            results.append((key, value))

        return results

    def keys(self) -> Tuple[str, ...]:
        results = list()
        for key, value in self.Markets.items():
            results.append(key)

        return tuple(results)

    def append(self, value: BaseMarket) -> None:
        self.Markets[value.Name] = value

    def extend(self, values: List[BaseMarket]) -> None:
        for value in values:
            self.Markets[value.Name] = value

    def remove(self, key: str) -> None:
        self.Markets.pop(key)

    def benefits_by_items(
        self,
        production: ProdModel,
    ) -> Dict[str, Parameter]:
        results = dict()
        for name, market in self.Markets.items():
            results[name] = market.clean_benefits(production)
        return results

    def benefits(self, production: ProdModel) -> Parameter:
        return sum(self.benefits_by_items(production).values())

    def risk_analysis_by_items(
        self,
        sensitivity: List[Union[float, int]] = None,
    ) -> Dict[str, Dict[Union[float, int], MarketPacket]]:

        results = dict()

        if not sensitivity:
            sensitivity = self.Sensitivity

        for name, point in self.Markets.items():
            point_results = dict()
            for mylti, var in point.risk_analysis(sensitivity).items():
                new = deepcopy(self)
                var.multiplier = mylti
                new.Markets[name] = var
                point_results[mylti] = new
            results[name] = point_results

        return results

    def report(self, production: ProdModel) -> Dict[str, Dict[str, Parameter]]:
        results = dict()
        for name, point in self.Markets.items():
            results[name] = point.report(production)

        return results


class MarketGenerator:
    Sheet = "Sheet"
    Table = "Table"
    Row = "Row"

    Price = "Price"
    Share = "Share"
    Scalar = "Scalar"
    VAT = "VAT"
    InnerTransport = "Transport"
    BeforeTrans = "TransportBefore"
    ForTrans = "TransportFor"
    ExportTaxRate = "ExportTaxRate"
    CurrencyRate = "CurrencyRate"

    @classmethod
    def get_param(
        cls,
        eco_excel: ECOExcel,
        data: Dict[str, str],
        sheet_name: str = "ffill",
    ) -> Parameter:

        sheet = data[cls.Sheet]
        table = data[cls.Table]
        row = data[cls.Row]
        return eco_excel.get(sheet, table, row, sheet_name)

    @classmethod
    def get_base(cls, eco_excel: ECOExcel, table: MarketTable) -> BaseMarket:
        name = table.Name
        price = cls.get_param(eco_excel, table.Rows[cls.Price])
        share = cls.get_param(eco_excel, table.Rows[cls.Share])
        scalar = cls.get_param(eco_excel, table.Rows[cls.Scalar])

        return BaseMarket(name, price, share, scalar)

    @classmethod
    def get_inner(
        cls, eco_excel: ECOExcel, table: InternalMarketTable
    ) -> InternalMarketModel:
        name = table.Name
        price = cls.get_param(eco_excel, table.Rows[cls.Price])
        share = cls.get_param(eco_excel, table.Rows[cls.Share])
        scalar = cls.get_param(eco_excel, table.Rows[cls.Scalar])
        transport = cls.get_param(eco_excel, table.Rows[cls.InnerTransport])
        vat = cls.get_param(eco_excel, table.Rows[cls.VAT])
        return InternalMarketModel(name, price, share, transport, vat, scalar)

    @classmethod
    def get_outer(
        cls, eco_excel: ECOExcel, table: ExternalMarketTable
    ) -> ExternalMarketModel:
        name = table.Name
        price = cls.get_param(eco_excel, table.Rows[cls.Price])
        share = cls.get_param(eco_excel, table.Rows[cls.Share])
        scalar = cls.get_param(eco_excel, table.Rows[cls.Scalar])
        innertrans = cls.get_param(eco_excel, table.Rows[cls.BeforeTrans])
        outertrans = cls.get_param(eco_excel, table.Rows[cls.ForTrans])
        export_rate = cls.get_param(eco_excel, table.Rows[cls.ExportTaxRate])
        currency_rate = cls.get_param(eco_excel, table.Rows[cls.CurrencyRate])

        results = ExternalMarketModel(
            name,
            price,
            share,
            innertrans,
            outertrans,
            export_rate,
            currency_rate,
            scalar,
        )

        return results

    @classmethod
    def get_market(
        cls,
        eco_excel: ECOExcel,
        table: Union[MarketTable, InternalMarketTable, ExternalMarketTable],
    ) -> BaseMarket:
        if type(table) == MarketTable:
            return cls.get_base(eco_excel, table)
        elif type(table) == InternalMarketTable:
            return cls.get_inner(eco_excel, table)
        elif type(table) == ExternalMarketTable:
            return cls.get_outer(eco_excel, table)
        else:
            raise KeyError

    @classmethod
    def get_market_packet(
        cls,
        eco_excel: ECOExcel,
        tables: List[
            Union[
                MarketTable,
                InternalMarketTable,
                ExternalMarketTable,
            ],
        ],
    ) -> MarketPacket:
        pass

        markets = MarketPacket()
        for table in tables:
            model = cls.get_market(eco_excel, table)
            markets.append(model)

        return markets


if __name__ == "__main__":
    link = Path(r"..\Проект_эффективность_нефть_шаблон_типовой.xls")
    ECO = read_eco_excel(link)
    Market = MarketGenerator.get_market_packet(
        ECO, [ExternalMarketTable(), InternalMarketTable()]
    )
    pass
