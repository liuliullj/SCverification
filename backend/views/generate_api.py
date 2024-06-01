import json
import re

from flask import Blueprint, jsonify, request
import pymysql
import pymysql.cursors
from datetime import datetime
from db_connect import fetch_all, fetch_one, insert, delete, update, fetch_total

# 创建一个蓝图对象
generate_api_blueprint = Blueprint('generate_api', __name__)



def generateBasicData(basicData):
    basicDataexpression = basicData["basicDataExpression"]
    basicDataexpression = basicDataexpression.replace(" ", "").replace("\t", "")
    result = ""
    if "mapping" in basicDataexpression:
        match1 = re.match(r'mapping\(([^→]*)→([^)]*)\)', basicDataexpression)
        stringex1 = match1.group(1)
        stringex2 = match1.group(2)
        result =basicData["basicDataName"]+" : mapping("+stringex1+"=>"+stringex2+")\n"
    elif "{" in basicDataexpression and "," in basicDataexpression and ";" not in basicDataexpression:
        basicDataexpression = basicDataexpression.replace("{", "").replace("}", "")
        items = basicDataexpression.split(",")
        result = basicData["basicDataName"] + " : "
        for item in items:
            result += item + " | "
        result = result[:-2]
        result += "\n"
    elif "{" in basicDataexpression and ":" in basicDataexpression and ";" in basicDataexpression:
        trimmed_str = basicDataexpression.strip("{}")
        key_value_pairs = trimmed_str.split(";")
        result  = "addition " + basicData["basicDataName"] + "{\n"
        for key_value_pair in key_value_pairs:
            result += "    " + key_value_pair + ";\n"
        result = result[:-2]
        result += "\n}\n"
    return result


def generateCondition(projectname, condition):
    result = ""
    conditionBasicDataOne = condition["conditionBasicDataOne"]
    conditionBasicDataTwo = condition["conditionBasicDataTwo"]
    conditionOperator = condition["conditionOperator"]
    if conditionOperator == "=":
        if conditionBasicDataOne == "true":
            result = conditionBasicDataTwo
        elif conditionBasicDataOne == "false":
            result = "!"+conditionBasicDataTwo
        elif conditionBasicDataTwo == "true":
            result = conditionBasicDataOne
        elif conditionBasicDataTwo == "false":
            result = "!"+conditionBasicDataOne
    else:
        result = conditionBasicDataOne + conditionOperator + conditionBasicDataTwo

    forcondition = ""
    mapping_table_name = f"{projectname}Mapping"
    search_mapping_sql = f"SELECT * FROM `{mapping_table_name}` WHERE mappingOutputBasicData = %s"
    mapping_one = fetch_one(search_mapping_sql, (conditionBasicDataOne,))
    if mapping_one:
        forcondition += conditionBasicDataOne + " = " + mapping_one["mappingName"]+"("+mapping_one["mappingInputBasicData"]+")\n"
    mapping_two = fetch_one(search_mapping_sql, (conditionBasicDataTwo,))
    if mapping_two:
        forcondition += conditionBasicDataTwo + " = " + mapping_two["mappingName"] + "(" + mapping_two["mappingInputBasicData"] + ")\n"

    return forcondition, result

def generateAgree(projectname,agree):
    interface_table_name = f"{projectname}Interface"
    condition_table_name = f"{projectname}Condition"
    mapping_table_name = f"{projectname}Mapping"
    demand_table_name = f"{projectname}Demand"
    basicdata_table_name = f"{projectname}BasicData"

    #conditionsitem中存储比较变量，后续函数表达不用加入该agree
    fetch_condition_sql = f"SELECT * FROM `{condition_table_name}`"
    all_conditions = fetch_total(fetch_condition_sql)
    conditionitems = ""
    for condition in all_conditions:
        conditionitems += condition["conditionBasicDataOne"]+";"
        conditionitems += condition["conditionBasicDataTwo"]+";"

    #assets中存储资产，用于判断后续是否为涉及资产的操作
    asset_demands_sql = f"SELECT * FROM `{demand_table_name}` WHERE category = %s"
    asset_demands = fetch_all(asset_demands_sql, ("相关资产",))
    assets = ""
    for asset in asset_demands:
        demandID = asset["id"]
        search_basicdata_sql = f"SELECT * FROM `{basicdata_table_name}` WHERE demandId = %s"
        basicdata = fetch_one(search_basicdata_sql, (demandID, ))
        if basicdata:
            assets += basicdata["basicDataName"]+';'

    WHERE = agree["agreementName"] +"("
    WHILE = agree["agreementName"] +"("
    INPUT = set()
    agreementInterfaces = agree["agreementInterfaces"].replace(" ", "").replace("\t", "")
    interfaces = agreementInterfaces.split(";")
    for item in interfaces:
        search_interface_sql = f"SELECT * FROM `{interface_table_name}` WHERE interfaceName = %s"
        interface = fetch_one(search_interface_sql, (item,))
        if interface:
            interfaceMethods = interface["interfaceMethods"].replace(" ", "").replace("\t", "")
            methods = interfaceMethods.split(";")
            for methodname in methods:
                search_method_sql = f"SELECT * FROM `{mapping_table_name}` WHERE mappingName = %s"
                method = fetch_one(search_method_sql, (methodname,))
                if method:
                    mappingInputBasicData = method["mappingInputBasicData"].replace(" ", "").replace("\t", "")
                    mappingOutputBasicData = method["mappingOutputBasicData"].replace(" ", "").replace("\t", "")


                    inputdatas = mappingInputBasicData.split(";")
                    flaginput = False
                    for inputdata in inputdatas:
                        if inputdata in assets:
                            flaginput = True

                    outputdatas = mappingOutputBasicData.split(";")
                    flagOutput = False
                    for output in outputdatas:
                        if output in conditionitems:
                            flagOutput = True
                        if output in assets:
                            flaginput = True


                    if not flagOutput and not flaginput:
                        WHERE += methodname+";"
                        INPUT = INPUT.union(set(inputdatas))
                    if not flagOutput and flaginput:
                        WHILE += methodname+";"
                        INPUT = INPUT.union(set(inputdatas))

    WHERE = WHERE[:-1]
    WHILE = WHILE[:-1]
    WHERE += ")"
    WHILE += ")"
    return INPUT, WHERE, WHILE


