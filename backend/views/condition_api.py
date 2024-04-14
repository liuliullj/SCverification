from flask import Blueprint, jsonify, request
from datetime import datetime
from db_connect import fetch_all, fetch_one, insert, delete, update
# 创建一个蓝图对象
condition_api_blueprint = Blueprint('condition_api', __name__)


@condition_api_blueprint.route('/getCondition', methods=['POST'])
def getConditionData():
    page = request.form.get('currentPage', default=1, type=int)
    print(page)
    size = request.form.get('size', default=10, type=int)
    offset = (page - 1) * size
    projecname = request.form.get('projectname')
    table_name = f"{projecname}Condition"
    fetch_sql = f"SELECT * FROM `{table_name}` LIMIT %s OFFSET %s"
    conditions = fetch_all(fetch_sql,(size,offset))
    count_sql = f"SELECT COUNT(*) AS total FROM `{table_name}`"
    total = fetch_one(count_sql, None)['total']
    print(conditions)
    return jsonify({"list": conditions, "total": total})


@condition_api_blueprint.route('/createCondition', methods=['POST'])
def createCondition():
    projectname = request.form.get('projectname')
    conditionName = request.form.get('conditionName')
    conditionBasicDataOne = request.form.get('conditionBasicDataOne')
    conditionBasicDataTwo = request.form.get('conditionBasicDataTwo')
    conditionOperator = request.form.get('conditionOperator')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    tablename = projectname + "Condition"
    get_id_sql = f"SELECT id FROM `{tablename}` ORDER BY id DESC LIMIT 1"
    row = fetch_one(get_id_sql, None)
    max_id = row['id'] if row else 0
    id_sql = f"ALTER TABLE `{tablename}` AUTO_INCREMENT = {max_id + 1}"
    update(id_sql, None)
    insert_sql = f"INSERT INTO `{tablename}` (conditionName, conditionBasicDataOne, conditionBasicDataTwo, conditionOperator, creattime) VALUES (%s, %s, %s, %s, %s)"
    insert(insert_sql, (conditionName, conditionBasicDataOne, conditionBasicDataTwo, conditionOperator, current_time))
    print("add condition!")
    return jsonify({"message": "条件类型创建成功"}), 200


@condition_api_blueprint.route('/updateCondition', methods=['POST'])
def updateCondition():
    projectname = request.form.get('projectname')
    conditionName = request.form.get('conditionName')
    conditionBasicDataOne = request.form.get('conditionBasicDataOne')
    conditionBasicDataTwo = request.form.get('conditionBasicDataTwo')
    conditionOperator = request.form.get('conditionOperator')
    id = request.form.get('id')
    table_name = projectname+"Condition"
    sql = f"UPDATE `{table_name}` SET `conditionName` = '{conditionName}', `conditionBasicDataOne` = '{conditionBasicDataOne}' , `conditionBasicDataTwo` = '{conditionBasicDataTwo}'  , `conditionOperator` = '{conditionOperator}' WHERE `id` = {id};"
    update(sql, None)
    print("update condition!")
    return jsonify({"message": "条件类型更新成功"}), 200


@condition_api_blueprint.route('/deleteCondition', methods=['POST'])
def deleteCondition():
    projectname = request.form.get('projectname')
    id = request.form.get('id')
    table_name = projectname+"Condition"
    sql = f"DELETE FROM `{table_name}` WHERE `id` = {id};"
    delete(sql, None)
    print("delete condition!")
    return jsonify({"message": "条件类型删除成功"}), 200
