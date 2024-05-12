from flask import Blueprint, jsonify, request
import pymysql
import pymysql.cursors
from datetime import datetime
from db_connect import fetch_all, fetch_one, insert, delete, update

# 创建一个蓝图对象
mapping_api_blueprint = Blueprint('mapping_api', __name__)


@mapping_api_blueprint.route('/getMapping', methods=['POST'])
def getMappingData():
    page = request.form.get('currentPage', default=1, type=int)
    print(page)
    size = request.form.get('size', default=10, type=int)
    offset = (page - 1) * size
    projecname = request.form.get('projectname')
    table_name = f"{projecname}Mapping"
    fetch_sql = f"SELECT * FROM `{table_name}` LIMIT %s OFFSET %s"
    mappings = fetch_all(fetch_sql, (size, offset))
    count_sql = f"SELECT COUNT(*) AS total FROM `{table_name}`"
    total = fetch_one(count_sql, None)['total']
    print(mappings)
    return jsonify({"list": mappings, "total": total})


@mapping_api_blueprint.route('/getBasicDataInput', methods=['POST'])
def getBasicDataInput():
    projecname = request.form.get('projectname')
    table_name = f"{projecname}BasicData"
    fetch_sql = f"SELECT basicDataName as name FROM `{table_name}`"
    basicDataInputs = fetch_all(fetch_sql, ())
    print(basicDataInputs)
    return jsonify({"list": basicDataInputs})


@mapping_api_blueprint.route('/createMapping', methods=['POST'])
def createMapping():
    projectname = request.form.get('projectname')
    mappingName = request.form.get('mappingName')
    mappingInputBasicData = request.form.get('mappingInputBasicData')
    mappingOutputBasicData = request.form.get('mappingOutputBasicData')
    demandId = request.form.get('demandId')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    tablename = projectname + "Mapping"
    get_id_sql = f"SELECT id FROM `{tablename}` ORDER BY id DESC LIMIT 1"
    row = fetch_one(get_id_sql, None)
    max_id = row['id'] if row else 0
    id_sql = f"ALTER TABLE `{tablename}` AUTO_INCREMENT = {max_id + 1}"
    update(id_sql, None)
    insert_sql = f"INSERT INTO `{tablename}` (mappingName, mappingInputBasicData, mappingOutputBasicData, demandId, creatTime) VALUES (%s, %s, %s, %s, %s)"
    insert(insert_sql, (mappingName, mappingInputBasicData, mappingOutputBasicData, demandId, current_time))
    print("add mapping!")
    return jsonify({"message": "映射类型创建成功"}), 200


@mapping_api_blueprint.route('/updateMapping', methods=['POST'])
def updateMapping():
    projectname = request.form.get('projectname')
    mappingName = request.form.get('mappingName')
    mappingInputBasicData = request.form.get('mappingInputBasicData')
    mappingOutputBasicData = request.form.get('mappingOutputBasicData')
    demandId = request.form.get('demandId')
    id = request.form.get('id')
    table_name = projectname + "Mapping"
    sql = f"UPDATE `{table_name}` SET `mappingName` = '{mappingName}', `mappingInputBasicData` = '{mappingInputBasicData}', `mappingOutputBasicData` = '{mappingOutputBasicData}', `demandId` = '{demandId}' WHERE `id` = {id};"
    update(sql, None)
    print("update mapping!")
    return jsonify({"message": "映射类型更新成功"}), 200


@mapping_api_blueprint.route('/deleteMapping', methods=['POST'])
def deleteMapping():
    projectname = request.form.get('projectname')
    id = request.form.get('id')
    table_name = projectname + "Mapping"
    sql = f"DELETE FROM `{table_name}` WHERE `id` = {id};"
    delete(sql, None)
    print("delete mapping!")
    return jsonify({"message": "映射类型删除成功"}), 200
