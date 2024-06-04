import json

from flask import Blueprint, jsonify, request
import pymysql
import pymysql.cursors
from datetime import datetime
from db_connect import fetch_all, fetch_one, insert, delete, update, fetch_total
import re
# 创建一个蓝图对象
structure_api_blueprint = Blueprint('structure_api', __name__)


def getExpectedExpression(demand):
    demandId = demand['id']
    demandName = demand['demandname']
    parentD = demand['parentD']
    expression = "(%s,%s,AggregationRelation)" % (demandId, parentD)
    return expression



def genStructureRule(projecname):
    table_name = f"{projecname}Demand"
    category_filter = "category='功能' OR category='执行流程' OR category='业务' OR category='智能合约' "
    all_demandsql = f"SELECT * FROM `{table_name}` WHERE {category_filter}"
    all_demands = fetch_total(all_demandsql)
    id2name = {0: projecname}
    structureRule_name = f"{projecname}StructureRule"

    #清空规则表，重新生成
    delete_sql = f"DELETE FROM `{structureRule_name}`"
    delete(delete_sql, None)

    for demand in all_demands:
        demandId = demand['id']
        demandname = demand['demandname']
        id2name[demandId] = demandname

    for demand in all_demands:
        expectedExpression = getExpectedExpression(demand)
        get_id_sql = f"SELECT id FROM `{structureRule_name}` ORDER BY id DESC LIMIT 1"
        row = fetch_one(get_id_sql, None)
        max_id = row['id'] if row else 0
        id_sql = f"ALTER TABLE `{structureRule_name}` AUTO_INCREMENT = {max_id + 1}"
        update(id_sql, None)
        insert_sql = f"INSERT INTO `{structureRule_name}` (demandId, demandName, expectedExpression) VALUES (%s, %s, %s)"
        insert(insert_sql, (demand['parentD'], id2name[demand['parentD']], expectedExpression))


    category_function = "category='方法'"
    function_demand_sql = f"SELECT * FROM `{table_name}` WHERE {category_function}"
    all_functions = fetch_total(function_demand_sql)
    for function in all_functions:
        demandId = function['id']
        demandname = function['demandname']
        id2name[demandId] = demandname
    for function in all_functions:
        demandId = function['id']
        demandName = function['demandname']
        parentD = function['parentD']
        expression = "(%s,%s,MethodCorrelation)" % (demandId, parentD)
        get_id_sql = f"SELECT id FROM `{structureRule_name}` ORDER BY id DESC LIMIT 1"
        row = fetch_one(get_id_sql, None)
        max_id = row['id'] if row else 0
        id_sql = f"ALTER TABLE `{structureRule_name}` AUTO_INCREMENT = {max_id + 1}"
        update(id_sql, None)
        insert_sql = f"INSERT INTO `{structureRule_name}` (demandId, demandName, expectedExpression) VALUES (%s, %s, %s)"
        insert(insert_sql, (function['parentD'], id2name[function['parentD']], expression))

