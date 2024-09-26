#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: zj
# date: 2024/1/5
import pandas as pd


# 等额本金
def calculate_equal_principal_loan(principal, annual_interest_rate, years):
    """
    等额本金（Equal Principal Payment）

    定义： 在等额本金还款方式中，每月偿还的本金金额是固定的，而每月的利息金额会随着剩余未偿还本金的减少而逐渐减少。

    特点：

    每月还款总额 = 本金 / 还款期数 + 剩余未偿还本金 * 月利率
    每月偿还的本金固定，每月支付的利息逐渐减少。
    总还款金额相对较低，利息支出相对较少。
    优点：

    总还款金额相对较低，适合希望尽早还清本金的借款人。
    缺点：

    前期月供较高，可能对还款人的月负担产生一定影响。
    """
    monthly_interest_rate = annual_interest_rate / 12 / 100
    total_payments = years * 12
    monthly_principal = principal / total_payments
    remaining_principal = principal
    payments = []
    principals = []
    interests = []
    remaning_principals = []

    for month in range(1, total_payments + 1):
        monthly_interest = remaining_principal * monthly_interest_rate
        monthly_payment = monthly_principal + monthly_interest
        remaining_principal -= monthly_principal

        payments.append(monthly_payment)
        principals.append(monthly_principal)
        interests.append(monthly_interest)
        remaning_principals.append(remaining_principal)

        print(f"Month {month}: Payment - {monthly_payment:.2f}, Principal - {monthly_principal:.2f}, "
              f"Interest - {monthly_interest:.2f}, Remaining Principal - {remaining_principal:.2f}")

    df = pd.DataFrame(
        data={"Month": list(range(1, total_payments + 1)), "Payment": payments, "Principal": principals,
              "Interest": interests,
              "Remaining Principai": remaning_principals},
        columns=["Month", "Payment", "Principal", "Interest", "Remaining Principai"])
    pd.set_option("display.float_format", "{:,.4f}".format)
    return df


# 等额本息
def calculate_equal_installment_loan(principal, annual_interest_rate, years):
    monthly_interest_rate = annual_interest_rate / 12 / 100
    total_payments = years * 12

    monthly_payment = (principal * monthly_interest_rate) / (1 - (1 + monthly_interest_rate) ** -total_payments)

    payments = []
    principals = []
    interests = []
    remaning_principals = []

    for month in range(1, total_payments + 1):
        monthly_interest = principal * monthly_interest_rate
        monthly_principal = monthly_payment - monthly_interest
        principal -= monthly_principal

        payments.append(monthly_payment)
        principals.append(monthly_principal)
        interests.append(monthly_interest)
        remaning_principals.append(principal)

        print(f"Month {month}: Payment - {monthly_payment:.2f}, Principal - {monthly_principal:.2f}, "
              f"Interest - {monthly_interest:.2f}, Remaining Principal - {principal:.2f}")
    df = pd.DataFrame(
        data={"Month": list(range(1, total_payments + 1)), "Payment": payments, "Principal": principals,
              "Interest": interests,
              "Remaining Principai": remaning_principals},
        columns=["Month", "Payment", "Principal", "Interest", "Remaining Principai"])
    pd.set_option("display.float_format", "{:,.4f}".format)

    return df


def main():
    # 示例
    principal_amount = 6  # 贷款本金
    annual_interest_rate = 4.1  # 年利率
    loan_years = 1  # 还款年限

    df = calculate_equal_principal_loan(principal_amount, annual_interest_rate, loan_years)

    # df = calculate_equal_installment_loan(principal_amount, annual_interest_rate, loan_years)
    print(df)
    print(f"interest sum: {df['Interest'].sum():.4f}")
    print(f"Principal sum: {df['Principal'].sum()}")


if __name__ == '__main__':
    main()
