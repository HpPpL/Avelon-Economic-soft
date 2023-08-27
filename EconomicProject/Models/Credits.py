from __future__ import annotations

import numpy as np

# from pathlib import Path
from copy import deepcopy
from typing import Dict, Optional  # , Tuple,
from abc import abstractmethod

from Units.Variables import Parameter

# from Units.Units import TimeUnit, PercentUnit
from ReaderWriter.SheetNames import Credits
from ReaderWriter.Reader import ECOExcel  # , read_eco_excel


class CreditsMethod:

    Annual_payment = "ГОДОВАЯ ВЫПЛАТА"
    Repayment = "ПОГАШЕНИЕ"
    Duty = "ОСТАТОК НА КОНЕЦ ГОДА"
    PaymentOfInterest = "ВЫПЛАТА ПРОЦЕНТОВ"

    def __init__(
        self,
        method: str,
        loan_amount: Parameter,
        issue_time: Parameter,
        grace_period: Parameter,
        interest_rate: Parameter,
        loan_time: Parameter,
        interest_capitalization: Parameter,
        years: Parameter,
    ) -> None:
        self.Method = method
        self.LoanAmount = loan_amount
        self.IssueTime = issue_time
        self.GracePeriod = grace_period
        self.InterestRate = interest_rate
        self.LoanTime = loan_time
        self.InterestCapitalization = interest_capitalization
        self.Years = years

    @abstractmethod
    def payments(self) -> Parameter:
        pass

    @abstractmethod
    def repayment(self) -> Parameter:
        pass

    @abstractmethod
    def interest_payment(self) -> Parameter:
        pass

    @abstractmethod
    def calculate(
        self,
    ) -> Dict[str, Parameter]:
        pass


class LinerCredit(CreditsMethod):
    def __init__(
        self,
        method: str,
        loan_amount: Parameter,
        issue_time: Parameter,
        grace_period: Parameter,
        interest_rate: Parameter,
        loan_time: Parameter,
        interest_capitalization: Parameter,
        years: Parameter,
    ) -> None:
        super().__init__(
            method,
            loan_amount,
            issue_time,
            grace_period,
            interest_rate,
            loan_time,
            interest_capitalization,
            years,
        )

    def repayment_one(self) -> Parameter:

        duty = deepcopy(self.LoanAmount)
        life_time = self.LoanTime.value
        cap_time = self.InterestCapitalization.value
        # privilege_time = self.GracePeriod.value

        return duty / (life_time - cap_time)

    def grace_period(self) -> Parameter:
        return self.IssueTime + self.GracePeriod

    def capitalization_period(self) -> Parameter:
        gp = self.grace_period()
        return gp + self.InterestCapitalization

    def end_of_loan(self) -> Parameter:
        gp = deepcopy(self.LoanTime)
        gp.value = 1
        return self.LoanTime + self.GracePeriod - gp

    def __get_base_duty(self) -> Parameter:
        duty = deepcopy(self.LoanAmount)
        duty.value = np.ones(self.Years.value.shape) * self.LoanAmount.value
        return duty

    def __get_interest_flow(self) -> Parameter:
        interest_flow = deepcopy(self.LoanAmount)
        interest_flow.value = np.zeros(self.Years.value.shape)
        return interest_flow

    def __get_payments_flow(self) -> Parameter:
        payments_flow = deepcopy(self.LoanAmount)
        payments_flow.value = np.zeros(self.Years.value.shape)
        return payments_flow

    def __get_repayments_flow(self) -> Parameter:
        repayments_flow = deepcopy(self.LoanAmount)
        repayments_flow.value = np.zeros(self.Years.value.shape)
        return repayments_flow

    def calculate(
        self,
    ) -> Dict[str, Parameter]:

        duty = self.__get_base_duty()
        interest_payments = self.__get_interest_flow()
        debt_payments = self.__get_payments_flow()
        all_payments = self.__get_repayments_flow()
        repay = self.repayment_one()

        for yid, y in enumerate(self.Years.value):

            if y < self.grace_period().value:
                pass

            elif y < self.capitalization_period().value:
                debt_increase = duty.value[yid] * self.InterestRate.value
                duty.value[yid:] = duty.value[yid] + debt_increase

            elif y <= self.end_of_loan().value + 1:
                percent = (duty - repay) * self.InterestRate
                interest_payments.value[yid] = percent.value[yid]
                percent.value = percent.value[yid]

                d_step = deepcopy(duty)
                d_step.value = d_step.value[yid]
                pay = repay + percent

                all_payments.value[yid] = pay.value

                debt_payments.value[yid] = repay.value
                duty.value[yid:] = (d_step - repay).value
            else:
                pass

        results = {
            self.Duty: duty,
            self.Annual_payment: debt_payments,
            self.PaymentOfInterest: interest_payments,
            self.Repayment: all_payments,
        }

        return results

    def repayment(self) -> Parameter:
        duty, payments_flow, interest_flow, repayments_flow = self.calculate()
        return repayments_flow

    def interest_payment(self, repayment: Parameter = None) -> Parameter:
        duty, payments_flow, interest_flow, repayments_flow = self.calculate()
        return interest_flow

    def payments(self) -> Parameter:
        duty, payments_flow, interest_flow, repayments_flow = self.calculate()
        return payments_flow