@structure_api_blueprint.route('/getStructure', methods=['POST'])
def getStructureData():
    page = request.form.get('currentPage', default=1, type=int)
    print(page)
    size = request.form.get('size', default=10, type=int)
    offset = (page - 1) * size
    projecname = request.form.get('projectname')
    table_name = f"{projecname}Demand"

    category_filter = "category='功能' OR category='执行流程' OR category='业务' OR category='智能合约' "
    fetch_sql = f"SELECT * FROM `{table_name}` WHERE {category_filter} LIMIT %s OFFSET %s"
    demands = fetch_all(fetch_sql, (size, offset))


    all_demandsql = f"SELECT * FROM `{table_name}` WHERE {category_filter}"
    all_demands = fetch_total(all_demandsql)
    id2name = {0:projecname}
    structureRule_name = f"{projecname}StructureRule"
    for demand in all_demands:
        demandId = demand['id']
        demandname = demand['demandname']
        id2name[demandId] = demandname

    genStructureRule(projecname)

    fetch_rule_sql = f"SELECT * FROM `{structureRule_name}` LIMIT %s OFFSET %s"
    structure_rules = fetch_all(fetch_rule_sql,(size,offset))
    # count_sql = f"SELECT COUNT(*) AS total FROM `{table_name}` WHERE {category_filter}"
    # total = fetch_one(count_sql, None)['total']

    count_sql = f"SELECT COUNT(*) AS total FROM `{structureRule_name}`"
    total = fetch_one(count_sql, None)['total']
    return jsonify({"list": structure_rules, "total": total})

    # page = request.form.get('currentPage', default=1, type=int)
    # print(page)
    # size = request.form.get('size', default=10, type=int)
    # offset = (page - 1) * size
    # projecname = request.form.get('projectname')
    # table_name = f"{projecname}BasicData"
    # fetch_sql = f"SELECT * FROM `{table_name}` LIMIT %s OFFSET %s"
    # basicDatas = fetch_all(fetch_sql,(size,offset))
    # count_sql = f"SELECT COUNT(*) AS total FROM `{table_name}`"
    # total = fetch_one(count_sql, None)['total']
    # print(basicDatas)
    # return jsonify({"list": basicDatas, "total": total})
    #
    # result = []
    # index = 1
    # for demand in demands:
    #     demandId = demand['parentD']
    #     demandName = id2name[demand['parentD']]
    #     expectedExpression = getExpectedExpression(demand)
    #     result.append({'id': index, 'demandId': demandId, 'demandName': demandName, 'expectedExpression': expectedExpression})
    #     index = index + 1
    #
    # print('get structure', result)
    # count_sql = f"SELECT COUNT(*) AS total FROM `{table_name}` WHERE {category_filter}"
    # total = fetch_one(count_sql, None)['total']
    #
    # return jsonify({"list": result, "total": total})


def getVerificationResult(projectname, expectedExpression, exid):
    expectedExpression = expectedExpression[1:-1] #(9,6,AggregationRelation)
    parts = expectedExpression.split(',')
    demandId = int(parts[0]) #子需求
    pId = int(parts[1]) #父需求
    relation = parts[2]

    #验证demandId对应的类型是否存在 需要读取
    result = ""
    demand_table_name = projectname + "Demand"
    interface_table_name = projectname + "Interface"
    agreement_table_name = projectname + "Agreement"
    entry_table_name = projectname + "EntryItem"
    sc_table_name = projectname + "SmartContract"

    searchdemandSql = f"SELECT * FROM `{demand_table_name}` WHERE id = %s"
    demandPid = fetch_one(searchdemandSql, (pId,))
    #print(demandPid)
    if demandPid['category'] == "智能合约":
        searchSCsql = f"SELECT * FROM `{sc_table_name}` WHERE demandId = %s"
        smartContractPid = fetch_one(searchSCsql, (pId, ))
        if smartContractPid:
            smartContractEntryItems = smartContractPid["smartContractEntryItems"]
            searchEntrysql = f"SELECT * FROM `{entry_table_name}` WHERE demandId = %s"
            entrySon = fetch_one(searchEntrysql, (demandId, ))
            if entrySon:
                entryItemName = entrySon["entryItemName"]
                if(entryItemName in smartContractEntryItems):
                    result += "需求" + str(pId) + "的性质" + exid + "验证通过!\n"
                else:
                    result += "需求" + str(pId) + "的性质" + exid + "对应类型不存在聚合关系规则，验证不通过\n"
            else:
                result += "需求" + str(pId) + "的性质" + exid + "对应类型不存在，验证不通过\n"
    elif demandPid['category'] == "业务":
        searchentrysql = f"SELECT * FROM `{entry_table_name}` WHERE demandId = %s"
        entryPid = fetch_one(searchentrysql, (pId,))
        if entryPid:
            entryItemAgreements = entryPid['entryItemAgreements']
            searchAgreesql = f"SELECT * FROM `{agreement_table_name}` WHERE demandId = %s"
            agreeson = fetch_one(searchAgreesql, (demandId, ))
            if agreeson:
                agreeName = agreeson["agreementName"]
                if(agreeName in entryItemAgreements):
                    result += "需求" + str(pId) + "的性质" + exid + "验证通过!\n"
                else:
                    result += "需求" + str(pId) + "的性质" + exid + "对应类型不存在聚合关系规则，验证不通过\n"
            else:
                result += "需求" + str(pId) + "的性质" + exid + "对应类型不存在，验证不通过\n"
    elif demandPid['category'] == "执行流程":
        searchAgree = f"SELECT * FROM `{agreement_table_name}` WHERE demandId = %s"
        agreePid = fetch_one(searchAgree, (pId,))
        if agreePid:
            agreementInterfaces = agreePid['agreementInterfaces']
            searchIntersql = f"SELECT * FROM `{interface_table_name}` WHERE demandId = %s"
            inetrson = fetch_one(searchIntersql, (demandId, ))
            if inetrson:
                intername = inetrson['interfaceName']
                if(intername in agreementInterfaces):
                    result += "需求" + str(pId) + "的性质" + exid + "验证通过!\n"
                else:
                    result += "需求" + str(pId) + "的性质" + exid + "对应类型不存在聚合关系规则，验证不通过\n"
            else:
                result += "需求" + str(pId) + "的性质" + exid + "对应类型不存在，验证不通过\n"

    # print(demandId)
    # print(pId)
    # print(relation)
    return result


