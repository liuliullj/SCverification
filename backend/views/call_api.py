import json
import re

from flask import Blueprint, jsonify, request
import pymysql
import pymysql.cursors
from datetime import datetime
from db_connect import fetch_all, fetch_one, insert, delete, update, fetch_total

# 创建一个蓝图对象
call_api_blueprint = Blueprint('call_api', __name__)

RRLEN = 140

def getVerificationResult(projectname, pathId, pathName, pathExpression):
    pattern = r"Function\d+\.Method\d+"
    pattern2int = r"Function(\d+)\.Method(\d+)"
    functions_methods = re.findall(pattern, pathExpression)
    print(functions_methods)
    result = ""
    Demand_table_name = projectname+"Demand"
    Function_table_name = projectname+"Interface"
    Method_table_name = projectname+"Mapping"

    #路径只包含单个节点的处理
    if len(functions_methods) == 1:
        fm = functions_methods[0]
        function_num, methods_num = re.search(pattern2int, fm).groups()
        fetch_demand_sql = f"SELECT * FROM `{Demand_table_name}` WHERE id = %s"
        demand_function = fetch_one(fetch_demand_sql, (function_num,))
        demand_method = fetch_one(fetch_demand_sql, (methods_num,))
        if demand_function['category'] != "功能":
            result += "需求"+function_num+"对应类型不为功能，路径有误!\n"
            result += "路径"+pathName+"可调用关系验证未通过！\n"
            return result
        if demand_method['category'] != "方法":
            result += "需求"+methods_num+"对应类型不为方法，路径有误!\n"
            result += "路径"+pathName+"可调用关系验证未通过！\n"
            return result
        fetch_function_sql = f"SELECT * FROM `{Function_table_name}` WHERE demandId = %s"
        fetch_method_sql = f"SELECT * FROM `{Method_table_name}` WHERE demandId = %s"
        function = fetch_one(fetch_function_sql, (function_num,))
        method = fetch_one(fetch_method_sql, (methods_num,))
        if function:
            if method:
                if method['mappingName'] not in function['interfaceMethods']:
                    result += "Method" + methods_num + "不是Function" + function_num + "的方法！\n"
                    result += "路径" + pathName + "可调用关系验证未通过！\n"
                    return result
                else:
                    result += "建模中Method" + methods_num + "是Function" + function_num + "的方法,具有可调用关系！\n"
            else:
                result += "需求" + methods_num + "方法缺少对应类型设计！\n"
                result += "路径" + pathName + "可调用关系验证未通过！\n"
                return result
        else:
            result += "需求"+function_num+"功能缺少对应类型设计！\n"
            result += "路径"+pathName+"可调用关系验证未通过！\n"
            return result



    for i in range(len(functions_methods)-1):
        result += "节点"+functions_methods[i]+"与"+functions_methods[i+1]+"调用关系验证:\n"
        fm = functions_methods[i]
        function_num_pre, methods_num_pre = re.search(pattern2int, fm).groups()
        function_num_next, methods_num_next = re.search(pattern2int, functions_methods[i+1]).groups()
        #判断是否为方法/功能
        fetch_demand_sql = f"SELECT * FROM `{Demand_table_name}` WHERE id = %s"
        demand_function_pre = fetch_one(fetch_demand_sql, (function_num_pre,))
        demand_method_pre = fetch_one(fetch_demand_sql, (methods_num_pre, ))
        demand_function_next = fetch_one(fetch_demand_sql, (function_num_next, ))
        demand_method_next = fetch_one(fetch_demand_sql, (methods_num_next, ))
        if demand_function_pre['category'] != "功能":
            result += "需求"+function_num_pre+"对应类型不为功能，路径有误!\n"
            result += "路径"+pathName+"可调用关系验证未通过！\n"
            return result
        if demand_function_next['category'] != "功能":
            result += "需求"+function_num_next+"对应类型不为功能，路径有误!\n"
            result += "路径"+pathName+"可调用关系验证未通过！\n"
            return result
        if demand_method_pre['category'] != "方法":
            result += "需求"+methods_num_pre+"对应类型不为方法，路径有误!\n"
            result += "路径"+pathName+"可调用关系验证未通过！\n"
            return result
        if demand_method_next['category'] != "方法":
            result += "需求"+methods_num_next+"对应类型不为方法，路径有误!\n"
            result += "路径"+pathName+"可调用关系验证未通过！\n"
            return result

        fetch_function_sql = f"SELECT * FROM `{Function_table_name}` WHERE demandId = %s"
        fetch_method_sql = f"SELECT * FROM `{Method_table_name}` WHERE demandId = %s"
        function_pre = fetch_one(fetch_function_sql, (function_num_pre, ))
        function_next = fetch_one(fetch_function_sql, (function_num_next, ))
        if function_pre:
            if function_next:
                method_pre = fetch_one(fetch_method_sql, (methods_num_pre, ))
                method_next = fetch_one(fetch_method_sql, (methods_num_next, ))
                if method_pre:
                    if method_next:

                        method_name_pre = method_pre['mappingName']
                        method_name_next = method_next['mappingName']
                        if method_name_pre not in function_pre['interfaceMethods']:
                            result += "Method"+methods_num_pre+"不是Function"+function_num_pre+"的方法！\n"
                            result += "路径" + pathName + "可调用关系验证未通过！\n"
                            return result
                        if method_name_next not in function_next['interfaceMethods']:
                            result += "Method"+methods_num_next+"不是Function"+function_num_next+"的方法！\n"
                            result += "路径" + pathName + "可调用关系验证未通过！\n"
                            return result
                        if function_num_pre == function_num_next:
                            call_re = "建模中Method"+methods_num_pre+"是Function"+function_num_pre+"的方法,"+"Method"+methods_num_next+"是Function"+function_num_next+"的方法，具有可调用关系!\n"
                            result += call_re
                            result += '-'*RRLEN+"\n"
                        else:
                            if function_next['interfaceName'] in function_pre['interfaceMember']:
                                call_re = "建模中Method" + methods_num_pre + "是Function" + function_num_pre + "的方法,"+"Method" + methods_num_next + "是Function" + function_num_next + "的方法,Function"+function_num_next+"是Function"+function_num_pre+"的成员类型，具有可调用关系！\n"
                                # result += "建模中Method" + methods_num_pre + "是Function" + function_num_pre + "的方法,"
                                # result += "Method" + methods_num_next + "是Function" + function_num_next + "的方法,Function"+function_num_next+"是Function"+function_num_pre+"的成员类型，具有可调用关系！\n"
                                result += call_re
                                result += '-' * RRLEN+"\n"
                            else:
                                print(function_next['interfaceName'])
                                print(function_pre['interfaceMember'])
                                result += "建模中Method" + methods_num_pre + "是Function" + function_num_pre + "的方法,"
                                result += "Method" + methods_num_next + "是Function" + function_num_next + "的方法,Function"+function_num_next+"不是Function"+function_num_pre+"的成员类型，不具备可调用关系！\n"
                                result += "路径" + pathName + "可调用关系验证未通过！\n"
                                return result

                    else:
                        result += "需求" + methods_num_next + "方法缺少对应类型设计！\n"
                        result += "路径" + pathName + "可调用关系验证未通过！\n"
                        return result
                else:
                    result += "需求" + methods_num_pre + "方法缺少对应类型设计！\n"
                    result += "路径" + pathName + "可调用关系验证未通过！\n"
                    return result
            else:
                result += "需求" + function_num_next + "功能缺少对应类型设计！\n"
                result += "路径" + pathName + "可调用关系验证未通过！\n"
                return result
        else:
            result += "需求"+function_num_pre+"功能缺少对应类型设计！\n"
            result += "路径"+pathName+"可调用关系验证未通过！\n"
            return result

    result += "路径"+pathName+"可调用关系验证通过！\n"

    return result



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
        result.append({'id': pathId, 'pathId': pathId, 'pathName': pathName, 'pathExpression': pathExpression})
        index = index + 1
    print('get call', result)
    count_sql = f"SELECT COUNT(*) AS total FROM `{table_name}`"
    total = fetch_one(count_sql, None)['total']
    return jsonify({"list": result, "total": total})



