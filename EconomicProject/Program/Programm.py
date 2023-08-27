from __future__ import annotations

import time

from pathlib import Path

from ReaderWriter.Reporter import Reporter
from Models.Production import ProdTable
from Models.Markets import MarketsList
from Models.CAPEX import BaseCapexList
from Models.OPEX import OpexList
from Models.Tax import TaxList
from Models.NPV import EconomicModelGenerator
from Operations import MonteСarlo


if __name__ == "__main__":
    t = time.time()
    Link = Path(r"Pattern.xls")
    EM = EconomicModelGenerator.get(
        Link,
        ProdTable(),
        MarketsList,
        BaseCapexList,
        OpexList,
        TaxList,
    )

    MoneyFlow = EM.money_flow()
    DiscountMoneyFlow = EM.discounted_money_flow()
    NPV = EM.npv()
    time1 = EM.real_payback_period()
    time2 = EM.discounted_payback_period()
    EM.elasticity()
    ERR = EM.irr()
    wi1 = EM.return_on_capital_costs()
    wi2 = EM.turnover_of_production_assets()
    # Только следующие две строки были незакоментированы
    reporter = Reporter()
    reporter.different_sheets_report(EM)
    MC = MonteСarlo.MonteCarlo()
    MSres = MC.monte_carlo(EM, (-0.1, 0.1), number=10000)
    MSres.sort()
    MSres.to_excel("res.xlsx")
    print(time.time() - t)
    pass