class NotLinerCredits(CreditsMethod):
    def __init__(
        self,
        method: str,
        loan_amount: Parameter,
        issue_time: Parameter,
        grace_period: Parameter,
        interest_rate: Parameter,
        loan_time: Parameter,
        interest_capitalization: Parameter,
        years: Parameter,
    ) -> None:
        super().__init__(
            method,
            loan_amount,
            issue_time,
            grace_period,
            interest_rate,
            loan_time,
            interest_capitalization,
            years,
        )

    def repayment_one(self) -> Parameter:
        rate = self.InterestRate.value
        life_time = self.LoanTime.value
        cap_time = self.InterestCapitalization.value
        privilege_time = self.GracePeriod.value

        multi = (1 + rate) ** life_time
        numerator = self.LoanAmount * multi * rate
        denominator = (1 + rate) ** (life_time - cap_time - privilege_time) - 1
        return numerator / denominator

    def grace_period(self) -> Parameter:
        return self.IssueTime + self.GracePeriod

    def capitalization_period(self) -> Parameter:
        gp = self.grace_period()
        return gp + self.InterestCapitalization

    def end_of_loan(self) -> Parameter:
        gp = deepcopy(self.LoanTime)
        gp.value = 1
        return self.LoanTime + self.GracePeriod - gp

    def __get_base_duty(self) -> Parameter:
        duty = deepcopy(self.LoanAmount)
        duty.value = np.ones(self.Years.value.shape) * self.LoanAmount.value
        return duty

    def __get_interest_flow(self) -> Parameter:
        interest_flow = deepcopy(self.LoanAmount)
        interest_flow.value = np.zeros(self.Years.value.shape)
        return interest_flow

    def __get_payments_flow(self) -> Parameter:
        payments_flow = deepcopy(self.LoanAmount)
        payments_flow.value = np.zeros(self.Years.value.shape)
        return payments_flow

    def get_repayments_flow(self) -> Parameter:
        repayments_flow = deepcopy(self.LoanAmount)
        repayments_flow.value = np.zeros(self.Years.value.shape)
        return repayments_flow

    def calculate(
        self,
    ) -> Dict[str, Parameter]:

        duty = self.__get_base_duty()
        interest_payments = self.__get_interest_flow()
        debt_payments = self.__get_payments_flow()
        all_payments = self.get_repayments_flow()
        pay = self.repayment_one()

        for yid, y in enumerate(self.Years.value):

            if y < self.capitalization_period().value:
                debt_increase = duty.value[yid] * self.InterestRate.value
                duty.value[yid:] = duty.value[yid] + debt_increase

            elif y < self.grace_period().value:
                percent = duty * self.InterestRate
                interest_payments.value[yid] = percent.value[yid]

            elif y <= self.end_of_loan().value + 1:
                percent = duty * self.InterestRate
                interest_payments.value[yid] = percent.value[yid]
                percent.value = percent.value[yid]

                d_step = deepcopy(duty)
                d_step.value = d_step.value[yid]
                repay = pay - percent

                all_payments.value[yid] = pay.value

                debt_payments.value[yid] = repay.value
                duty.value[yid:] = (d_step - repay).value

        results = {
            self.Duty: duty,
            self.Annual_payment: debt_payments,
            self.PaymentOfInterest: interest_payments,
            self.Repayment: all_payments,
        }

        return results

    def repayment(self) -> Parameter:
        duty, payments_flow, interest_flow, repayments_flow = self.calculate()
        return repayments_flow

    def interest_payment(self, repayment: Parameter = None) -> Parameter:
        duty, payments_flow, interest_flow, repayments_flow = self.calculate()
        return interest_flow

    def payments(self) -> Parameter:
        duty, payments_flow, interest_flow, repayments_flow = self.calculate()
        return payments_flow


class CreditPortfolio:
    def __init__(self) -> None:
        self.Pack: Dict[str, CreditsMethod] = dict()

    def __getitem__(self, key: str) -> CreditsMethod:
        return self.Pack[key]

    def __setitem__(self, key: str, value: CreditsMethod) -> None:
        self.Pack[key] = value

    def repayment(self) -> Optional[Parameter]:
        results = None
        for name, credits in self.Pack.items():
            if results is None:
                results = credits.calculate()[CreditsMethod.Repayment]
            else:
                results += credits.calculate()[CreditsMethod.Repayment]

        return results

    def payment_of_interest(self) -> Optional[Parameter]:
        results = None
        for name, credits in self.Pack.items():
            if results is None:
                results = credits.calculate()[CreditsMethod.PaymentOfInterest]
            else:
                results += credits.calculate()[CreditsMethod.PaymentOfInterest]

        return results


