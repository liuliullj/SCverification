from flask import Blueprint, jsonify, request
import pymysql
import pymysql.cursors
from datetime import datetime
from db_connect import fetch_all, fetch_one, insert, delete, update
# 创建一个蓝图对象
demand_api_blueprint = Blueprint('demand_api', __name__)

# 从原始文件中复制db和cursor的定义到这里，或者使用其他方式导入它们
# db = pymysql.connect(host="127.0.0.1", user="root", password="1999511510", database="database_learn", port=3306)
# cursor = db.cursor()

@demand_api_blueprint.route('/getProjectName', methods=['GET'])
def getProjectName():
    sql = "SELECT name FROM projectmanagement"
    print(sql)
    result = fetch_all(sql, None)
    names = [row['name'] for row in result]
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
    category_filter = "category='功能' OR category='执行流程' OR category='业务' OR category='智能合约' "
    fetch_sql = f"SELECT * FROM `{table_name}` WHERE {category_filter} LIMIT %s OFFSET %s"
    demands = fetch_all(fetch_sql,(size,offset))
    count_sql = f"SELECT COUNT(*) AS total FROM `{table_name}`"
    total = fetch_one(count_sql, None)['total']
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
    get_id_sql = f"SELECT id FROM `{tablename}` ORDER BY id DESC LIMIT 1"
    row = fetch_one(get_id_sql, None)
    max_id = row['id'] if row else 0
    id_sql = f"ALTER TABLE `{tablename}` AUTO_INCREMENT = {max_id + 1}"
    update(id_sql, None)
    insert_sql = f"INSERT INTO `{tablename}` (demandname, category, demanddescription, parentD,creattime) VALUES (%s, %s, %s, %s, %s)"
    insert(insert_sql, (demandname, category, demanddescription, parentD, current_time))
    print("add demand!")
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
    update(sql, None)
    print("update demand!")
    return jsonify({"message": "需求更新成功"}), 200


@demand_api_blueprint.route('/deleteDemand', methods=['POST'])
def deleteDemand():
    projectname = request.form.get('projectname')
    id = request.form.get('id')
    table_name = projectname+"Demand"
    sql = f"DELETE FROM `{table_name}` WHERE `id` = {id};"
    delete(sql, None)
    print("delete demand!")
    return jsonify({"message": "需求删除成功"}), 200
