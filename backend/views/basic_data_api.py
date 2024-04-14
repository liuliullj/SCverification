from flask import Blueprint, jsonify, request
import pymysql
import pymysql.cursors
from datetime import datetime
from db_connect import fetch_all, fetch_one, insert, delete, update
# 创建一个蓝图对象
basic_data_api_blueprint = Blueprint('basic_data_api', __name__)

# 从原始文件中复制db和cursor的定义到这里，或者使用其他方式导入它们
# db = pymysql.connect(host="127.0.0.1", user="root", password="1999511510", database="database_learn", port=3306)
# cursor = db.cursor()

# @basic_data_api_blueprint.route('/getProjectName', methods=['GET'])
# def getProjectName():
#     sql = "SELECT name FROM projectmanagement"
#     result = fetch_all(sql, None)
#     names = [row['name'] for row in result]
#     print(names)
#     return jsonify(names)

@basic_data_api_blueprint.route('/getBasicData', methods=['POST'])
def getBasicDataData():
    page = request.form.get('currentPage', default=1, type=int)
    print(page)
    size = request.form.get('size', default=10, type=int)
    offset = (page - 1) * size
    projecname = request.form.get('projectname')
    table_name = f"{projecname}BasicData"
    fetch_sql = f"SELECT * FROM `{table_name}` LIMIT %s OFFSET %s"
    basicDatas = fetch_all(fetch_sql,(size,offset))
    count_sql = f"SELECT COUNT(*) AS total FROM `{table_name}`"
    total = fetch_one(count_sql, None)['total']
    print(basicDatas)
    return jsonify({"list": basicDatas, "total": total})


@basic_data_api_blueprint.route('/createBasicData', methods=['POST'])
def createBasicData():
    projectname = request.form.get('projectname')
    basicDataName = request.form.get('basicDataName')
    basicDataExpression = request.form.get('basicDataExpression')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    tablename = projectname + "BasicData"
    get_id_sql = f"SELECT id FROM `{tablename}` ORDER BY id DESC LIMIT 1"
    row = fetch_one(get_id_sql, None)
    max_id = row['id'] if row else 0
    id_sql = f"ALTER TABLE `{tablename}` AUTO_INCREMENT = {max_id + 1}"
    update(id_sql, None)
    insert_sql = f"INSERT INTO `{tablename}` (basicDataName, basicDataExpression, creattime) VALUES (%s, %s, %s)"
    insert(insert_sql, (basicDataName, basicDataExpression, current_time))
    print("addbasicData!")
    return jsonify({"message": "基础数据类型创建成功"}), 200


@basic_data_api_blueprint.route('/updateBasicData', methods=['POST'])
def updateBasicData():
    projectname = request.form.get('projectname')
    basicDataName = request.form.get('basicDataName')
    basicDataExpression = request.form.get('basicDataExpression')
    id = request.form.get('id')
    table_name = projectname+"BasicData"
    sql = f"UPDATE `{table_name}` SET `basicDataName` = '{basicDataName}', `basicDataExpression` = '{basicDataExpression}' WHERE `id` = {id};"
    update(sql, None)
    print("updatebasicData!")
    return jsonify({"message": "基础数据类型更新成功"}), 200


@basic_data_api_blueprint.route('/deleteBasicData', methods=['POST'])
def deleteBasicData():
    projectname = request.form.get('projectname')
    id = request.form.get('id')
    table_name = projectname+"BasicData"
    sql = f"DELETE FROM `{table_name}` WHERE `id` = {id};"
    delete(sql, None)
    print("deletebasicData!")
    return jsonify({"message": "基础数据类型删除成功"}), 200
