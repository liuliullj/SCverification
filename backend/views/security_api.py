import json

from flask import Blueprint, jsonify, request
import  re
import pymysql
import pymysql.cursors
from datetime import datetime
from db_connect import fetch_all, fetch_one, insert, delete, update, fetch_total

# 创建一个蓝图对象
security_api_blueprint = Blueprint('security_api', __name__)

RRLEN = 100
def getVerificationResult(projectname, pathId, pathName, expectedExpression):
    return projectname + ' ' + pathName + '\n这\n里\n是\n合\n约\n安\n全\n性\n验\n证\n的\n结\n果，\n请\n查\n看\n是\n否\n是\n多\n行\n显\n示\n'


def getAllVerificationResult(projectname, pathList):
    str_name = ''
    for path in pathList:
        str_name += path['pathName']
        str_name += '\n'
    return projectname + '\n' + str_name + '\n这\n里\n是\n合\n约\n安\n全\n性\n验\n证\n全部路径\n的\n结\n果，\n请\n查\n看\n是\n否\n是\n多\n行\n显\n示\n'


@security_api_blueprint.route('/getSecurity', methods=['POST'])
def getSecurityData():
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
    print('get security', result)
    count_sql = f"SELECT COUNT(*) AS total FROM `{table_name}`"
    total = fetch_one(count_sql, None)['total']
    return jsonify({"list": result, "total": total})


def checkTimestampDependency(projectname, pathExpression):
    pattern = r'\[([^\]]*)\]'
    matches = re.findall(pattern, pathExpression)
    condition_table_name = f"{projectname}Condition"
    basicdata_table_name = f"{projectname}BasicData"
    # print(matches)
    for match in matches:
        items = match.split(";")
        for item in items:
            fetch_condition_sql = f"SELECT * FROM `{condition_table_name}` WHERE conditionName = %s"
            condition = fetch_one(fetch_condition_sql, (item, ))
            if condition:
                print(condition)
                conditionBasicDataOne = condition["conditionBasicDataOne"]
                print(conditionBasicDataOne)
                conditionBasicDataTwo = condition["conditionBasicDataTwo"]
                fetch_basicdata_sql = f"SELECT * FROM `{basicdata_table_name}` WHERE basicDataName = %s"
                basicdata1 = fetch_one(fetch_basicdata_sql, (conditionBasicDataOne, ))
                basicdata2 = fetch_one(fetch_basicdata_sql, (conditionBasicDataTwo, ))
                if basicdata1:
                    print(basicdata1)
                    if "timestamp" in basicdata1["basicDataExpression"]:
                        return item
                if basicdata2:
                    if "timestamp" in basicdata2["basicDataExpression"]:
                        return item
    return False

def checkDos(projectname, pathExpression):
    pattern = r'\[([^\]]*)\]'
    pathExpression = pathExpression.replace(" ", "").replace("\t", "")
    matches = re.findall(pattern, pathExpression)
    print(matches)
    if len(matches) % 2 == 1:
        return True
    i = 0
    while i < len(matches):
        con = matches[i]
        el = matches[i+1]
        if el.startswith("ELSE"):
            sub = "["+con+"];["+el+"]"
            if sub not in pathExpression:
                return True
        else:
            return True
        i += 2

    return False


