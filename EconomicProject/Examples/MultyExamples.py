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
    LOF = ('E1', 'E2', 'E3', 'E4', 'E5')
    for file in LOF:
        t = time.time()
        Link = Path(f"{file}.xls")
        EM = EconomicModelGenerator.get(
            Link,
            ProdTable(),
            MarketsList,
            BaseCapexList,
            OpexList,
            TaxList,
        )

        reporter = Reporter()
        reporter.different_sheets_report(EM, f"Report_{file}.xlsx")

        print(f"Файл {file} был обработан, время выполнения: {time.time() - t}")
        pass
