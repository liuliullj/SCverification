from flask import Blueprint, jsonify, request
import pymysql
import pymysql.cursors
from datetime import datetime
from db_connect import fetch_all, fetch_one, insert, delete, update
# 创建一个蓝图对象
entryItem_api_blueprint = Blueprint('entryItem_api', __name__)

@entryItem_api_blueprint.route('/getEntryItem', methods=['POST'])
def getEntryItemData():
    page = request.form.get('currentPage', default=1, type=int)
    print(page)
    size = request.form.get('size', default=10, type=int)
    offset = (page - 1) * size
    projecname = request.form.get('projectname')
    table_name = f"{projecname}EntryItem"
    fetch_sql = f"SELECT * FROM `{table_name}` LIMIT %s OFFSET %s"
    entryItems = fetch_all(fetch_sql,(size,offset))
    count_sql = f"SELECT COUNT(*) AS total FROM `{table_name}`"
    total = fetch_one(count_sql, None)['total']
    print(entryItems)
    return jsonify({"list": entryItems, "total": total})


@entryItem_api_blueprint.route('/createEntryItem', methods=['POST'])
def createEntryItem():
    projectname = request.form.get('projectname')
    entryItemName = request.form.get('entryItemName')
    entryItemConditions = request.form.get('entryItemConditions')
    entryItemAgreements = request.form.get('entryItemAgreements')
    demandId = request.form.get('demandId')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    tablename = projectname + "EntryItem"
    get_id_sql = f"SELECT id FROM `{tablename}` ORDER BY id DESC LIMIT 1"
    row = fetch_one(get_id_sql, None)
    max_id = row['id'] if row else 0
    id_sql = f"ALTER TABLE `{tablename}` AUTO_INCREMENT = {max_id + 1}"
    update(id_sql, None)
    insert_sql = f"INSERT INTO `{tablename}` (entryItemName, entryItemConditions, entryItemAgreements, demandId, creatTime) VALUES (%s, %s, %s, %s, %s)"
    insert(insert_sql, (entryItemName, entryItemConditions, entryItemAgreements, demandId, current_time))
    print("add entryItem!")
    return jsonify({"message": "映射类型创建成功"}), 200


@entryItem_api_blueprint.route('/updateEntryItem', methods=['POST'])
def updateEntryItem():
    projectname = request.form.get('projectname')
    entryItemName = request.form.get('entryItemName')
    entryItemConditions = request.form.get('entryItemConditions')
    entryItemAgreements = request.form.get('entryItemAgreements')
    demandId = request.form.get('demandId')
    id = request.form.get('id')
    table_name = projectname+"EntryItem"
    sql = f"UPDATE `{table_name}` SET `entryItemName` = '{entryItemName}', `entryItemConditions` = '{entryItemConditions}', `entryItemAgreements` = '{entryItemAgreements}', `demandId` = '{demandId}' WHERE `id` = {id};"
    update(sql, None)
    print("update entryItem!")
    return jsonify({"message": "映射类型更新成功"}), 200


@entryItem_api_blueprint.route('/deleteEntryItem', methods=['POST'])
def deleteEntryItem():
    projectname = request.form.get('projectname')
    id = request.form.get('id')
    table_name = projectname+"EntryItem"
    sql = f"DELETE FROM `{table_name}` WHERE `id` = {id};"
    delete(sql, None)
    print("delete entryItem!")
    return jsonify({"message": "映射类型删除成功"}), 200


@entryItem_api_blueprint.route('/getEntryItemCondition', methods=['POST'])
def getEntryItemCondition():
    projecname = request.form.get('projectname')
    table_name = f"{projecname}Condition"
    fetch_sql = f"SELECT conditionName as name FROM `{table_name}`"
    dataInputs = fetch_all(fetch_sql, ())
    print(dataInputs)
    return jsonify({"list": dataInputs})


@entryItem_api_blueprint.route('/getEntryItemAgreement', methods=['POST'])
def getEntryItemAgreement():
    projecname = request.form.get('projectname')
    table_name = f"{projecname}Agreement"
    fetch_sql = f"SELECT agreementName as name FROM `{table_name}`"
    dataInputs = fetch_all(fetch_sql, ())
    print(dataInputs)
    return jsonify({"list": dataInputs})
