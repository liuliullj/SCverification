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




def getAllVerificationResult(projectname, demandList):
    str_name = ''
    for demand in demandList:
        str_name += demand['demandName']
        str_name += '\n'
    return projectname + '\n' + str_name + '\n这\n里\n是\n结\n构\n正\n确\n性\n验\n证\n全部需求\n的\n结\n果，\n请\n查\n看\n是\n否\n是\n多\n行\n显\n示\n'


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
    count_sql = f"SELECT COUNT(*) AS total FROM `{table_name}` WHERE {category_filter}"
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


def getVerificationResult(projectname, expectedExpression, demandId):
    expectedExpression = expectedExpression[1:-1]
    parts = expectedExpression.split(',')
    demandId = int(parts[0])
    pId = int(parts[1])
    relation = parts[2]

    #验证demandId对应的类型是否存在
    result = "验证需求:\n"
    demandId = int(demandId)
    


    print(demandId)
    print(pId)
    print(relation)
    return relation

@structure_api_blueprint.route('/verifyStructure', methods=['POST'])
def verifyStructure():
    print("ehweew")

    projectname = request.form.get('projectname')
    expectedExpression = request.form.get('expectedExpression')
    demandId = request.form.get('demandId')
    demandName = request.form.get('demandName')
    print(expectedExpression)
    expectedExpression = expectedExpression[:-1]
    parts = expectedExpression.split(';')
    demandId = demandId[:-1]
    demandId = demandId.split(';')[0]
    result = ""
    result += "需求" + demandId + "验证开始:\n"
    for part in parts:
        part_ver = getVerificationResult(projectname, part, demandId)

    print('verifyStructure', projectname + ' ' + expectedExpression + ' ' + demandId + ' ' + demandName)
    return jsonify({"result": result}), 200


@structure_api_blueprint.route('/verifyAllStructure', methods=['POST'])
def verifyAll():
    projectname = request.form.get('projectname')
    demandList = request.form.get('demandList')
    demandList = json.loads(demandList)

    print('verifyStructure', projectname)
    print(demandList)
    return jsonify({"result": getAllVerificationResult(projectname, demandList)}), 200
