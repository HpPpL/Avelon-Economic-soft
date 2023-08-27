from __future__ import annotations

import numpy as np

from typing import Dict, Union, List, Tuple, Optional
from pathlib import Path
from copy import deepcopy

from ReaderWriter.Reader import read_eco_excel, ECOExcel
from Units.Units import UnitStack, PercentUnit, RubUnit, TimeUnit
from Units.Variables import Parameter
from scipy.optimize import root

from Models.Production import ProdModel, ProdGenerator, ProdTable
from Models.Markets import MarketPacket, MarketGenerator, MarketsList
from Models.CAPEX import CAPEXPacket, CAPEXGenerator, BaseCapexList
from Models.OPEX import OPEXPacket, OPEXGenerator, OpexList
from Models.Tax import TaxPacket, TaxGenerator, TaxList
from Models.Credits import CreditsGenerator, CreditPortfolio


class EconomicModel:
    Sensitivity = [0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3]

    def __init__(
        self,
        discount_rate: Parameter,
        production: ProdModel,
        market: MarketPacket,
        capex: CAPEXPacket,
        opex: OPEXPacket,
        tax: TaxPacket,
        cred: CreditPortfolio,
    ) -> None:
        self.DiscountRate = discount_rate
        self.Production = production
        self.Market = market
        self.CAPEX = capex
        self.OPEX = opex
        self.Tax = tax
        self.Credits = cred

    def discount_coefficient(self) -> Parameter:
        year = np.arange(1, len(self.DiscountRate.value) + 1)
        dr = deepcopy(self.DiscountRate.value)
        if np.any(dr != -1):
            dc: np.ndarray = 1 / (1 + dr) ** year
        else:
            dr[dr == -1] = -0.999
            dc = 1 / (1 + dr) ** year
        results = Parameter(dc, deepcopy(PercentUnit))
        return results

    def money_flow(self, credit_accounting: bool = False) -> Parameter:
        benefits = self.Market.benefits(self.Production)
        investments = self.CAPEX.investments()
        expenses = self.OPEX.expenses(self.CAPEX)
        tax = self.Tax.payment(
            self.Production,
            self.CAPEX,
            self.OPEX,
            self.Market,
        )

        if credit_accounting:
            repayment = self.Credits.payment_of_interest()
            return benefits - investments - expenses - tax - repayment
        else:
            return benefits - investments - expenses - tax

    def discounted_money_flow(self, credit_accounting: bool = False) -> Parameter:
        money_flow = self.money_flow(credit_accounting)
        discount_coefficient = self.discount_coefficient()
        return money_flow * discount_coefficient

    def npv(self, credit_accounting: bool = False) -> Parameter:
        discounted_money_flow = self.discounted_money_flow(credit_accounting)
        npv = discounted_money_flow.cumsum()
        npv.value = npv.value[-1]
        return npv

    @staticmethod
    def payback_period(cum_flow: Parameter) -> Optional[Parameter]:

        for pid, value in enumerate(cum_flow.value[:-1]):
            if value < 0 < cum_flow.value[pid + 1]:
                x1 = pid + 1
                x2 = pid + 2
                y1 = value
                y2 = cum_flow.value[pid + 1]
                k = (y2 - y1) / (x2 - x1)
                b = y2 - k * x2
                results = Parameter(-b / k, TimeUnit)
                return results

        return None

    def real_payback_period(
        self, credit_accounting: bool = False
    ) -> Optional[Parameter]:
        return self.payback_period(self.money_flow(credit_accounting).cumsum())

    def discounted_payback_period(
        self, credit_accounting: bool = False
    ) -> Optional[Parameter]:
        return self.payback_period(
            self.discounted_money_flow(credit_accounting).cumsum()
        )

    def risk_analysis(
        self,
        sensitivity: List[Union[float, int]] = None,
    ) -> Dict[str, Dict[Union[float, int], Parameter]]:
        if sensitivity:
            sensitivity = self.Sensitivity

        results: Dict[str, Dict[Union[float, int], Parameter]] = dict()

        results["CAPEX"] = dict()
        capex_risks = self.CAPEX.risk_analysis(sensitivity).items()
        for multy, capex in capex_risks:
            capex_model = deepcopy(self)
            capex_model.CAPEX = capex
            results["CAPEX"][multy] = capex_model.npv()

        capex_risks = self.CAPEX.risk_analysis_by_items(sensitivity).items()
        for name, point in capex_risks:
            results[f"CAPEX: {name}"] = dict()
            for multy, capex in point.items():
                point_opex_model = deepcopy(self)
                point_opex_model.CAPEX = capex
                results[f"CAPEX: {name}"][multy] = point_opex_model.npv()

        results["OPEX"] = dict()
        opex_risks = self.OPEX.risk_analysis(sensitivity).items()
        for multy, opex in opex_risks:
            opex_model = deepcopy(self)
            opex_model.OPEX = opex
            results["OPEX"][multy] = opex_model.npv()

        opex_risks = self.OPEX.risk_analysis_by_items(sensitivity).items()
        for name, point in opex_risks:
            results[f"OPEX: {name}"] = dict()
            for multy, opex in point.items():
                point_opex_model = deepcopy(self)
                point_opex_model.OPEX = opex
                results[f"OPEX: {name}"][multy] = point_opex_model.npv()

        market_risks = self.Market.risk_analysis_by_items(sensitivity).items()
        for name, point in market_risks:
            results[f"Market: {name}"] = dict()
            for multy, market in point.items():
                market_model = deepcopy(self)
                market_model.Market = market
                results[f"Market: {name}"][multy] = market_model.npv()

        results["Production"] = dict()
        production_risks = self.Production.risk_analysis(sensitivity).items()
        for multy, production in production_risks:
            production_model = deepcopy(self)
            production_model.Production = production
            results["Production"][multy] = production_model.npv()

        return results

    def risk_analysis_for_report(
        self,
        sensitivity: List[Union[float, int]] = None,
    ) -> Tuple[List[int], List[str], Parameter]:
        if sensitivity is None:
            sensitivity = self.Sensitivity

        main_capex_risks = self.CAPEX.risk_analysis(sensitivity)
        capex_risks = self.CAPEX.risk_analysis_by_items(sensitivity)
        main_opex_risks = self.OPEX.risk_analysis(sensitivity)
        opex_risks = self.OPEX.risk_analysis_by_items(sensitivity)
        market_risks = self.Market.risk_analysis_by_items(sensitivity)
        production_risks = self.Production.risk_analysis(sensitivity)

        length = 1  # main_capex_risks
        length += len(capex_risks.items())
        length += 1  # main_opex_risks
        length += len(opex_risks.items())
        length += len(market_risks.items())
        length += 1  # production_risks

        value = np.zeros((length, len(sensitivity)))
        names = list()
        char_id = list()

        i, j = 0, 0
        names.append("CAPEX")
        char_id.append(1)
        for ind, (multy, capex) in enumerate(main_capex_risks.items()):
            capex_model = deepcopy(self)
            capex_model.CAPEX = capex
            value[i, j] = capex_model.npv().value
            j += 1

        for name, point in capex_risks.items():
            i, j = len(names), 0
            names.append(f"CAPEX: {name}")
            char_id.append(2)
            for multy, capex in point.items():
                point_opex_model = deepcopy(self)
                point_opex_model.CAPEX = capex
                value[i, j] = point_opex_model.npv().value
                j += 1

        i, j = len(names), 0
        names.append("OPEX")
        char_id.append(1)
        for multy, opex in main_opex_risks.items():
            opex_model = deepcopy(self)
            opex_model.OPEX = opex
            value[i, j] = opex_model.npv().value
            j += 1

        for name, point in opex_risks.items():
            i, j = len(names), 0
            names.append(f"OPEX: {name}")
            char_id.append(3)
            for multy, opex in point.items():
                point_opex_model = deepcopy(self)
                point_opex_model.OPEX = opex
                value[i, j] = point_opex_model.npv().value
                j += 1

        for name, point in market_risks.items():
            i, j = len(names), 0
            names.append(f"Market: {name}")
            char_id.append(1)
            for multy, market in point.items():
                market_model = deepcopy(self)
                market_model.Market = market
                value[i, j] = market_model.npv().value
                j += 1

        i, j = len(names), 0
        names.append("Production")
        char_id.append(1)
        for multy, production in production_risks.items():
            production_model = deepcopy(self)
            production_model.Production = production
            value[i, j] = production_model.npv().value
            j += 1

        us = UnitStack()
        rub = deepcopy(RubUnit)
        rub.change_view("млн.руб")
        us.append(rub)
        results = Parameter(value, us, true_mult=False)
        return char_id, names, results

    """
    def elasticity(
        self, sensitivity: List[Union[float, int]] = None
    ) -> Tuple[
        Dict[str, Dict[Union[float, int], Parameter]],
        Dict[str, Dict[Union[float, int], Parameter]],
        Dict[str, Dict[Union[float, int], Parameter]],
    ]:
        if not sensitivity:
            sensitivity = self.Sensitivity

        npv = self.risk_analysis(sensitivity)
        delta_npv = deepcopy(npv)
        elastic = deepcopy(npv)
        for name, parameter in delta_npv.items():
            if 1 in list(parameter.keys()):
                ind = 1
            else:
                ind = min(list(parameter.keys()))

            base = parameter[ind]
            for multy, npv_point in parameter.items():
                delta_npv[name][multy] = (npv[name][multy] - base) / base
                delta_npv[name][multy].units = UnitStack()
                pu = deepcopy(PercentUnit)
                pu.change_view("%")
                delta_npv[name][multy].units.append(pu)
                if multy != ind:
                    delta = delta_npv[name][multy]
                    elastic[name][multy] = delta / (multy - ind)
                    elastic[name][multy].units = UnitStack()
                    elastic[name][multy].units.append(PercentUnit)
                else:
                    v = delta_npv[name][multy]
                    v.value = 0
                    elastic[name][multy] = v
                    elastic[name][multy].units = UnitStack()
                    elastic[name][multy].units.append(PercentUnit)

        return npv, delta_npv, elastic
    """

    def elasticity(
        self, sensitivity: List[Union[float, int]] = None
    ) -> Tuple[List[int], List[str], Parameter, Parameter, Parameter]:
        if not sensitivity:
            sensitivity = self.Sensitivity

        char_id, names, npv = self.risk_analysis_for_report(sensitivity)

        base_value = np.vstack(npv.value[:, sensitivity.index(1)])
        base = Parameter(base_value, RubUnit, true_mult=False)
        delta_npv = (npv - base) / base
        delta_npv.value[:, sensitivity.index(1)] = 0
        new_u = deepcopy(PercentUnit)
        new_u.change_view("%")
        delta_npv.units = new_u

        denominator = np.array(sensitivity) - 1
        denominator[sensitivity.index(1)] = 1
        elastic = delta_npv / denominator
        new_u = deepcopy(PercentUnit)
        elastic.units = new_u
        return char_id, names, npv, delta_npv, elastic

    """
    def irr(self, credit_accounting: bool = False) -> Parameter:
        def get_npv(
            discount_rate: np.ndarray,
            em: EconomicModel,
            ca: bool = False
        ) -> Union[float, int, np.ndarray]:

            if type(em.DiscountRate.value) == np.ndarray:
                em.DiscountRate.value[:] = discount_rate[0]
            else:
                em.DiscountRate.value[:] = discount_rate[0]
            results: Union[float, int, np.ndarray] = em.npv(ca).value
            return results

        model = deepcopy(self)

        solution = root(
            get_npv,
            x0=np.array(model.DiscountRate.value[0]),
            args=(model, credit_accounting, ),
        )

        irr = deepcopy(model.DiscountRate)
        irr.value = solution.x

        return irr
    """

    def irr(self, credit_accounting: bool = False) -> Parameter:
        m_f = self.money_flow(credit_accounting)

        def get_npv(
            replacement: np.ndarray,
            mf: Parameter,
        ) -> Union[float, int, np.ndarray]:
            npv = mf * (1 + replacement) ** (len(mf.value) - np.arange(1, 21, 1))
            results: np.ndarray = np.sum(npv.value)
            return results

        model = deepcopy(self)

        solution = root(
            get_npv,
            x0=np.array([1]),
            args=(m_f,),
        )

        irr = deepcopy(model.DiscountRate)
        irr.value = solution.x

        return irr

    def return_on_capital_costs(self) -> Parameter:
        discount_coefficient = self.discount_coefficient()
        benefits = self.Market.benefits(self.Production)
        investments = self.CAPEX.investments()
        expenses = self.OPEX.expenses(self.CAPEX)
        tax = self.Tax.payment(
            self.Production,
            self.CAPEX,
            self.OPEX,
            self.Market,
        )
        numerator = benefits * discount_coefficient
        denominator = (investments + expenses + tax) * discount_coefficient
        return numerator.sum() / denominator.sum()

    def turnover_of_production_assets(self) -> Parameter:
        discount_coefficient = self.discount_coefficient()
        benefits = self.Market.benefits(self.Production)
        investments = self.CAPEX.investments()
        expenses = self.OPEX.expenses(self.CAPEX)
        tax = self.Tax.payment(
            self.Production,
            self.CAPEX,
            self.OPEX,
            self.Market,
        )
        numerator = (benefits - expenses - tax) * discount_coefficient
        denominator = investments * discount_coefficient
        return numerator.sum() / denominator.sum()

    def profitability_index(self, credit_accounting: bool = False) -> Parameter:
        pi = self.npv(credit_accounting) / self.CAPEX.investments().sum()
        pi.value += 1
        return pi


class EconomicModelGenerator:

    DiscountRateName = {
        "Sheet": "Фин",
        "Table": "NPV",
        "Row": "Норма дисконта",
    }

    @classmethod
    def get_discount_rate(
        cls,
        eco_table: ECOExcel,
    ) -> Parameter:
        sheet = cls.DiscountRateName["Sheet"]
        table = cls.DiscountRateName["Table"]
        row = cls.DiscountRateName["Row"]
        return eco_table.get(sheet, table, row)

    @classmethod
    def get(
        cls,
        link: Path,
        production_table: ProdTable,
        market_table: MarketsList,
        capex_table: BaseCapexList,
        opex_table: OpexList,
        tax_table: TaxList,
    ) -> EconomicModel:
        eco_table = read_eco_excel(link)

        results = EconomicModel(
            cls.get_discount_rate(eco_table),
            ProdGenerator.get_production(eco_table, production_table),
            MarketGenerator.get_market_packet(eco_table, market_table),
            CAPEXGenerator.get_capex_packet(eco_table, capex_table),
            OPEXGenerator.get_opex_packet(eco_table, opex_table),
            TaxGenerator.get_tax_packet(eco_table, tax_table),
            CreditsGenerator.get_credits(eco_table),
        )
        return results