def checkAuthoritycontrol(projectname, pathExpression):
    pattern = r'\[([^\]]*)\]'
    pathExpression = pathExpression.replace(" ", "").replace("\t", "")
    matches = re.findall(pattern, pathExpression)

    Demand_table_name = projectname+"Demand"
    Function_table_name = projectname+"Interface"
    Method_table_name = projectname+"Mapping"
    BasicData_table_name = projectname+"BasicData"
    patternFM = r"Function\d+\.Method\d+"
    pattern2int = r"Function(\d+)\.Method(\d+)"
    functions_methods = re.findall(patternFM, pathExpression)
    for i in range(len(functions_methods)):
        fm = functions_methods[i]
        print(fm)
        function_num, methods_num = re.search(pattern2int, fm).groups()
        fetch_method_sql = f"SELECT * FROM `{Method_table_name}` WHERE demandId = %s"
        method = fetch_one(fetch_method_sql, (methods_num,))
        if method:
            mappingInputBasicData = method["mappingInputBasicData"]
            mappingOutputBasicData = method["mappingOutputBasicData"]
            fetch_basicData_sql = f"SELECT * FROM `{BasicData_table_name}` WHERE basicDataName = %s"
            fetch_demand_sql = f"SELECT * FROM `{Demand_table_name}` WHERE id = %s"

            #如果outputdata本来就是条件类型的比较对象，则说明正在进行敏感数据的判断，不存在权限控制漏洞
            condition_table_name = projectname + "Condition"
            fetch_condition_sql_one = f"SELECT * FROM `{condition_table_name}` WHERE conditionBasicDataOne = %s"
            fetch_condition_sql_two = f"SELECT * FROM `{condition_table_name}` WHERE conditionBasicDataTwo = %s"
            condition_one = fetch_one(fetch_condition_sql_one, (mappingOutputBasicData, ))
            condition_two = fetch_one(fetch_condition_sql_two, (mappingOutputBasicData, ))
            if condition_one:
                return False
            if condition_two:
                return False

            inputdatas = mappingInputBasicData.replace(" ", "").replace("\t", "").split(";")
            for input in inputdatas:
                basicdata = fetch_one(fetch_basicData_sql, (input, ))
                if basicdata:
                    demandId = basicdata["demandId"]
                    demand = fetch_one(fetch_demand_sql, (demandId, ))
                    if demand:
                        if demand["category"] == "相关资产":
                            flag = True
                            for match in matches:
                                if fm in match:
                                    flag = False
                            if flag:
                                return fm

            outputdatas = mappingOutputBasicData.replace(" ", "").replace("\t", "").split(";")
            for output in outputdatas:
                basicdata = fetch_one(fetch_basicData_sql, (output,))
                if basicdata:
                    demandId = basicdata["demandId"]
                    demand = fetch_one(fetch_demand_sql, (demandId,))
                    if demand:
                        if demand["category"] == "相关资产":
                            flag = True
                            for match in matches:
                                if fm in match:
                                    flag = False
                            if flag:
                                return fm
    return False

@security_api_blueprint.route('/verifySecurity', methods=['POST'])
def verifySecurity():
    projectname = request.form.get('projectname')
    pathExpression = request.form.get('pathExpression')
    pathId = request.form.get('pathId')
    pathName = request.form.get('pathName')

    result = "路径"+pathName+"安全性验证:\n"
    whetherTimestamp = checkTimestampDependency(projectname, pathExpression)
    if isinstance(whetherTimestamp, str):
        result += "路径"+pathName+"中"+whetherTimestamp+"存在时间戳依赖漏洞，验证不通过！\n"

    whetherAuthoritycontrol = checkAuthoritycontrol(projectname, pathExpression)
    if isinstance(whetherAuthoritycontrol, str):
        result += "路径"+pathName+"中"+whetherAuthoritycontrol+"存在权限控制漏洞，验证不通过！\n"

    whetherDos = checkDos(projectname, pathExpression)
    if whetherDos:
        result += "路径"+pathName+"存在拒绝服务攻击漏洞，验证不通过！\n"

    if "不通过" not in result and not whetherDos:
        result += "路径"+pathName+"不存在安全漏洞，验证通过！\n"

    return jsonify({"result": result}), 200


@security_api_blueprint.route('/verifyAllSecurity', methods=['POST'])
def verifyAll():
    projectname = request.form.get('projectname')
    pathList = request.form.get('pathList')
    pathList = json.loads(pathList)

    path_table_name = projectname + "Design"
    fetch_path_sql = f"SELECT * FROM `{path_table_name}`"
    all_Paths = fetch_total(fetch_path_sql)
    result = "所有路径验证开始:\n"
    for path in all_Paths:
        pathresult = "路径"+path['pathname']+"安全性验证：\n"

        whetherTimestamp = checkTimestampDependency(projectname, path['expression'])
        if isinstance(whetherTimestamp, str):
            pathresult += "路径" + path['pathname'] + "中" + whetherTimestamp +"存在时间戳依赖漏洞，验证不通过！\n"

        whetherAuthoritycontrol = checkAuthoritycontrol(projectname, path['expression'])
        if isinstance(whetherAuthoritycontrol, str):
            pathresult += "路径" + path['pathname'] + "中"+whetherAuthoritycontrol + "存在权限控制漏洞，验证不通过！\n"

        whetherDos = checkDos(projectname, path['expression'])
        if whetherDos:
            pathresult += "路径" + path['pathname'] + "存在拒绝服务攻击漏洞，验证不通过！\n"

        if "不通过" not in result and not whetherDos:
            pathresult += "路径" + path['pathname'] + "不存在安全漏洞，验证通过！\n"

        result += pathresult
        result += '#'*RRLEN+"\n"

    return jsonify({"result": result}), 200