def getVerifyTwoPath(projectname, pathId, pathName, pathExpression):
    pathExpression = pathExpression.replace(" ", "").replace("\t", "")
    # 使用正则表达式找到所有中括号内的内容
    matches = re.findall(r'\[([^]]+)\]', pathExpression)

    result = "路径"+pathName+"验证开始:\n"
    # 确保找到了两个匹配的中括号内容
    if len(matches) == 2:
        string2, string3 = matches
        # 找到第一个中括号的位置，将之前的内容作为 string1
        first_bracket_index = pathExpression.find('[')
        string1 = pathExpression[:first_bracket_index]

        # 组合 string1 + string2 和 string1 + string3
        combined1 = string1 + string2
        combined2 = string1 + string3

        result1 = getVerificationResult(projectname, pathId, pathName, combined1)
        result2 = getVerificationResult(projectname, pathId, pathName, combined2)
        result += "路径"+pathName+"的分支"+combined1+"验证：\n"
        result += '-' * RRLEN + "\n"
        result += result1
        result += "路径"+pathName+"的分支"+combined2+"验证：\n"
        result += '-' * RRLEN + "\n"
        result += result2

    else:
        result += "路径"+pathName+"不符合路径表达式规范，验证失败！\n"
    return result


@call_api_blueprint.route('/verifyCall', methods=['POST'])
def verifyCall():
    projectname = request.form.get('projectname')
    pathExpression = request.form.get('pathExpression')
    pathId = request.form.get('pathId')
    pathName = request.form.get('pathName')

    print("pathexpression", pathExpression)
    print('verifyCall', projectname + ' ' + pathExpression + ' ' + pathId + ' ' + pathName)
    return jsonify({"result": getVerifyTwoPath(projectname, pathId, pathName, pathExpression)}), 200


def getAllVerificationResult(projectname, pathList):
    path_table_name = projectname + "Design"
    fetch_path_sql = f"SELECT * FROM `{path_table_name}`"
    all_Paths = fetch_total(fetch_path_sql)
    result = "所有路径验证开始:\n"
    for path in all_Paths:
        result += getVerifyTwoPath(projectname, path['id'], path['pathname'], path['expression'])
        result += '#'*RRLEN+"\n"
    return result

    # str_name = ''
    # for path in pathList:
    #     str_name += path['pathName']
    #     str_name += '\n'
    # return projectname + '\n' + str_name + '\n这\n里\n是\n调\n用\n正\n确\n性\n验\n证\n全部路径\n的\n结\n果，\n请\n查\n看\n是\n否\n是\n多\n行\n显\n示\n'

@call_api_blueprint.route('/verifyAllCall', methods=['POST'])
def verifyAll():
    projectname = request.form.get('projectname')
    pathList = request.form.get('pathList')
    pathList = json.loads(pathList)

    print('verifyCall', projectname)
    print(pathList)

    return jsonify({"result": getAllVerificationResult(projectname, pathList)}), 200