def getParentVer(projectname, demandId):
    result = ""
    # expectedExpression = expectedExpression[1:-1] #(9,6,AggregationRelation)
    # parts = expectedExpression.split(',')
    # demandId = int(parts[0]) #子需求
    pId = int(demandId) #父需求

    demand_table_name = projectname + "Demand"
    interface_table_name = projectname + "Interface"
    agreement_table_name = projectname + "Agreement"
    entry_table_name = projectname + "EntryItem"
    sc_table_name = projectname + "SmartContract"

    searchdemandSql = f"SELECT * FROM `{demand_table_name}` WHERE id = %s"
    demandPid = fetch_one(searchdemandSql, (pId,))
    #print(demandPid)
    if demandPid['category'] == "智能合约":
        searchSCsql = f"SELECT * FROM `{sc_table_name}` WHERE demandId = %s"
        smartContractPid = fetch_one(searchSCsql, (pId,))
        if smartContractPid:  # 判断父需求是否有对应的类型
            result += "需求"+str(pId)+"验证通过!\n"
        else:
            result += "需求" + str(pId) + "缺少对应类型,验证不通过\n"
    elif demandPid['category'] == '业务':
        searchentrysql = f"SELECT * FROM `{entry_table_name}` WHERE demandId = %s"
        entryPid = fetch_one(searchentrysql, (pId,))
        if entryPid:
            result += "需求" + str(pId) + "验证通过!\n"
        else:
            result += "需求" + str(pId) + "缺少对应类型,验证不通过\n"
    elif demandPid['category'] == '执行流程':
        searchAgree = f"SELECT * FROM `{agreement_table_name}` WHERE demandId = %s"
        agreePid = fetch_one(searchAgree, (pId,))
        if agreePid:
            result += "需求" + str(pId) + "验证通过!\n"
        else:
            result += "需求" + str(pId) + "缺少对应类型,验证不通过\n"
    elif demandPid['category'] == '功能':
        searchIntersql = f"SELECT * FROM `{interface_table_name}` WHERE demandId = %s"
        interPid = fetch_one(searchIntersql, (pId,))
        if interPid:
            result += "需求" + str(pId) + "验证通过!\n"
        else:
            result += "需求" + str(pId) + "缺少对应类型,验证不通过\n"

    return result

def getSCverify(projectname, expectedExpression, exid):
    expectedExpression = expectedExpression[1:-1] #(9,6,AggregationRelation)
    parts = expectedExpression.split(',')
    demandId = int(parts[0]) #子需求
    pId = int(parts[1]) #父需求
    result = ""
    sc_table_name = projectname + "SmartContract"
    searchSCsql = f"SELECT * FROM `{sc_table_name}` WHERE demandId = %s"
    sc = fetch_one(searchSCsql, (demandId, ))
    if sc:
        result += "需求" + str(pId) + "的性质" + exid + "验证通过!\n"
    else:
        result += "需求" + str(demandId) + "缺少对应类型,验证不通过\n"
    return result