def checkAddress(basicdataname, basicDataValue):
    result = ""
    if len(basicDataValue) != 42:
        result = "基础数据类型"+basicdataname+"格式错误，存在短地址攻击漏洞！验证不通过！\n"
    elif not re.match(r'^0x[a-fA-F0-9]{40}$', basicDataValue):
        result = "基础数据类型" + basicdataname + "格式错误，存在短地址攻击漏洞！验证不通过！\n"
    else:
        result = "基础数据类型" + basicdataname + "验证通过！\n"
    return result


def string2dict(basicDataExpression):
    basicDataExpression = basicDataExpression.replace(" ", "").replace("\t", "")
    trimmed_str = basicDataExpression.strip("{}")
    key_value_pairs = trimmed_str.split(";")
    product_dict = {}
    for pair in key_value_pairs:
        if pair:  # 确保不处理空字符串
            key, value = pair.split(":")
            product_dict[key.strip()] = value.strip()
    return product_dict


def checkBasicdata(projectname,basicdataname, basicDataExpression, basicDataValues):
    basic_data_table = f"{projectname}BasicData"
    result = ""
    if basicDataExpression == "address":
        result = checkAddress(basicdataname, basicDataValues)
    if "mapping" in basicDataExpression:
        match1 = re.match(r'mapping\(([^→]*)→([^)]*)\)', basicDataExpression)
        stringex1 = match1.group(1)
        stringex2 = match1.group(2)
        match2 = re.match(r'mapping\(([^→]*)→([^)]*)\)', basicDataValues)
        if stringex1 == "address":
            result = checkAddress(basicdataname, match2.group(1))
        elif stringex2 == "address":
            result = checkAddress(basicdataname, match2.group(2))
        else:
            fetch_basic_expression = f"SELECT * FROM `{basic_data_table}` WHERE basicDataName = %s"
            expression1_sql = fetch_one(fetch_basic_expression, (stringex1, ))
            expression2_sql = fetch_one(fetch_basic_expression, (stringex2, ))
            if expression1_sql:
                if "address" in expression1_sql["basicDataExpression"]:
                    expression1 = expression1_sql["basicDataExpression"].replace(" ", "").replace("\t", "")
                    expression_dict = string2dict(expression1)
                    values_dict = string2dict(match2.group(1))
                    for key in expression_dict:
                        if expression_dict[key] == "address":
                            if key in values_dict.keys():
                                result = checkAddress(basicdataname, values_dict[key])
                                if "不通过" in result:
                                    return result
                            else:
                                result = "基础数据类型" + basicdataname + "键值对有误，请重新上传！\n"
                                return result
            if expression2_sql:
                if "address" in expression2_sql["basicDataExpression"]:
                    expression2 = expression2_sql["basicDataExpression"].replace(" ", "").replace("\t", "")
                    expression_dict = string2dict(expression2)
                    values_dict = string2dict(match2.group(2))
                    for key in expression_dict:
                        if expression_dict[key] == "address":
                            if key in values_dict.keys():
                                result = checkAddress(basicdataname, values_dict[key])
                                if "不通过" in result:
                                    return result
                            else:
                                result = "基础数据类型" + basicdataname + "键值对有误，请重新上传！\n"
                                return result
            result = "基础数据类型" + basicdataname + "验证通过！\n"
    if ":" in basicDataExpression and "{" in basicDataExpression and "}" in basicDataExpression:
        expression_dict = string2dict(basicDataExpression)
        values_dict = string2dict(basicDataValues)
        for key in expression_dict:
            if expression_dict[key] == "address":
                if key in values_dict.keys():
                    result = checkAddress(basicdataname, values_dict[key])
                    if "不通过" in result:
                        return result
                else:
                    result = "基础数据类型"+basicdataname+"键值对有误，请重新上传！\n"
                    return result
        result = "基础数据类型" + basicdataname + "验证通过！\n"

    return result



