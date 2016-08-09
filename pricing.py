# -*- coding: utf-8 -*-
# pricing.py
"""
채권 가격 계산
TODO 계산과정을 별로의 class로 분리하자.
"""
import datetime
import LoadJson

class BondPricing:
    """
    채권 가격 계산
    채권 정보와 날짜 YTM을 파라미터로 받음
    PARAM bond Dictionary
    PARAM today String
    PARAM ytm Float
    """

    def __init__(self, bond, today, ytm):
        self.bond = bond
        self.today = today
        self.ytm = ytm / 100

        self.remain_days = 0
        self.section_days = 0

        self.discount_price_list = []
        self.discount_price = 0
        self.present_value = 0

        self.calc_days()

    def calc_days(self):
        """ remain_days, section_days 계산 """
        for cf in self.bond['CASH_FLOW']:
            if self.today <= cf[2]:
                today = datetime.datetime.strptime(self.today, "%Y%m%d").date()
                int_end = datetime.datetime.strptime(cf[2], "%Y%m%d").date()
                self.remain_days = (int_end - today).days
                self.section_days = cf[3]
                break


    def calc_bond_price(self):
        """ 계산 """

        if self.bond['INT_PAY_TYPE_CODE'] == '11':
            pass
        elif self.bond['INT_PAY_TYPE_CODE'] == '12':
            pass
        elif self.bond['INT_PAY_TYPE_CODE'] == '13':
            if self.bond['COUPON_PRORATED'] == '1':
                return self.calc_coupon_bond_standard_ver2()
            else:
                return self.calc_coupon_bond_standard_ver1()
        elif self.bond['INT_PAY_TYPE_CODE'] == '14':
            pass
        return self.present_value

    def calc_simple_interest_bond(self):
        """ 단리채 int_pay_type_code == 14 """
        pass

    def calc_compound_bond(self):
        """ 복리채 int_pay_type_code == 12 """
        pass

    def calc_zero_coupon_bond(self):
        """ 할인채 int_pay_type_code == 11 """
        pass

    def calc_coupon_bond_standard_ver1(self):
        """ 이표채 int_pay_type_code == 13 and 일할계산 COUPON_PRORATED <> 1 """
        count = 0
        for cf in self.bond['CASH_FLOW']:
            if self.today <= cf[2]:
                tmp_price = cf[0]/((1+self.ytm/12 \
                / self.bond['INT_PERIOD_MONTH'])**count)
                self.discount_price_list.append(tmp_price)
                count += 1

        for cf in self.discount_price_list:
            self.discount_price += cf

        self.present_value = self.discount_price \
            / (1+(self.ytm/12/self.bond['INT_PERIOD_MONTH']) \
            *(self.remain_days/self.section_days))
        self.present_value = round(self.present_value, 7)
        return self.present_value

    def calc_coupon_bond_standard_ver2(self):
        """ 이표채 int_pay_type_code == 13 and 일할계산 COUPON_PRORATED == 1 """
        count = 0
        self.bond['CASH_FLOW'].reverse()
        for cf in self.bond['CASH_FLOW']:
            if self.today <= cf[1]:
                tmp_price = cf[0]
                for cf2 in self.bond['CASH_FLOW'][count:]:
                    if self.today <= cf2[1]:
                        tmp_price = tmp_price/(1+self.ytm*cf2[3]/365)
                    else:
                        break
                count = count + 1
                self.discount_price_list.append(tmp_price)
            elif self.today <= cf[2]:
                self.discount_price_list.append(cf[0])
                break
        self.bond['CASH_FLOW'].reverse()

        for price in self.discount_price_list:
            self.discount_price += price

        if self.today == self.bond['ISSUE_DAY']:
            self.present_value = self.discount_price
        else:
            self.present_value = self.discount_price / (1+self.ytm*self.remain_days/365)
        self.present_value = round(self.present_value, 7)
        return self.present_value

    def print_basic_info(self):
        """기본 정보 및 날짜 출력"""
        print("Today: ", self.today)
        print("Remain days: ", self.remain_days)
        print("Section days: ", self.section_days)
        print("YTM: ", self.ytm)

    def print_price(self):
        """가격 출력"""
        for cf in self.discount_price_list:
            print(cf)
        print(self.discount_price)
        print(round(self.present_value, 7))

    def print_cash_flow(self):
        """cash_flow 확인"""
        print("CASH_FLOW")
        for cf in self.bond['CASH_FLOW']:
            print(cf)

if __name__ == "__main__":
    data = LoadJson.LoadJson('BondData_KR623919J629.json')
    dic_bond = data.read_json_file()

    for item in dic_bond.keys():
        p = BondPricing(dic_bond[item], "20160628", 1.462) #발행일
        p.print_basic_info()
        p.calc_bond_price()
        p.print_price()
