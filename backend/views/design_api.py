from flask import Blueprint, jsonify, request
import pymysql
import pymysql.cursors
from datetime import datetime
from db_connect import fetch_all, fetch_one, insert, delete, update

# 创建一个蓝图对象
design_api_blueprint = Blueprint('design_api', __name__)

# 你可以从原始文件中复制db和cursor的定义到这里，或者使用其他方式导入它们
# db = pymysql.connect(host="127.0.0.1", user="root", password="1999511510", database="database_learn", port=3306)
# cursor = db.cursor()


@design_api_blueprint.route('/getDesignData', methods=['POST'])
def getDesignData():
    page = request.form.get('currentPage', default=1, type=int)
    print(page)
    size = request.form.get('size', default=10, type=int)
    offset = (page - 1) * size
    projecname = request.form.get('projectname')
    table_name = f"{projecname}Demand"

    category_filter = "category='功能' OR category='方法' OR category='合约参与方' OR category='相关物品' OR category='相关资产' "
    print("get design+"+table_name)
    fetch_sql = f"SELECT * FROM `{table_name}` WHERE {category_filter} LIMIT %s OFFSET %s"
    demands = fetch_all(fetch_sql, (size,offset))
    count_sql = f"SELECT COUNT(*) AS total FROM `{table_name}` WHERE {category_filter}"
    total = fetch_one(count_sql, None)['total']
    print(demands)
    return jsonify({"list": demands, "total": total})



@design_api_blueprint.route('/getPathData', methods=['POST'])
def getPathData():
    page = request.form.get('currentPage', default=1, type=int)
    #print(page)
    size = request.form.get('size', default=10, type=int)
    offset = (page - 1) * size
    projecname = request.form.get('projectname')
    table_name = f"{projecname}Design"
    print("getpath+"+table_name)
    fetch_sql = f"SELECT * FROM `{table_name}` LIMIT %s OFFSET %s"
    designs = fetch_all(fetch_sql, (size, offset))
    count_sql = f"SELECT COUNT(*) AS total FROM `{table_name}`"
    total = fetch_one(count_sql, None)['total']
    print(designs)
    return jsonify({"list": designs, "total": total})


@design_api_blueprint.route('/createDesign', methods=['POST'])
def createDesign():
    projectname = request.form.get('projectname')
    pathname = request.form.get('pathname')
    expression = request.form.get('expression')

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    tablename = projectname + "Design"
    get_id_sql = f"SELECT id FROM `{tablename}` ORDER BY Id DESC LIMIT 1"
    row = fetch_one(get_id_sql, None)
    max_id = row['id'] if row else 0
    id_sql = f"ALTER TABLE `{tablename}` AUTO_INCREMENT = {max_id + 1}"
    update(id_sql, None)
    insert_sql = f"INSERT INTO `{tablename}` (pathname, expression, creattime) VALUES (%s, %s, %s)"
    insert(insert_sql, (pathname, expression,  current_time))
    print("adddesign!")
    return jsonify({"message": "路径创建成功"}), 200


@design_api_blueprint.route('/updateDesign', methods=['POST'])
def updateDesign():
    projectname = request.form.get('projectname')
    pathname = request.form.get('pathname')
    expression = request.form.get('expression')
    id = request.form.get('id')
    table_name = projectname+"Design"
    sql = f"UPDATE `{table_name}` SET `pathname` = '{pathname}', `expression` = '{expression}'  WHERE `id` = {id};"
    update(sql, None)
    print("update design!")
    return jsonify({"message": "路径更新成功"}), 200


@design_api_blueprint.route('/deleteDesign', methods=['POST'])
def deleteDesign():
    projectname = request.form.get('projectname')
    id = request.form.get('id')
    table_name = projectname+"Design"
    sql = f"DELETE FROM `{table_name}` WHERE `id` = {id};"
    delete(sql, None)
    print("deletedesign!")
    return jsonify({"message": "路径删除成功"}), 200