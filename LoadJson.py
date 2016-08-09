#-*- coding:utf-8 -*-
"""특정 json 파일을 읽어 데이터를 로드"""

import json

class LoadJson():
    """
    특정 json 파일을 읽어 데이터를 로드
    PARAM filename String
    """
    def __init__(self, filename):
        self.filename = filename

    def read_json_file(self):
        """
        특정 json 파일을 읽어 Dictionary 생성 후 return
        RETURN dic_bond_temp Dictionary
        """
        fd = open(self.filename, 'r')
        dic_bond_temp = json.loads(fd.read())
        fd.close()
        return dic_bond_temp

if __name__ == "__main__":
    data = LoadJson('BondData_KR623919J629.json')
    dic_bond = data.read_json_file()
    print(dic_bond)
