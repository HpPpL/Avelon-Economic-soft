from __future__ import annotations

import numpy as np
import xlsxwriter as xlsw

from xlsxwriter import Workbook
from xlsxwriter.workbook import Worksheet
from typing import Dict, List
from copy import deepcopy

from Units.Variables import Parameter
from Models.NPV import EconomicModel
from Operations.MonteСarlo import MonteCarlo


class Reporter:
    BenefitsNPVName = "Выгоды"
    InvestmentsNPVName = "Инвестиции"
    ExpensesNPVName = "Затраты"
    TaxNPVName = "Налоги"
    CreditsRepaymentNPVName = "Платежи по процентам"
    MoneyFlowNPVName = "Денежный поток"
    CumulativeMoneyFlowNPVName = "Накопленный денежный поток"
    discount_coefficientNPVName = "Коэффициент дисконтирования"
    DiscountedMoneyFlowNPVName = "Дисконтированный денежный поток"
    CumDiscMoneyFlowNPVName = "Накопленный дисконтированный денежный поток"

    def __init__(self) -> None:
        self.NameBook = "Report"
        self.BookFormat = "xlsx"
        self.number_format = None
        self.TableNameFormatDict = {
            "rotation": 90,
            "text_wrap": True,
            "align": "center",
            "valign": "vcenter",
            "border": 1,
        }
        self.FloatNumbers = {
            "num_format": "0.00",
            "border": 1,
            "align": "center",
            "valign": "vcenter",
        }
        self.IntNumbers = {
            "num_format": "0",
            "border": 1,
            "align": "center",
            "valign": "vcenter",
        }

        self.TitleFormatDict = {
            "border": 1,
            "align": "left",
            "valign": "vcenter",
        }

        self.UnitFormatDict = {
            "border": 1,
            "align": "center",
            "valign": "vcenter",
            "text_wrap": True,
        }

    def __book_name(self) -> str:
        return f"{self.NameBook}.{self.BookFormat}"

    def __write_table(
        self,
        book: Workbook,
        sheet: Worksheet,
        i: int,
        table: Dict[str, Parameter],
        table_name: str,
    ) -> int:

        tablename_format = book.add_format(self.TableNameFormatDict)
        float_format = book.add_format(self.FloatNumbers)
        int_format = book.add_format(self.IntNumbers)
        title_format = book.add_format(self.TitleFormatDict)
        unit_format = book.add_format(self.UnitFormatDict)

        len_time = len(list(table.values())[0].get())
        sheet.write_row(i, 3, np.arange(1, len_time + 1), int_format)
        i += 1

        number = i + len(table.keys())
        sheet.merge_range(i - 1, 0, number - 1, 0, table_name, tablename_format)

        sheet.merge_range(i - 1, 1, i - 1, 2, "Год", title_format)

        for row_name, row in table.items():
            sheet.write(i, 1, row_name, title_format)
            sheet.write(i, 2, str(row.units), unit_format)
            sheet.write_row(i, 3, row.get(), float_format)
            i += 1
        return i

    def __capex_report(
        self,
        book: Workbook,
        sheet: Worksheet,
        i: int,
        em: EconomicModel,
    ) -> int:
        for table_name, table in em.CAPEX.report().items():
            i = self.__write_table(book, sheet, i, table, table_name)
            i += 1
        return i

    def opex_report(
        self,
        book: Workbook,
        sheet: Worksheet,
        i: int,
        em: EconomicModel,
    ) -> int:
        for table_name, table in em.OPEX.report(em.CAPEX).items():
            i = self.__write_table(book, sheet, i, table, table_name)
            i += 1
        return i

    def tax_report(
        self,
        book: Workbook,
        sheet: Worksheet,
        i: int,
        em: EconomicModel,
    ) -> int:
        tax_report = em.Tax.report(
            em.Production,
            em.CAPEX,
            em.OPEX,
            em.Market,
        ).items()

        for table_name, table in tax_report:
            i = self.__write_table(book, sheet, i, table, table_name)
            i += 1
        return i

    def market_report(
        self,
        book: Workbook,
        sheet: Worksheet,
        i: int,
        em: EconomicModel,
    ) -> int:
        for table_name, table in em.Market.report(em.Production).items():
            i = self.__write_table(book, sheet, i, table, table_name)
            i += 1
        return i

    def production_report(
        self,
        book: Workbook,
        sheet: Worksheet,
        i: int,
        em: EconomicModel,
    ) -> int:
        table = em.Production.report()
        table_name = "Production"
        i = self.__write_table(book, sheet, i, table, table_name)
        i += 1
        return i

    def npv_table(
        self,
        book: Workbook,
        sheet: Worksheet,
        i: int,
        em: EconomicModel,
        credit_accounting: bool = False,
    ) -> int:

        benefits = em.Market.benefits(em.Production)
        investments = em.CAPEX.investments()
        expenses = em.OPEX.expenses(em.CAPEX)
        tax = em.Tax.payment(
            em.Production,
            em.CAPEX,
            em.OPEX,
            em.Market,
        )
        repayment = em.Credits.payment_of_interest()
        # 'd_coef': em.discount_coefficient()
        money_flow = em.money_flow(credit_accounting)
        cumulative_money_flow = money_flow.cumsum()
        discounted_money_flow = em.discounted_money_flow(credit_accounting)
        cum_disc_money_flow = discounted_money_flow.cumsum()

        benefits.units[0].change_view("млрд.руб")
        investments.units[0].change_view("млрд.руб")
        expenses.units[0].change_view("млрд.руб")
        tax.units[0].change_view("млрд.руб")

        money_flow.units[0].change_view("млрд.руб")
        cumulative_money_flow.units[0].change_view("млрд.руб")
        discounted_money_flow.units[0].change_view("млрд.руб")
        cum_disc_money_flow.units[0].change_view("млрд.руб")

        if repayment is not None:
            repayment.units[0].change_view("млрд.руб")

        table = {
            self.BenefitsNPVName: benefits,
            self.InvestmentsNPVName: investments,
            self.ExpensesNPVName: expenses,
            self.TaxNPVName: tax,
            self.MoneyFlowNPVName: money_flow,
            self.CumulativeMoneyFlowNPVName: cumulative_money_flow,
            self.discount_coefficientNPVName: em.discount_coefficient(),
            self.DiscountedMoneyFlowNPVName: discounted_money_flow,
            self.CumDiscMoneyFlowNPVName: cum_disc_money_flow,
        }

        if credit_accounting:
            table[self.CreditsRepaymentNPVName] = repayment

        chart = book.add_chart(
            {
                "type": "scatter",
                "subtype": "smooth_with_markers",
            }
        )

        keys = list(table)
        cmf_ind = keys.index(self.CumulativeMoneyFlowNPVName) + 1
        chart.add_series(
            {
                "categories": [sheet.name, 0, 3, 0, 22],
                "values": [sheet.name, cmf_ind + i, 3, cmf_ind + i, 22],
                "name": [sheet.name, cmf_ind + i, 1, cmf_ind + i, 1],
                # 'line':       {'color': 'red'},
            }
        )

        dcmf_ind = keys.index(self.CumDiscMoneyFlowNPVName) + 1
        chart.add_series(
            {
                "categories": [sheet.name, 0, 3, 0, 22],
                "values": [sheet.name, dcmf_ind + i, 3, dcmf_ind + i, 22],
                "name": [sheet.name, dcmf_ind + i, 1, dcmf_ind + i, 1],
                # 'line':       {'color': 'red'},
            }
        )
        sheet.insert_chart(
            i + 12,
            4,
            chart,
            {
                "x_scale": 2,
                "y_scale": 1,
            },
        )

        i = self.__write_table(book, sheet, i, table, "NPV")
        npv = em.npv(credit_accounting)
        irr = em.irr(credit_accounting)
        rcc = em.return_on_capital_costs()
        tpa = em.turnover_of_production_assets()
        rpp = em.real_payback_period(credit_accounting)
        dpp = em.discounted_payback_period(credit_accounting)

        if rpp is not None:
            rpp_np = rpp.get()
        else:
            rpp_np = dpp

        if dpp is not None:
            dpp_np = dpp.get()
        else:
            dpp_np = dpp

        float_format = book.add_format(self.FloatNumbers)
        title_format = book.add_format(self.TitleFormatDict)
        unit_format = book.add_format(self.UnitFormatDict)
        tablename_format = book.add_format(self.TableNameFormatDict)

        sheet.merge_range(i + 2, 0, i + 8, 0, "Свод", tablename_format)

        i += 2
        sheet.write(i, 1, "NPV", title_format)
        sheet.write(i, 2, str(npv.units), unit_format)
        sheet.write(i, 3, npv.get(), float_format)

        i += 1
        sheet.write(i, 1, "IRR", title_format)
        sheet.write(i, 2, str(irr.units), unit_format)
        sheet.write(i, 3, irr.get(), float_format)

        i += 1
        sheet.write(i, 1, "(B/C)", title_format)
        sheet.write(i, 2, str(rcc.units), unit_format)
        sheet.write(i, 3, rcc.get(), float_format)

        i += 1
        sheet.write(i, 1, "(B-O)/K", title_format)
        sheet.write(i, 2, str(tpa.units), unit_format)
        sheet.write(i, 3, tpa.get(), float_format)

        i += 1
        sheet.write(i, 1, "Индекс доходности", title_format)
        sheet.write(i, 2, str(em.profitability_index().units), unit_format)
        sheet.write(i, 3, em.profitability_index().get(), float_format)

        i += 1
        sheet.write(i, 1, "ПРОСТОЙ СРОК ОКУПАЕМОСТИ (ГОД)", title_format)
        sheet.write(i, 2, "Год", unit_format)
        sheet.write(i, 3, rpp_np, float_format)

        i += 1
        sheet.write(i, 1, "ДИСКОНТИРОВАННЫЙ СРОК ОКУПАЕМОСТИ (ГОД)", title_format)
        sheet.write(i, 2, "Год", unit_format)
        sheet.write(i, 3, dpp_np, float_format)

        i += 1

        pi = em.profitability_index(credit_accounting)
        dr = deepcopy(em.DiscountRate)
        dr.value = dr.value[0]
        text_report = self.text_report(npv, pi, irr, dr, rpp, dpp)
        sheet.merge_range(i + 9, 0, i + 19, 18, text_report, unit_format)

        i += 21

        return i

    def el_table(
        self,
        book: Workbook,
        sheet: Worksheet,
        i: int,
        names: List[str],
        table: Parameter,
    ) -> int:

        # tablename_format = book.add_format(self.TableNameFormatDict)
        float_format = book.add_format(self.FloatNumbers)
        # int_format = book.add_format(self.IntNumbers)
        title_format = book.add_format(self.TitleFormatDict)
        unit_format = book.add_format(self.UnitFormatDict)

        shape = table.shape()
        rows = shape[0]
        for rid in range(rows):
            sheet.write(i + rid, 0, names[rid], title_format)
            sheet.write(i + rid, 1, str(table.units), unit_format)
            sheet.write_row(i + rid, 2, table.get()[rid, :], float_format)

        i += rows
        i += 1
        return i

    def elastic_report(
        self,
        book: Workbook,
        sheet: Worksheet,
        i: int,
        em: EconomicModel,
    ) -> int:
        char_id, names, npv, delta_npv, elastic = em.elasticity()
        float_format = book.add_format(self.FloatNumbers)
        sheet.write_row(i, 2, [0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3], float_format)
        i += 1
        i = self.el_table(book, sheet, i, names, npv)
        i = self.el_table(book, sheet, i, names, delta_npv)
        i = self.el_table(book, sheet, i, names, elastic)

        chart1 = book.add_chart(
            {
                "type": "scatter",
                "subtype": "smooth",
            }
        )

        chart2 = book.add_chart(
            {
                "type": "scatter",
                "subtype": "smooth",
            }
        )

        chart3 = book.add_chart(
            {
                "type": "scatter",
                "subtype": "smooth",
            }
        )

        chart1.set_x_axis(
            {
                "min": min(em.Sensitivity),
                "max": max(em.Sensitivity),
                "major_unit": 0.1,
            }
        )

        chart2.set_x_axis(
            {
                "min": min(em.Sensitivity),
                "max": max(em.Sensitivity),
                "major_unit": 0.1,
            }
        )

        chart3.set_x_axis(
            {
                "min": min(em.Sensitivity),
                "max": max(em.Sensitivity),
                "major_unit": 0.1,
            }
        )

        for cid, chart_type in enumerate(char_id):
            if chart_type == 1:
                chart1.add_series(
                    {
                        "categories": [sheet.name, 0, 2, 0, 9],
                        "values": [sheet.name, cid + 1, 2, cid + 1, 9],
                        "name": [sheet.name, cid + 1, 0, cid + 1, 0],
                        # 'line':       {'color': 'red'},
                    }
                )
            elif chart_type == 2:
                chart2.add_series(
                    {
                        "categories": [sheet.name, 0, 2, 0, 9],
                        "values": [sheet.name, cid + 1, 2, cid + 1, 9],
                        "name": [sheet.name, cid + 1, 0, cid + 1, 0],
                        # 'line':       {'color': 'red'},
                    }
                )
            elif chart_type == 3:
                chart3.add_series(
                    {
                        "categories": [sheet.name, 0, 2, 0, 9],
                        "values": [sheet.name, cid + 1, 2, cid + 1, 9],
                        "name": [sheet.name, cid + 1, 0, cid + 1, 0],
                        # 'line':       {'color': 'red'},
                    }
                )

        sheet.insert_chart(
            "J1",
            chart1,
            {
                "x_scale": 2,
                "y_scale": 1,
            },
        )
        sheet.insert_chart(
            "J16",
            chart2,
            {
                "x_scale": 2,
                "y_scale": 1,
            },
        )
        sheet.insert_chart(
            "J31",
            chart3,
            {
                "x_scale": 2,
                "y_scale": 1,
            },
        )

        return i

    @staticmethod
    def text_report(
        npv_d: Parameter,
        pi: Parameter,
        irr: Parameter,
        dr: Parameter,
        pp: Parameter,
        dpp: Parameter,
    ) -> str:

        # npv_d = em.npv()
        npv = Parameter(round(npv_d.get(), 3), npv_d.units)
        if npv.value > 0:
            npv_choose = f"проект следует принять."
        elif npv.value < 0:
            npv_choose = f"проект принимать не следует."
        else:
            npv_choose = f"принятие проекта не принесет ни прибыли, ни убытка."

        # pi = em.profitability_index()
        pi.value = round(pi.value, 3)
        if pi.value > 1:
            pi_choose = f"проект следует принять."
        elif pi.value < 1:
            pi_choose = f"проект следует отвергнуть."
        else:
            pi_choose = f"проект ни прибыльный, ни убыточный."

        #  irr = em.irr()
        irr.value = round(irr.value[0], 3)
        # dr = deepcopy(em.DiscountRate)
        dr.value = round(dr.value, 3)

        if irr.value > dr.value:
            irr_choose = (
                f"IRR ({str(irr)}) больше нормы дисконта ({str(dr)}) "
                f"проект следует принять."
            )
        elif irr.value < dr.value:
            irr_choose = (
                f"IRR ({str(irr)}) меньше нормы дисконта ({str(dr)}) "
                f"проект следует отвергнуть."
            )
        else:
            irr_choose = (
                f"IRR ({str(irr)}) равен норме дисконта ({str(dr)}) "
                f"нельзя однозначно точно вынети решение "
                f"о реализации проекта, поскольку проект "
                f"ни прибыльный, ни убыточный."
            )

        # pp = em.real_payback_period()
        if pp is not None:
            pp.value = round(pp.value, 3)
            pp_choose = f"срок окупаемости проекта {pp}"
        else:
            pp_choose = f"срока окупаемости в заданный период нет"

        # dpp = em.discounted_payback_period()
        if dpp is not None:
            dpp.value = round(dpp.value, 3)
            dpp_choose = f" а дисконтированный cрок окупаемости проекта {dpp}."
        else:
            dpp_choose = f"при отсутсвующем дисконтированном сроке окупаемости"

        text = (
            f"На основании NPV, значение которого имеет {str(npv)}, {npv_choose}\n"
            f"На основании индекса рентабельности, значение которого имеет {str(pi)}"
            f" {pi_choose}\n"
            f"Исходя из того, что {irr_choose}\n"
            f"Дополнительно отметим, что {pp_choose}, {dpp_choose}"
        )
        return text

    def credits_report(
        self,
        book: Workbook,
        sheet: Worksheet,
        i: int,
        em: EconomicModel,
    ) -> int:
        all_credits = em.Credits.Pack
        str_format = book.add_format(self.TitleFormatDict)
        float_format = book.add_format(self.FloatNumbers)
        int_format = book.add_format(self.FloatNumbers)
        for cr_name, cr in all_credits.items():
            credits_flow = cr.calculate()
            sheet.merge_range(i, 0, i, 1, "Метод", str_format)
            sheet.merge_range(i + 1, 0, i + 1, 1, "ПОСТУПЛЕНИЕ", str_format)
            sheet.merge_range(i + 2, 0, i + 2, 1, "Момент выдачи", str_format)
            sheet.merge_range(i + 3, 0, i + 3, 1, "ЛЬГОТНЫЙ ПЕРИОД", str_format)
            sheet.merge_range(i + 4, 0, i + 4, 1, "ПРОЦЕНТНАЯ СТАВКА", str_format)
            sheet.merge_range(i + 5, 0, i + 5, 1, "ДЛИТЕЛЬНОСТЬ ЗАЙМА", str_format)
            sheet.merge_range(i + 6, 0, i + 6, 1, "КАПИТАЛИЗАЦИЯ ПРОЦЕНТОВ", str_format)

            sheet.merge_range(i, 2, i, 3, cr.Method, str_format)
            sheet.write(i + 1, 2, str(cr.LoanAmount.units), str_format)
            sheet.write(i + 2, 2, str(cr.IssueTime.units), str_format)
            sheet.write(i + 3, 2, str(cr.GracePeriod.units), str_format)
            sheet.write(i + 4, 2, str(cr.InterestRate.units), str_format)
            sheet.write(i + 5, 2, str(cr.LoanTime.units), str_format)
            sheet.write(i + 6, 2, str(cr.InterestCapitalization.units), str_format)

            sheet.write(i + 1, 3, cr.LoanAmount.get(), float_format)
            sheet.write(i + 2, 3, cr.IssueTime.get(), float_format)
            sheet.write(i + 3, 3, cr.GracePeriod.get(), int_format)
            sheet.write(i + 4, 3, cr.InterestRate.get(), int_format)
            sheet.write(i + 5, 3, cr.LoanTime.get(), int_format)
            sheet.write(i + 6, 3, cr.InterestCapitalization.get(), float_format)

            i += 7
            i = self.__write_table(book, sheet, i, credits_flow, cr_name)
            i += 2
        return i

    def one_sheet_report(self, em: EconomicModel) -> None:
        book = xlsw.Workbook("report.xlsx")
        sheet = book.add_worksheet("test")
        i = 0
        i = self.__capex_report(book, sheet, i, em)
        i = self.production_report(book, sheet, i, em)
        i = self.opex_report(book, sheet, i, em)
        i = self.market_report(book, sheet, i, em)
        i = self.tax_report(book, sheet, i, em)
        self.npv_table(book, sheet, i, em)
        book.close()

    def different_sheets_report(self, em: EconomicModel, name: str = None) -> None:
        if name is not None:
            book = xlsw.Workbook(name)
        else:
            book = xlsw.Workbook(self.__book_name())

        sheet = book.add_worksheet("CAPEX")
        sheet.set_column(0, 0, 2.5)
        sheet.set_column(1, 1, 25)
        sheet.set_column(2, 2, 15)
        self.__capex_report(book, sheet, 0, em)

        sheet = book.add_worksheet("Production")
        sheet.set_column(0, 0, 2.5)
        sheet.set_column(1, 1, 25)
        sheet.set_column(2, 2, 15)
        self.production_report(book, sheet, 0, em)

        sheet = book.add_worksheet("OPEX")
        sheet.set_column(0, 0, 2.5)
        sheet.set_column(1, 1, 25)
        sheet.set_column(2, 2, 15)
        self.opex_report(book, sheet, 0, em)

        sheet = book.add_worksheet("Market")
        sheet.set_column(0, 0, 2.5)
        sheet.set_column(1, 1, 25)
        sheet.set_column(2, 2, 15)
        self.market_report(book, sheet, 0, em)

        sheet = book.add_worksheet("Tax")
        sheet.set_column(0, 0, 2.5)
        sheet.set_column(1, 1, 25)
        sheet.set_column(2, 2, 15)
        self.tax_report(book, sheet, 0, em)

        sheet = book.add_worksheet("NPV")
        sheet.set_column(0, 0, 2.5)
        sheet.set_column(1, 1, 45)
        sheet.set_column(2, 2, 15)
        i = self.npv_table(book, sheet, 0, em)
        self.npv_table(book, sheet, i, em, True)

        sheet = book.add_worksheet("Elastic")
        sheet.set_column(0, 0, 45)
        sheet.set_column(1, 1, 10)
        self.elastic_report(book, sheet, 0, em)

        sheet = book.add_worksheet("Credits")
        sheet.set_column(0, 0, 2.5)
        sheet.set_column(1, 1, 25)
        sheet.set_column(2, 2, 15)
        self.credits_report(book, sheet, 0, em)

        sheet = book.add_worksheet("MonteСarlo")

        self.monte_carlo(book, sheet, 0, em)

        book.close()

    def monte_carlo(
        self,
        book: Workbook,
        sheet: Worksheet,
        i: int,
        em: EconomicModel,
    ) -> None:

        int_format = book.add_format(self.IntNumbers)
        float_format = book.add_format(self.FloatNumbers)
        str_format = book.add_format(self.TitleFormatDict)
        mc = MonteCarlo()
        results = mc.monte_carlo(em)
        sheet.write(0, 0, "Number", str_format)
        sheet.write(0, 1, "Values", str_format)
        sheet.write_column(1, 0, np.arange(len(results.npv())), int_format)
        sheet.write_column(1, 1, results.npv(), float_format)
        str_n, cr = results.clustering()

        sheet.write(0, 3, "Interval", str_format)
        sheet.write(0, 4, "Quantity", str_format)
        sheet.write_column(1, 3, str_n, float_format)
        sheet.write_column(1, 4, cr, float_format)

        chart1 = book.add_chart(
            {
             'type': 'column',
             'subtype': 'stacked',
            }
        )

        chart1.add_series(
            {
                # "name": [sheet.name, 0, 2, 0, 9],
                "values": [sheet.name, 1, 4, 1++ len(str_n), 4],
                "categories": [sheet.name, 1, 3, 1++ len(str_n), 3],
                # 'line':       {'color': 'red'},
            }
        )

        sheet.insert_chart(
            "J1",
            chart1,
            {
                "x_scale": 2,
                "y_scale": 1,
            },
        )
        # chart = book.add_chart({'type': 'stock', 'subtype': 'clustered' })
        # chart.add_series({
        # 'categories': [sheet.name, 0, 0, 4, 0],
        # 'values': [sheet.name, 1, 1, 1+len(results.npv()), 1],
        # 'line': {'color': 'red'},
        # }
        # )
        # sheet.insert_chart('C1', chart)
        results.to_excel("MonteCarlo_All_Data.xlsx")