def checkUint(basicDataExpression, basicDataValues):
    pattern = r"uint(\d+)"
    match = re.search(pattern, basicDataExpression)
    if match:
        num = int(match.group(1))
    else:
        num = 256
    try:
        value_int = int(basicDataValues)
        max_int = 2**num - 1
        return 0 <= value_int <= max_int
    except:
        return "valueError"



def checkLimt(projectname,basicdataname, basicDataExpression, basicDataValues):
    basic_data_table = f"{projectname}BasicData"
    result = ""
    if "uint" in basicDataExpression and "mapping" not in basicDataExpression:
        flag = checkUint(basicDataExpression, basicDataValues)
        if isinstance(flag, str):
            result = "基础数据类型"+basicdataname+"值有误，请重新上传！\n"
        elif flag:
            result = "基础数据类型"+basicdataname+"验证通过！\n"
        else:
            result = "基础数据类型" + basicdataname + "存在数值溢出漏洞！验证不通过！\n"

    if ":" in basicDataExpression and "{" in basicDataExpression and "}" in basicDataExpression:
        expression_dict = string2dict(basicDataExpression)
        values_dict = string2dict(basicDataValues)
        for key in expression_dict:
            if "uint" in expression_dict[key]:
                if key in values_dict.keys():
                    flag = checkUint(expression_dict[key], values_dict[key])
                if isinstance(flag, str):
                    result = "基础数据类型" + basicdataname + "值有误，请重新上传！\n"
                    return result
                elif flag:
                    result = "基础数据类型" + basicdataname + "验证通过！\n"
                else:
                    result = "基础数据类型" + basicdataname + "存在数值溢出漏洞！验证不通过！\n"
                    return result
        result = "基础数据类型" + basicdataname + "验证通过！\n"

    if "mapping" in basicDataExpression:
        match1 = re.match(r'mapping\(([^→]*)→([^)]*)\)', basicDataExpression)
        stringex1 = match1.group(1)
        stringex2 = match1.group(2)
        match2 = re.match(r'mapping\(([^→]*)→([^)]*)\)', basicDataValues)
        if "uint" in stringex1 :
            flag = checkUint(stringex1, match2.group(1))
            if isinstance(flag, str):
                result = "基础数据类型" + basicdataname + "值有误，请重新上传！\n"
                return result
            elif flag:
                result = "基础数据类型" + basicdataname + "验证通过！\n"
            else:
                result = "基础数据类型" + basicdataname + "存在数值溢出漏洞！验证不通过！\n"
                return result

        elif "uint" in stringex2 :
            flag = checkUint(stringex2, match2.group(2))
            if isinstance(flag, str):
                result = "基础数据类型" + basicdataname + "值有误，请重新上传！\n"
                return result
            elif flag:
                result = "基础数据类型" + basicdataname + "验证通过！\n"
            else:
                result = "基础数据类型" + basicdataname + "存在数值溢出漏洞！验证不通过！\n"
                return result

        else:
            fetch_basic_expression = f"SELECT * FROM `{basic_data_table}` WHERE basicDataName = %s"
            expression1_sql = fetch_one(fetch_basic_expression, (stringex1, ))
            expression2_sql = fetch_one(fetch_basic_expression, (stringex2, ))
            if expression1_sql:
                if "uint" in expression1_sql["basicDataExpression"]:
                    expression1 = expression1_sql["basicDataExpression"].replace(" ", "").replace("\t", "")
                    expression_dict = string2dict(expression1)
                    values_dict = string2dict(match2.group(1))
                    for key in expression_dict:
                        if "uint" in expression_dict[key]:
                            if key in values_dict.keys():
                                flag = checkUint(expression_dict[key], values_dict[key])
                                if isinstance(flag, str):
                                    result = "基础数据类型" + basicdataname + "值有误，请重新上传！\n"
                                    return result
                                elif flag:
                                    result = "基础数据类型" + basicdataname + "验证通过！\n"
                                else:
                                    result = "基础数据类型" + basicdataname + "存在数值溢出漏洞！验证不通过！\n"
                                    return result
                            else:
                                result = "基础数据类型" + basicdataname + "键值对有误，请重新上传！\n"
                                return result
            if expression2_sql:
                if "uint" in expression2_sql["basicDataExpression"]:
                    expression2 = expression2_sql["basicDataExpression"].replace(" ", "").replace("\t", "")
                    expression_dict = string2dict(expression2)
                    values_dict = string2dict(match2.group(2))
                    for key in expression_dict:
                        if "uint" in expression_dict[key]:
                            if key in values_dict.keys():
                                flag = checkUint(expression_dict[key], values_dict[key])
                                if isinstance(flag, str):
                                    result = "基础数据类型" + basicdataname + "值有误，请重新上传！\n"
                                    return result
                                elif flag:
                                    result = "基础数据类型" + basicdataname + "验证通过！\n"
                                else:
                                    result = "基础数据类型" + basicdataname + "存在数值溢出漏洞！验证不通过！\n"
                                    return result
                            else:
                                result = "基础数据类型" + basicdataname + "键值对有误，请重新上传！\n"
                                return result
            result = "基础数据类型" + basicdataname + "验证通过！\n"

    return result

