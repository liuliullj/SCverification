import json

from flask import Blueprint, jsonify, request
import pymysql
import pymysql.cursors
from datetime import datetime
from db_connect import fetch_all, fetch_one, insert, delete, update

# 创建一个蓝图对象
call_api_blueprint = Blueprint('call_api', __name__)


def getVerificationResult(projectname, pathId, pathName, expectedExpression):
    return projectname + ' ' + pathName + '\n这\n里\n是\n调\n用\n正\n确\n性\n验\n证\n的\n结\n果，\n请\n查\n看\n是\n否\n是\n多\n行\n显\n示\n'


def getAllVerificationResult(projectname, pathList):
    str_name = ''
    for path in pathList:
        str_name += path['pathName']
        str_name += '\n'
    return projectname + '\n' + str_name + '\n这\n里\n是\n调\n用\n正\n确\n性\n验\n证\n全部路径\n的\n结\n果，\n请\n查\n看\n是\n否\n是\n多\n行\n显\n示\n'


@call_api_blueprint.route('/getCall', methods=['POST'])
def getCallData():
    page = request.form.get('currentPage', default=1, type=int)
    print(page)
    size = request.form.get('size', default=10, type=int)
    offset = (page - 1) * size
    projecname = request.form.get('projectname')
    table_name = f"{projecname}Design"

    fetch_sql = f"SELECT * FROM `{table_name}` LIMIT %s OFFSET %s"
    paths = fetch_all(fetch_sql, (size, offset))
    result = []
    index = 1
    for path in paths:
        pathId = path['id']
        pathName = path['pathname']
        pathExpression = path['expression']
        result.append({'id': index, 'pathId': pathId, 'pathName': pathName, 'pathExpression': pathExpression})
        index = index + 1
    print('get call', result)
    return jsonify({"list": result, "total": len(result)})


@call_api_blueprint.route('/verifyCall', methods=['POST'])
def verifyCall():
    projectname = request.form.get('projectname')
    pathExpression = request.form.get('pathExpression')
    pathId = request.form.get('pathId')
    pathName = request.form.get('pathName')

    print('verifyCall', projectname + ' ' + pathExpression + ' ' + pathId + ' ' + pathName)
    return jsonify({"result": getVerificationResult(projectname, pathId, pathName, pathExpression)}), 200


@call_api_blueprint.route('/verifyAllCall', methods=['POST'])
def verifyAll():
    projectname = request.form.get('projectname')
    pathList = request.form.get('pathList')
    pathList = json.loads(pathList)

    print('verifyCall', projectname)
    print(pathList)
    return jsonify({"result": getAllVerificationResult(projectname, pathList)}), 200
