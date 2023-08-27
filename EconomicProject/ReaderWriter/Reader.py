import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, Union, Type, List, Tuple, Optional, Any
from Units.ChooseUnits import define_unit
from Units.Units import UnitStack
from Units.Variables import Parameter

pd.options.mode.chained_assignment = None


class Names:
    Sheet: str = ""
    Table: str = ""
    row: str = ""
    Name = ""


class ECORow:
    def __init__(self, value: pd.Series, unit: str) -> None:
        self.value = value
        self.unit = unit

    def get_unit(self) -> UnitStack:
        return define_unit(self.unit)

    def get_value(self, fill_method: str = "ffill") -> Union[np.ndarray, float, int]:
        if fill_method == "Zero":
            value = self.value.fillna(0)
            results: np.ndarray = value.values
            return results
        elif fill_method == "first":
            one_results: Union[float, int] = self.value.iloc[0]
            return one_results
        else:
            value = self.value.fillna(method=fill_method)
            any_results: np.ndarray = value.values
            return any_results

    def get_parameter(self, fill_method: str = "ffill") -> Optional[Parameter]:
        try:
            value = self.get_value(fill_method)
            units = self.get_unit()
            return Parameter(value, units)
        except:
            return None


class ECOTable:
    def __init__(self) -> None:
        self.Rows: Dict[str, ECORow] = dict()

    def __getitem__(self, key: str) -> ECORow:
        return self.Rows[key]

    def __setitem__(self, key: str, value: ECORow) -> None:

        self.Rows[key] = value

    def keys(self) -> List[str]:
        return list(self.Rows.keys())

    def append(self, value: Dict[str, ECORow]) -> None:
        for key, item in value.items():
            self.Rows[key] = item

    def get(self, row_name: str) -> ECORow:
        return self.Rows[row_name]

    def get_value(self, row_name: str, number: int = None) -> Any:
        row = self.Rows[row_name]
        if number:
            return row.value[number]
        else:
            return row.value


class ECOSheet:
    def __init__(self) -> None:
        self.Tables: Dict[str, ECOTable] = dict()

    def __getitem__(self, key: str) -> ECOTable:
        return self.Tables[key]

    def __setitem__(self, key: str, value: ECOTable) -> None:
        self.Tables[key] = value

    def keys(self) -> List[str]:
        return list(self.Tables.keys())

    def append(self, value: Dict[str, ECOTable]) -> None:
        for key, item in value.items():
            self.Tables[key] = item


class ECOExcel:
    Sheet = "Sheet"
    Table = "Table"
    Row = "Row"

    def __init__(self) -> None:
        self.Sheets: Dict[str, ECOSheet] = dict()

    def __getitem__(self, key: str) -> ECOSheet:
        return self.Sheets[key]

    def __setitem__(self, key: str, value: ECOSheet) -> None:
        self.Sheets[key] = value

    def keys(self) -> List[str]:
        return list(self.Sheets.keys())

    def get(
        self,
        sheet_name: str,
        table_name: str,
        row_name: str,
        fill_method: str = "ffill",
    ) -> Optional[Parameter]:

        sheet = self.Sheets[sheet_name]
        table = sheet[table_name]
        row = table[row_name]
        return row.get_parameter(fill_method)

    def get_param(
        self,
        data: Dict[str, str],
        fill_method: str = "ffill",
    ) -> Parameter:
        sheet = data[self.Sheet]
        table = data[self.Table]
        row = data[self.Row]
        return self.get(sheet, table, row, fill_method)


def tables_standardization(df: pd.DataFrame, name: str) -> pd.DataFrame:
    new_df = df[df[0] == name]
    new_label = new_df[1].values
    new_label[0] = "Год"
    new_df = new_df.set_index(new_label)
    # new_df = new_df.fillna(method="ffill", axis=1)

    columnnumber = len(new_df.columns)
    labels = [0, 1, columnnumber - 2, columnnumber - 1]
    return new_df.drop(labels=labels, axis=1)


def create_sheet_table(df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    results = dict()
    df = df.dropna(axis=0, how="all")
    df.loc[:, 0] = df.loc[:, 0].fillna(method="ffill")
    uniq_name = pd.unique(df[0])
    for name in uniq_name:
        results[name] = tables_standardization(df, name)
    return results


def read_tables(
    link: Path, sheet_name: Union[str, List[str]] = None
) -> Dict[str, Dict[str, pd.DataFrame]]:
    results = dict()

    df = pd.read_excel(link, sheet_name=sheet_name, header=None)
    if type(df) == dict:
        for key in df:
            tables = create_sheet_table(df[key])
            results[key] = tables
        return results

    elif type(df) == pd.DataFrame:
        results[sheet_name] = create_sheet_table(df)
        return results

    else:
        raise TypeError()


def read_eco_excel(
    link: Path,
    sheet_names: Tuple[str, ...] = (
        "Фин",
        "Выгоды",
        "Затраты",
        "Капитал",
        "Налоги",
        "Валюта",
        "Долг",
    ),
) -> ECOExcel:

    edf = read_tables(link, list(sheet_names))
    eco_excel = ECOExcel()
    for sheet_name, tables in edf.items():
        # sheet_name = sheet_name.lower()
        if sheet_name not in eco_excel.keys():
            eco_excel[sheet_name] = ECOSheet()

        for table_name, table in tables.items():
            # table_name = table_name.lower()
            if table_name not in eco_excel[sheet_name].keys():
                eco_excel[sheet_name][table_name] = ECOTable()

            for (
                row_name,
                row,
            ) in list(table.iterrows()):
                if row_name in eco_excel[sheet_name][table_name].keys():
                    row_name = f"{row_name}(1)"

                raw_unit = row.iloc[0]
                raw_value = row.iloc[1:]
                eco_row = ECORow(raw_value, raw_unit)
                eco_excel[sheet_name][table_name].append({row_name: eco_row})

    return eco_excel


if __name__ == "__main__":
    Link = Path(
        r"C:\Users\ender\Desktop\Base\Работа\Gubka\ПО экономика\EconomicProject\Проект_эффективность_нефть_шаблон_типовой.xls"
    )
    ECO = read_eco_excel(Link)
    pass
