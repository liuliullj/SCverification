import json

from flask import Blueprint, jsonify, request
import pymysql
import pymysql.cursors
from datetime import datetime
from db_connect import fetch_all, fetch_one, insert, delete, update

# 创建一个蓝图对象
structure_api_blueprint = Blueprint('structure_api', __name__)


def getExpectedExpression(demand):
    return 'expression'


def getVerificationResult(projectname, demandId, demandName, expectedExpression):
    return projectname + ' ' + demandName + '\n这\n里\n是\n结\n构\n正\n确\n性\n验\n证\n的\n结\n果，\n请\n查\n看\n是\n否\n是\n多\n行\n显\n示\n'


def getAllVerificationResult(projectname, demandList):
    str_name = ''
    for demand in demandList:
        str_name += demand['demandName']
        str_name += '\n'
    return projectname + '\n' + str_name + '\n这\n里\n是\n结\n构\n正\n确\n性\n验\n证\n全部需求\n的\n结\n果，\n请\n查\n看\n是\n否\n是\n多\n行\n显\n示\n'


@structure_api_blueprint.route('/getStructure', methods=['POST'])
def getStructureData():
    page = request.form.get('currentPage', default=1, type=int)
    print(page)
    size = request.form.get('size', default=10, type=int)
    offset = (page - 1) * size
    projecname = request.form.get('projectname')
    table_name = f"{projecname}Demand"

    category_filter = "category!='附加信息'"
    fetch_sql = f"SELECT * FROM `{table_name}` WHERE {category_filter} LIMIT %s OFFSET %s"
    demands = fetch_all(fetch_sql, (size, offset))
    result = []
    index = 1
    for demand in demands:
        demandId = demand['id']
        demandName = demand['demandname']
        expectedExpression = getExpectedExpression(demand)
        result.append({'id': index, 'demandId': demandId, 'demandName': demandName, 'expectedExpression': expectedExpression})
        index = index + 1
    print('get structure', result)
    return jsonify({"list": result, "total": len(result)})


@structure_api_blueprint.route('/verifyStructure', methods=['POST'])
def verifyStructure():
    projectname = request.form.get('projectname')
    expectedExpression = request.form.get('expectedExpression')
    demandId = request.form.get('demandId')
    demandName = request.form.get('demandName')

    print('verifyStructure', projectname + ' ' + expectedExpression + ' ' + demandId + ' ' + demandName)
    return jsonify({"result": getVerificationResult(projectname, demandId, demandName, expectedExpression)}), 200


@structure_api_blueprint.route('/verifyAllStructure', methods=['POST'])
def verifyAll():
    projectname = request.form.get('projectname')
    demandList = request.form.get('demandList')
    demandList = json.loads(demandList)

    print('verifyStructure', projectname)
    print(demandList)
    return jsonify({"result": getAllVerificationResult(projectname, demandList)}), 200
