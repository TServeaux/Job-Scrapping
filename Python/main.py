import organize as org
import json

if __name__ == "__main__" :

    with open("./data/data.json",'r',encoding='utf-8') as d:
        data = json.load(d)

    org.createReport(data['keyWord'],data['loc'],data['codeInsee'],data['resN'])