def getFunctionVerification(projectname, expectedExpression, exid):
    expectedExpression = expectedExpression[1:-1] #(59,25,MethodCorrelation)
    parts = expectedExpression.split(',')
    demandId = int(parts[0]) #子需求 方法 mapping
    pId = int(parts[1]) #父需求 功能 interface

    result = ""
    demand_table_name = projectname + "Demand"
    interface_table_name = projectname + "Interface"
    mapping_table_name = projectname + "Mapping"

    search_interface_sql = f"SELECT * FROM `{interface_table_name}` WHERE demandId = %s"
    interface = fetch_one(search_interface_sql, (pId, ))
    if interface:
        interfaceMethods = interface["interfaceMethods"]
        search_function_sql = f"SELECT * FROM `{mapping_table_name}` WHERE demandId = %s"
        function = fetch_one(search_function_sql, (demandId, ))
        if function:
            functionname = function["mappingName"]
            if functionname in interfaceMethods:
                result += "需求" + str(pId) + "的性质" + exid + "验证通过!\n"
            else:
                result += "需求" + str(pId) + "的性质" + exid + "对应类型不存在方法关联关系，验证不通过\n"
        else:
            result += "需求" + str(pId) + "的性质" + exid + "对应类型不存在，验证不通过\n"
    else:
        result += "需求" + str(pId) + "的性质" + exid + "对应类型不存在，验证不通过\n"

    return result



@structure_api_blueprint.route('/verifyStructure', methods=['POST'])
def verifyStructure():

    projectname = request.form.get('projectname')
    expectedExpression = request.form.get('expectedExpression')
    demandId = request.form.get('demandId')
    demandName = request.form.get('demandName')
    ids = request.form.get('id')
    print(expectedExpression)
    expectedExpression = expectedExpression[:-1]
    parts = expectedExpression.split(';')
    demandId = demandId[:-1]
    demandId = demandId.split(';')[0]
    ids = ids[:-1]
    ids = ids.split(';')
    result = ""
    result += "需求" + demandId + "验证开始:\n"

    #print(type(demandId[0]))
    if demandId == "0":
        result += "验证性质:\n"
        for i in range(len(parts)):
            verSCRe = getSCverify(projectname, parts[i], ids[i])
            result += verSCRe
    else:
        result += "验证需求:\n"
        parent_exist_ver = getParentVer(projectname, demandId)
        result += parent_exist_ver
        if "不通过" in parent_exist_ver:
            return jsonify({"result": result}), 200
        result += "验证性质:\n"
        for i in range(len(parts)):
            if "AggregationRelation" in parts[i]:
                part_ver = getVerificationResult(projectname, parts[i], ids[i])
                result += part_ver
            else:
                part_ver = getFunctionVerification(projectname, parts[i], ids[i])
                result += part_ver

    # for part in parts:
    #     part_ver = getVerificationResult(projectname, part, demandId)

    return jsonify({"result": result}), 200



def getAllVerificationResult(projectname, demandList):
    str_name = ''
    for demand in demandList:
        str_name += demand['demandName']
        str_name += '\n'
    return projectname + '\n' + str_name + '\n这\n里\n是\n结\n构\n正\n确\n性\n验\n证\n全部需求\n的\n结\n果，\n请\n查\n看\n是\n否\n是\n多\n行\n显\n示\n'


@structure_api_blueprint.route('/verifyAllStructure', methods=['POST'])
def verifyAll():
    projectname = request.form.get('projectname')
    demandList = request.form.get('demandList')
    demandList = json.loads(demandList)

    print('verifyStructure', projectname)

    result = "验证需求:\n"
    structureRule_table_name = projectname + "StructureRule"
    all_demandsId_sql = f"SELECT DISTINCT demandId FROM `{structureRule_table_name}`"
    all_demandIds = fetch_all(all_demandsId_sql, ())

    allRules_sql = f"SELECT * FROM `{structureRule_table_name}`"
    all_Rules = fetch_total(allRules_sql)

    expectedRes = ""
    SCverifyRes = ""
    for Rule in all_Rules:
        if Rule["demandId"] == 0:
            verRes = getSCverify(projectname, Rule['expectedExpression'], str(Rule['id']))
            SCverifyRes += verRes
        else:
            if "AggregationRelation" in Rule['expectedExpression']:
                verRes = getVerificationResult(projectname, Rule['expectedExpression'], str(Rule['id']))
            else:
                verRes = getFunctionVerification(projectname, Rule['expectedExpression'], str(Rule['id']))
            expectedRes += verRes

    demandRes = dict()
    for demandId in all_demandIds:
        print(demandId['demandId'])
        if demandId['demandId'] != 0:
            res = getParentVer(projectname, demandId['demandId'])
            demandRes[res] = None

    demandresstring = ""
    for key in demandRes:
        demandresstring += key

    result += SCverifyRes
    result += demandresstring
    result += "验证性质:\n"
    result += expectedRes


    return jsonify({"result": result}), 200