def generateSmartContract(projectname, demandId, scids):
    demand_table_name = f"{projectname}Demand"
    design_table_name = f"{projectname}Design"
    basicdata_table_name = f"{projectname}BasicData"
    mapping_table_name = f"{projectname}Mapping"
    interface_table_name = f"{projectname}Interface"
    condition_table_name = f"{projectname}Condition"
    agreement_table_name = f"{projectname}Agreement"
    entry_table_name = f"{projectname}EntryItem"
    smartcontract_table_name = f"{projectname}SmartContract"

    result = ""
    fetch_basicData_sql = f"SELECT * FROM `{basicdata_table_name}`"
    all_basicDatas = fetch_total(fetch_basicData_sql)
    for basicData in all_basicDatas:
        if basicData["demandId"] == demandId:
            result += generateBasicData(basicData)
        elif str(basicData["demandId"]) not in scids:
            print(basicData["demandId"])#96
            searchdemandSql = f"SELECT * FROM `{demand_table_name}` WHERE id = %s"
            demand = fetch_one(searchdemandSql, (basicData["demandId"],))
            if demand["parentD"] == demandId:
                result += generateBasicData(basicData)

    fetch_entry_sql = f"SELECT * FROM `{entry_table_name}`"
    all_entrys = fetch_total(fetch_entry_sql)
    i = 1
    for entry in all_entrys:
        entrydemandId = entry["demandId"]
        searchdemandSql = f"SELECT * FROM `{demand_table_name}` WHERE id = %s"
        demand = fetch_one(searchdemandSql, (entrydemandId,))
        if demand:
            if demand["parentD"] == demandId: #该entry属于demandId对应的智能合约
                entryItemConditions = entry["entryItemConditions"].replace(" ", "").replace("\t", "")
                entryItemAgreements = entry["entryItemAgreements"].replace(" ", "").replace("\t", "")

                conditions = entryItemConditions.split(";")
                conditionlanguage = ""
                forconditions = ""
                for item in conditions:
                    searchconditionsql = f"SELECT * FROM `{condition_table_name}` WHERE conditionName = %s"
                    condition = fetch_one(searchconditionsql, (item, ))
                    if condition:
                        forcondition, flag = generateCondition(projectname, condition)
                        if forcondition not in forconditions:
                            forconditions += forcondition
                        conditionlanguage += flag
                        conditionlanguage += " and "
                conditionlanguage = conditionlanguage[:-5]
                conditionlanguage += "\n"
                result += forconditions  #把条件比较所需参数转换后写入

                aggreements = entryItemAgreements.split(";")
                INPUT = set()
                WHERE = ""
                WHILE = ""
                for item in aggreements:
                    searchagreesql = f"SELECT * FROM `{agreement_table_name}` WHERE agreementName = %s"
                    agree = fetch_one(searchagreesql, (item, ))
                    if agree:
                        INPUTtemp, WHEREtemp, WHILEtemp = generateAgree(projectname,agree)
                        INPUT = INPUT.union(INPUTtemp)
                        WHERE += WHEREtemp+ ";"
                        if "(" in WHILEtemp:
                            WHILE += WHILEtemp + ";"

                inputdata = ""
                for k in INPUT:
                    if k != "Null":
                        inputdata += k + ";"
                inputdata = inputdata[:-1]
                term = "Terms No" + str(i) + " :  Users can " + entry["entryItemName"] + "("+inputdata+")\n"
                term += "    WHEN  " + conditionlanguage
                if WHILE!="":
                    term += "    WHILE  " + WHILE +"\n"
                term += "    WHERE  " + WHERE + "\n"
                result += term
                i += 1


    return result

@generate_api_blueprint.route('/generateApi', methods=['POST'])
def generateApi():
    projectname = request.form.get('projectname')
    demand_table_name = f"{projectname}Demand"
    design_table_name = f"{projectname}Design"
    basicdata_table_name = f"{projectname}BasicData"
    mapping_table_name = f"{projectname}Mapping"
    interface_table_name = f"{projectname}Interface"
    condition_table_name = f"{projectname}Condition"
    agreement_table_name = f"{projectname}Agreement"
    entry_table_name = f"{projectname}EntryItem"
    smartcontract_table_name = f"{projectname}SmartContract"

    result = ""
    sc_demands_sql = f"SELECT * FROM `{demand_table_name}` WHERE category = %s"
    sc_demands = fetch_all(sc_demands_sql, ("智能合约",))
    scids = ""
    for sc in sc_demands:
        scids += str(sc["id"]) + ";"

    fetch_demand_sql = f"SELECT * FROM `{demand_table_name}`"
    all_demands = fetch_total(fetch_demand_sql)
    for demand in all_demands:
        if demand["category"] == "智能合约":
            temp = projectname + demand["demandname"] + "元语言如下：\n"
            demandId = demand["id"]
            temp += generateSmartContract(projectname, demandId, scids)
            result += temp
            result += "-" * 140 +"\n"

    return jsonify({"result": result}), 200