@security_api_blueprint.route('/uploadFileApi', methods=['POST'])
def uploadFile():
    projectname = request.form.get('projectname')
    keyvalues = request.form.get('keyvalues')
    keyvalues = keyvalues.replace(" ", "").replace("\t", "")
    keyvalues = keyvalues[:-1]
    values = keyvalues.split("#")

    table_name = f"{projectname}Values"
    check_table_exists = f"SHOW TABLES LIKE '{table_name}';"
    check = fetch_one(check_table_exists, None)
    if check:
        delete_sql = f"DELETE FROM `{table_name}`"
        delete(delete_sql, None)

    creat_Values_sql = f"""
                CREATE TABLE IF NOT EXISTS `{table_name}` (
                    `basicDataName` VARCHAR(255) NOT NULL,
                    `basicDataExpression` VARCHAR(255) NOT NULL,
                    `basicDataValue` VARCHAR(255) NOT NULL
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
                """
    insert(creat_Values_sql, None)

    basicdata_table_name = f"{projectname}BasicData"
    result = ""
    for item in values:
        eaches = item.split("$")
        if len(eaches)!= 3:
            return jsonify({"result": "表格数据有误，请重新上传！"}), 200
        if eaches[0] != "basicDataName":
            basicdataname = eaches[0]
            fetch_basicdata_sql = f"SELECT * FROM `{basicdata_table_name}` WHERE basicDataName = %s"
            basicDate = fetch_one(fetch_basicdata_sql, (basicdataname, ))
            if basicDate:
                basicDataExpression = basicDate["basicDataExpression"].replace(" ", "").replace("\t", "")
                updateExpression = eaches[1].replace(" ", "").replace("\t", "")
                if basicDataExpression != updateExpression:
                    result = basicdataname + "的表达式与定义不符，请重新上传！"
                    return jsonify({"result": result}), 200
                else:
                    #result += checkBasicdata(projectname, basicdataname, basicDataExpression, eaches[2])
                    result1 = checkBasicdata(projectname, basicdataname, basicDataExpression, eaches[2])
                    result2 = checkLimt(projectname, basicdataname, basicDataExpression, eaches[2])
                    if "验证通过" in result1 and "验证通过" in result2:
                        result += "基础数据类型"+basicdataname+"验证通过！\n"
                    elif "验证通过" in result1 and "验证通过" not in result2 and result2 != "":
                        result += result2
                    elif "验证通过" in result2 and "验证通过" not in result1 and result1 != "":
                        result += result1
                    else:
                        result += result1
                        result += result2
            else:
                result = "不存在名为"+basicdataname+"的基础数据类型，请重新上传！"
                return jsonify({"result": result}), 200

    return jsonify({"result": result}), 200