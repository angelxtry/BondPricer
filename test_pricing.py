# -*- conding: utf-8 -*-
""" TEST PRICING """
import LoadJson
import pricing

def test_coupon_bond_standard_ver1():
    """ 이표채 테스트 """

    # KR623919J629 티월드제1차1-18
    # ISSUE_DAY 20160229
    # MAT_DAY 20170829
    # INT_PAY_TYPE_CODE 13
    # INT_PERIOD_MONTH 1
    # 20160629 이표지급일
    data = LoadJson.LoadJson('BondData_KR623919J629.json')
    dic_bond = data.read_json_file()

    for item in dic_bond.keys():
        p = pricing.BondPricing(dic_bond[item], "20160229", 1.684) #발행일
        assert p.calc_bond_price() == 10000

        p = pricing.BondPricing(dic_bond[item], "20160628", 1.462)
        assert p.calc_bond_price() == 10039.3036465

        p = pricing.BondPricing(dic_bond[item], "20160629", 1.462)
        assert p.calc_bond_price() == 10039.6982019

        p = pricing.BondPricing(dic_bond[item], "20160630", 1.456)
        assert p.calc_bond_price() == 10026.7645338

        p = pricing.BondPricing(dic_bond[item], "20160630", -1.456) #마이너스 금리
        assert p.calc_bond_price() == 10369.2687619

def test_coupon_bond_standard_ver2():
    """ 이표채 테스트 일할계산"""

    # KR6228071595 아사도3차1-1
    # ISSUE_DAY 20150916
    # MAT_DAY 20160916
    # INT_PAY_TYPE_CODE 13
    # INT_PERIOD_MONTH 1
    # 이표지급일 매달 16일
    data = LoadJson.LoadJson('BondData_KR6228071595.json')
    dic_bond = data.read_json_file()

    for item in dic_bond.keys():
        p = pricing.BondPricing(dic_bond[item], "20150916", 3.720) #발행일
        assert p.calc_bond_price() == 10000

        p = pricing.BondPricing(dic_bond[item], "20160204", 3.290)
        assert p.calc_bond_price() == 10045.5488998

        p = pricing.BondPricing(dic_bond[item], "20160215", 3.236)
        assert p.calc_bond_price() == 10058.6447763

        p = pricing.BondPricing(dic_bond[item], "20160216", 3.237)
        assert p.calc_bond_price() == 10059.478727

        p = pricing.BondPricing(dic_bond[item], "20160217", 3.196)
        assert p.calc_bond_price() == 10031.1314208

        p = pricing.BondPricing(dic_bond[item], "20160204", -3.29) #마이너스 금리
        assert p.calc_bond_price() == 10456.5069252
    