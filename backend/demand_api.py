from flask import Blueprint, jsonify, request
import pymysql
import pymysql.cursors
from datetime import datetime

# 创建一个蓝图对象
demand_api_blueprint = Blueprint('demand_api', __name__)

# 从原始文件中复制db和cursor的定义到这里，或者使用其他方式导入它们
db = pymysql.connect(host="127.0.0.1", user="root", password="990326Llj", database="database_learn", port=3306)
cursor = db.cursor()

@demand_api_blueprint.route('/getProjectName', methods=['GET'])
def getProjectName():
    sql = "SELECT name FROM projectmanagement"
    cursor.execute(sql)
    result = cursor.fetchall()
    names = [row[0] for row in result]
    print(names)
    return jsonify(names)

@demand_api_blueprint.route('/getDemandData', methods=['POST'])
def getDemandData():
    page = request.form.get('currentPage', default=1, type=int)
    print(page)
    size = request.form.get('size', default=10, type=int)
    offset = (page - 1) * size
    projecname = request.form.get('projectname')
    table_name = f"{projecname}Demand"
    fetch_sql = f"SELECT * FROM `{table_name}` LIMIT %s OFFSET %s"
    cursor.execute(fetch_sql,(size,offset))
    demands = cursor.fetchall()
    count_sql = f"SELECT COUNT(*) AS total FROM `{table_name}`"
    cursor.execute(count_sql)
    total = cursor.fetchone()[0]
    print(demands)
    return jsonify({"list": demands, "total": total})


@demand_api_blueprint.route('/createDemand', methods=['POST'])
def createDemand():
    projectname = request.form.get('projectname')
    demandname = request.form.get('demandname')
    category = request.form.get('category')
    demanddescription = request.form.get('demanddescription')
    parentD = request.form.get('parentD')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    tablename = projectname + "Demand"
    get_id_sql = f"SELECT Id FROM `{tablename}` ORDER BY Id DESC LIMIT 1"
    cursor.execute(get_id_sql)
    row = cursor.fetchone()
    max_id = row[0] if row else 0
    id_sql = f"ALTER TABLE `{tablename}` AUTO_INCREMENT = {max_id + 1}"
    cursor.execute(id_sql)
    insert_sql = f"INSERT INTO `{tablename}` (demandname, category, demanddescription, parentD,creattime) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(insert_sql, (demandname, category, demanddescription, parentD, current_time))
    cursor.connection.commit()
    print("adddemand!")
    return jsonify({"message": "需求创建成功"}), 200


@demand_api_blueprint.route('/updateDemand', methods=['POST'])
def updateDemand():
    projectname = request.form.get('projectname')
    demandname = request.form.get('demandname')
    category = request.form.get('category')
    demanddescription = request.form.get('demanddescription')
    parentD = request.form.get('parentD')
    id = request.form.get('id')
    table_name = projectname+"Demand"
    sql = f"UPDATE `{table_name}` SET `demandname` = '{demandname}', `category` = '{category}', `demanddescription` = '{demanddescription}', `parentD` = {parentD} WHERE `id` = {id};"
    cursor.execute(sql)
    cursor.connection.commit()
    print("updatedemand!")
    return jsonify({"message": "需求更新成功"}), 200


@demand_api_blueprint.route('/deleteDemand', methods=['POST'])
def deleteDemand():
    projectname = request.form.get('projectname')
    id = request.form.get('id')
    table_name = projectname+"Demand"
    sql = f"DELETE FROM `{table_name}` WHERE `id` = {id};"
    cursor.execute(sql)
    cursor.connection.commit()
    print("deletedemand!")
    return jsonify({"message": "需求删除成功"}), 200
