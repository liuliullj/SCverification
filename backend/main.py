# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from flask import Flask, request, jsonify, make_response
import pymysql
import pymysql.cursors
from datetime import datetime
from flask_cors import CORS, cross_origin
from demand_api import demand_api_blueprint
from design_api import design_api_blueprint
import json

app = Flask(__name__)


# 跨域支持
def after_request(response):
    # JS前端跨域支持
    response.headers['Cache-Control'] = 'no-cache'
    response.headers['Access-Control-Allow-Origin'] = '*'
    # response.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE,OPTIONS'
    return response


app.after_request(after_request)

HOSTNAME = "127.0.0.1"
PORT = 3306
USERNAME = "root"
PASSWORD = "990326Llj"
DATABASE = "database_learn"

db = pymysql.connect(host=HOSTNAME, user=USERNAME, password=PASSWORD, database=DATABASE, port=PORT)  # 建立连接

cursor = db.cursor()


@app.route('/myapi/getTableData', methods=['GET'])
def get_table_data():
    # 获取请求参数
    page = request.args.get('currentPage', default=1, type=int)
    size = request.args.get('size', default=10, type=int)
    name = request.args.get('name', default='', type=str)
    description = request.args.get('description', default='', type=str)

    offset = (page - 1) * size
    query = "SELECT * FROM projectmanagement WHERE name LIKE %s AND description LIKE %s LIMIT %s OFFSET %s"

    cursor.execute(query, (f'%{name}%', f'%{description}%', size, offset))
    projects = cursor.fetchall()

    # 获取总数
    count_query = "SELECT COUNT(*) as total FROM projectmanagement WHERE name LIKE %s AND description LIKE %s"
    cursor.execute(count_query, (f'%{name}%', f'%{description}%'))
    tuple_res = cursor.fetchone()
    print(projects)
    total = tuple_res[0]

    return jsonify({"list": projects, "total": total})
    # return "hello world"


@app.route('/myapi/createProject', methods=['POST'])
def createProject():

    # if request.method == 'OPTIONS':
    #     headers = {
    #         'Content-Type': 'application/json',
    #         'Access-Control-Allow-Origin': '*',
    #         'Access-Control-Allow-Methods': 'POST'
    #     }
    #     return make_response(jsonify({"error_code": 0}), 200, headers)
    # else:
    name = request.form.get('name')
    description = request.form.get('description')
    print(name, description)
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("SELECT Id FROM projectmanagement ORDER BY Id DESC LIMIT 1")
    row = cursor.fetchone()
    max_id = row[0] if row else 0
    cursor.execute("ALTER TABLE projectmanagement AUTO_INCREMENT = %s", (max_id + 1,))
    sql = "INSERT INTO projectmanagement (name, description, creattime) VALUES (%s, %s, %s)"
    cursor.execute(sql, (name, description, current_time))
    cursor.connection.commit()
    print("add!")

    # 新增项目后创建对应的需求表
    table_name = f"{name}Demand"
    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS `{table_name}` (
        `id` INT AUTO_INCREMENT PRIMARY KEY,
        `demandname` VARCHAR(255) NOT NULL,
        `category` VARCHAR(255) NOT NULL,
        `demanddescription` VARCHAR(255),
        `parentD` INT,
        `creattime` DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (`parentD`) REFERENCES `{table_name}` (`id`) ON DELETE SET NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """
    cursor.execute(create_table_sql)
    cursor.connection.commit()

    #新增项目后创建对应的设计表
    design_name = f"{name}Design"
    create_design_sql = f"""
    CREATE TABLE IF NOT EXISTS `{design_name}` (
        `id` INT AUTO_INCREMENT PRIMARY KEY,
        `pathname` VARCHAR(255) NOT NULL,
        `expression` VARCHAR(255) NOT NULL,
        `creattime` DATETIME DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """
    cursor.execute(create_design_sql)
    cursor.connection.commit()

    return jsonify({"message": "项目创建成功"}), 200



@app.route('/myapi/deleteProject', methods=['POST'])
def deleteProject():
    id = request.form.get('id')
    #删除对应的表
    sql_select_name = f"SELECT * FROM projectmanagement WHERE id = {id}"
    print(sql_select_name)
    cursor.execute(sql_select_name)
    result = cursor.fetchone()
    print(result)
    if result:
        name = result[1]
        design_name = name + "Design"
        name += "Demand"
        print(name)
        sql_delete_table = f"DROP TABLE IF EXISTS `{name}`;"
        cursor.execute(sql_delete_table)
        sql_delete_design = f"DROP TABLE IF EXISTS `{design_name}`;"
        cursor.execute(sql_delete_design)
    #删除该行
    sql = "DELETE FROM projectmanagement WHERE id = %s"
    cursor.execute(sql, (id,))
    cursor.connection.commit()
    print("delete!")
    return jsonify({"message": "项目删除成功"}), 200


@app.route('/myapi/updateProject', methods=['POST'])
def updateProject():
    id = request.form.get('id')
    name = request.form.get('name')
    description = request.form.get('description')
    print(description)
    sql_ori_name = f"SELECT * FROM projectmanagement WHERE id = {id}"
    cursor.execute(sql_ori_name)
    result = cursor.fetchone()
    ori_name = result[1]+"Demand"
    new_name = name + "Demand"
    rename_table_sql = f"RENAME TABLE `{ori_name}` TO `{new_name}`;"
    cursor.execute(rename_table_sql)
    cursor.connection.commit()

    ori_design_name = result[1]+"Design"
    new_design_name = name + "Design"
    rename_design = f"RENAME TABLE `{ori_design_name}` TO `{new_design_name}`;"
    cursor.execute(rename_design)
    cursor.connection.commit()


    sql = "UPDATE projectmanagement SET name = %s, description = %s WHERE id = %s"
    cursor.execute(sql, (name, description, id))
    cursor.connection.commit()
    print("update!")
    return jsonify({"message": "项目更新成功"}), 200


app.register_blueprint(demand_api_blueprint, url_prefix='/myapi')
app.register_blueprint(design_api_blueprint, url_prefix='/myapi')

# @app.route('/myapi/getProjectName', methods=['GET'])
# def getProjectName():
#     sql = "SELECT name FROM projectmanagement"
#     cursor.execute(sql)
#     result = cursor.fetchall()
#     names = [row[0] for row in result]
#     print(names)
#     return jsonify(names)
#
#
# @app.route('/myapi/getDemandData', methods=['POST'])
# def getDemandData():
#     projecname = request.form.get('projectname')
#     projecname += "Demand"
#     fetch_sql = f"SELECT * FROM `{projecname}`"
#     cursor.execute(fetch_sql)
#     demands = cursor.fetchall()
#     print(projecname)
#     count_sql = f"SELECT COUNT(*) AS total FROM `{projecname}`"
#     cursor.execute(count_sql)
#     total = cursor.fetchone()[0]
#     print(demands)
#     return jsonify({"list": demands, "total": total})



if __name__ == '__main__':
    app.run(host="127.0.0.1", debug=True)
    CORS(app, supports_credentials=True)  # 跨域设置

# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.
#
#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