class CreditsGenerator:
    @classmethod
    def get_liner_method(
        cls,
        exce: ECOExcel,
        table_name: str,
    ) -> LinerCredit:

        method = "линейный"

        loan_amount = exce.get(
            Credits.Name,
            table_name,
            Credits.LoanAmount,
            "first",
        )

        issue_time = exce.get(
            Credits.Name,
            table_name,
            Credits.IssueTime,
            "first",
        )
        grace_period = exce.get(
            Credits.Name,
            table_name,
            Credits.GracePeriod,
            "first",
        )
        interest_rate = exce.get(
            Credits.Name,
            table_name,
            Credits.InterestRate,
            "first",
        )
        loan_time = exce.get(
            Credits.Name,
            table_name,
            Credits.LoanTime,
            "first",
        )
        int_cap = exce.get(
            Credits.Name,
            table_name,
            Credits.InterestCapital,
            "first",
        )

        years = exce.get(
            Credits.Name,
            table_name,
            Credits.Years,
            "Zero",
        )

        credits_model = LinerCredit(
            method,
            loan_amount,
            issue_time,
            grace_period,
            interest_rate,
            loan_time,
            int_cap,
            years,
        )

        return credits_model

    @classmethod
    def get_not_liner_method(
        cls,
        exce: ECOExcel,
        table_name: str,
    ) -> NotLinerCredits:

        method = "Не линейный"
        loan_amount = exce.get(
            Credits.Name,
            table_name,
            Credits.LoanAmount,
            "first",
        )

        issue_time = exce.get(
            Credits.Name,
            table_name,
            Credits.IssueTime,
            "first",
        )
        grace_period = exce.get(
            Credits.Name,
            table_name,
            Credits.GracePeriod,
            "first",
        )
        interest_rate = exce.get(
            Credits.Name,
            table_name,
            Credits.InterestRate,
            "first",
        )
        loan_time = exce.get(
            Credits.Name,
            table_name,
            Credits.LoanTime,
            "first",
        )
        int_cap = exce.get(
            Credits.Name,
            table_name,
            Credits.InterestCapital,
            "first",
        )

        years = exce.get(
            Credits.Name,
            table_name,
            Credits.Years,
            "Zero",
        )

        credits_model = NotLinerCredits(
            method,
            loan_amount,
            issue_time,
            grace_period,
            interest_rate,
            loan_time,
            int_cap,
            years,
        )
        return credits_model

    @classmethod
    def get_credits(cls, eco_excel: ECOExcel) -> CreditPortfolio:
        credit_portfolio = CreditPortfolio()

        sheet = eco_excel[Credits.Name]
        for table_name, table in sheet.Tables.items():
            method = table[Credits.Method].value[3].lower().strip()
            if method == "линейный":
                lc = cls.get_liner_method(eco_excel, table_name)
                credit_portfolio[table_name] = lc
            elif method == "не линейный":
                nlc = cls.get_not_liner_method(eco_excel, table_name)
                credit_portfolio[table_name] = nlc

        return credit_portfolio


"""
def choose_nlc(money_flow: Parameter, start: int, end: int):

    method = "Не линейный"
    loan_amount = deepcopy(money_flow)
    loan_amount.value = sum(money_flow.value[:start])
    issue_time = Parameter(1, deepcopy(TimeUnit))
    grace_period = Parameter(0, deepcopy(TimeUnit))
    interest_rate = Parameter(0.1, deepcopy(PercentUnit))
    loan_time = Parameter(end, deepcopy(TimeUnit))
    interest_capitalization = Parameter(start, deepcopy(TimeUnit))
    years = Parameter(np.arange(1, len(money_flow.value) + 1), deepcopy(TimeUnit))

    nlc = NotLinerCredits(
        method,
        loan_amount,
        issue_time,
        grace_period,
        interest_rate,
        loan_time,
        interest_capitalization,
        years,
    )

def choose_credits(money_flow: Parameter) -> Optional[CreditsMethod]:

    start = None
    for vid, value in enumerate(money_flow.value):
        if value > 0:
            start = vid
            break

    end = None
    for vid, value in enumerate(money_flow.value[::-1]):
        if value > 0:
            end = vid
            break
        elif vid == len(money_flow.value) - 1:
            end = vid

    if start is None:
        return None

    total_expenses = sum(money_flow.value[:start])
    total_income = sum(money_flow.value[start:end])
    if total_expenses > total_income:
        return None



if __name__ == "__main__":
    link = Path(r"..\Pattern.xls")
    ECO = read_eco_excel(link)
    CP = CreditsGenerator.get_credits(ECO)
    CP.repayment()
    pass
"""
