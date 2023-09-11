from __future__ import annotations

import os
import time

from pathlib import Path

import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

from ReaderWriter.Reporter import Reporter
from Models.Production import ProdTable
from Models.Markets import MarketsList
from Models.CAPEX import BaseCapexList
from Models.OPEX import OpexList
from Models.Tax import TaxList
from Models.NPV import EconomicModelGenerator
from Operations import MonteСarlo


def name_checker(file):
    if file[0] == 'E' and '.' in file:
        return file[1:file.index('.')].isdigit()
    return False


if __name__ == "__main__":
    dir_files = os.listdir()
    LOF = []
    for file in dir_files:
        if name_checker(file):
            LOF.append(file)
        else:
            pass

    for file in LOF:
        t = time.time()
        Link = Path(f"{file}")
        EM = EconomicModelGenerator.get(
            Link,
            ProdTable(),
            MarketsList,
            BaseCapexList,
            OpexList,
            TaxList,
        )

        reporter = Reporter()
        reporter.different_sheets_report(EM, f"Report_{file.split('.')[0]}.xlsx")

        print(f"Файл {file} был обработан, время выполнения: {round(time.time() - t, 2)}")
        pass
