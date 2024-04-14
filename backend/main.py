# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from flask import Flask, request, jsonify
from datetime import datetime
from flask_cors import CORS

from views.basic_data_api import basic_data_api_blueprint
from db_connect import fetch_all, fetch_one, insert, delete, update
from views.condition_api import condition_api_blueprint
from views.demand_api import demand_api_blueprint
from views.design_api import design_api_blueprint
from views.interface_api import interface_api_blueprint

from views.mapping_api import mapping_api_blueprint

app = Flask(__name__)


# 跨域支持
def after_request(response):
    # JS前端跨域支持
    response.headers['Cache-Control'] = 'no-cache'
    response.headers['Access-Control-Allow-Origin'] = '*'
    # response.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE,OPTIONS'
    return response


app.after_request(after_request)


@app.route('/myapi/getTableData', methods=['GET'])
def get_table_data():
    # 获取请求参数
    page = request.args.get('currentPage', default=1, type=int)
    size = request.args.get('size', default=10, type=int)

    offset = (page - 1) * size
    query = f"SELECT * FROM projectmanagement LIMIT {size} OFFSET {offset}"

    # cursor.execute(query, (f'%{name}%', f'%{description}%', size, offset))
    print(query)
    projects = fetch_all(query, None)

    # 获取总数
    count_query = f"SELECT COUNT(*) as total FROM projectmanagement"
    # cursor.execute(count_query, (f'%{name}%', f'%{description}%'))
    tuple_res = fetch_one(count_query, None)
    total = tuple_res['total']

    return jsonify({"list": projects, "total": total})


@app.route('/myapi/createProject', methods=['POST'])
def createProject():
    name = request.form.get('name')
    description = request.form.get('description')
    print(name, description)
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    row = fetch_one("SELECT Id FROM projectmanagement ORDER BY Id DESC LIMIT 1", None)
    print(row)
    max_id = row['Id'] if row else 0
    increment_sql = f"ALTER TABLE projectmanagement AUTO_INCREMENT = {max_id + 1}"
    update(increment_sql, None)
    insert_sql = f"INSERT INTO projectmanagement (name, description, creatTime) VALUES (%s, %s, %s)"
    insert(insert_sql, (name, description, current_time))

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
        `creatTime` DATETIME DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """
    insert(create_table_sql, None)

    #新增项目后创建对应的设计表
    design_name = f"{name}Design"
    create_design_sql = f"""
    CREATE TABLE IF NOT EXISTS `{design_name}` (
        `id` INT AUTO_INCREMENT PRIMARY KEY,
        `pathname` VARCHAR(255) NOT NULL,
        `expression` VARCHAR(255) NOT NULL,
        `creatTime` DATETIME DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """
    insert(create_design_sql, None)

    # 新增项目后创建对应的基础数据表
    table_name = f"{name}BasicData"
    create_basic_data_sql = f"""
        CREATE TABLE IF NOT EXISTS `{table_name}` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `basicDataName` VARCHAR(255) NOT NULL,
            `basicDataExpression` VARCHAR(255) NOT NULL,
            `creatTime` DATETIME DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
    insert(create_basic_data_sql, None)

    # 新增项目后创建对应的映射类型表
    table_name = f"{name}Mapping"
    create_mapping_sql = f"""
            CREATE TABLE IF NOT EXISTS `{table_name}` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `mappingName` VARCHAR(255) NOT NULL,
                `mappingInputBasicData` VARCHAR(255) NOT NULL,
                `mappingOutputBasicData` VARCHAR(255) NOT NULL,
                `creatTime` DATETIME DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """
    insert(create_mapping_sql, None)

    # 新增项目后创建对应的接口类型表
    table_name = f"{name}Interface"
    create_interface_sql = f"""
                CREATE TABLE IF NOT EXISTS `{table_name}` (
                    `id` INT AUTO_INCREMENT PRIMARY KEY,
                    `interfaceName` VARCHAR(255) NOT NULL,
                    `interfaceMember` VARCHAR(255) NOT NULL,
                    `interfaceMethods` VARCHAR(255) NOT NULL,
                    `creatTime` DATETIME DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
                """
    insert(create_interface_sql, None)

    # 新增项目后创建对应的条件类型表
    table_name = f"{name}Condition"
    create_condition_sql = f"""
                    CREATE TABLE IF NOT EXISTS `{table_name}` (
                        `id` INT AUTO_INCREMENT PRIMARY KEY,
                        `conditionName` VARCHAR(255) NOT NULL,
                        `conditionBasicDataOne` VARCHAR(255) NOT NULL,
                        `conditionBasicDataTwo` VARCHAR(255) NOT NULL,
                        `conditionOperator` VARCHAR(255) NOT NULL,
                        `creatTime` DATETIME DEFAULT CURRENT_TIMESTAMP
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
                    """
    insert(create_condition_sql, None)

    return jsonify({"message": "项目创建成功"}), 200



@app.route('/myapi/deleteProject', methods=['POST'])
def deleteProject():
    id = request.form.get('id')
    #删除对应的表
    sql_select_name = f"SELECT * FROM projectmanagement WHERE Id = {id}"
    print(sql_select_name)
    result = fetch_one(sql_select_name, None)
    print(result)
    if result:
        name = result['name']
        design_name = name + "Design"
        demand_name = name + "Demand"
        print(name)

        sql_delete_table = f"DROP TABLE IF EXISTS `{demand_name}`;"
        delete(sql_delete_table, None)

        sql_delete_design = f"DROP TABLE IF EXISTS `{design_name}`;"
        delete(sql_delete_design, None)

        basicDataName = name + "BasicData"
        sql_delete_basic_data = f"DROP TABLE IF EXISTS `{basicDataName}`;"
        delete(sql_delete_basic_data, None)

        mappingName = name + "Mapping"
        sql_delete_mapping = f"DROP TABLE IF EXISTS `{mappingName}`;"
        delete(sql_delete_mapping, None)

        interfaceName = name + "Interface"
        sql_delete_interface = f"DROP TABLE IF EXISTS `{interfaceName}`;"
        delete(sql_delete_interface, None)

        conditionName = name + "Condition"
        sql_delete_condition = f"DROP TABLE IF EXISTS `{conditionName}`;"
        delete(sql_delete_condition, None)
    #删除该行
    sql = "DELETE FROM projectmanagement WHERE id = %s"
    delete(sql, (id,))
    print("delete!")
    return jsonify({"message": "项目删除成功"}), 200


@app.route('/myapi/updateProject', methods=['POST'])
def updateProject():
    id = request.form.get('id')
    name = request.form.get('name')
    description = request.form.get('description')
    print(description)
    sql_ori_name = f"SELECT * FROM projectmanagement WHERE id = {id}"
    result = fetch_one(sql_ori_name, None)
    ori_name = result['name']+"Demand"
    new_name = name + "Demand"
    rename_table_sql = f"RENAME TABLE `{ori_name}` TO `{new_name}`;"
    update(rename_table_sql, None)


    ori_design_name = result['name']+"Design"
    new_design_name = name + "Design"
    rename_design = f"RENAME TABLE `{ori_design_name}` TO `{new_design_name}`;"
    update(rename_design, None)

    ori_basic_data_name = result['name'] + "BasicData"
    new_basic_data_name = name + "BasicData"
    rename_basic_data = f"RENAME TABLE `{ori_basic_data_name}` TO `{new_basic_data_name}`;"
    update(rename_basic_data, None)

    ori_mapping_name = result['name'] + "Mapping"
    new_mapping_name = name + "Mapping"
    rename_mapping = f"RENAME TABLE `{ori_mapping_name}` TO `{new_mapping_name}`;"
    update(rename_mapping, None)

    ori_interface_name = result['name'] + "Interface"
    new_interface_name = name + "Interface"
    rename_interface = f"RENAME TABLE `{ori_interface_name}` TO `{new_interface_name}`;"
    update(rename_interface, None)

    ori_condition_name = result['name'] + "Condition"
    new_condition_name = name + "Condition"
    rename_condition = f"RENAME TABLE `{ori_condition_name}` TO `{new_condition_name}`;"
    update(rename_condition, None)


    sql = "UPDATE projectmanagement SET name = %s, description = %s WHERE id = %s"
    update(sql, (name, description, id))
    print("update!")
    return jsonify({"message": "项目更新成功"}), 200


app.register_blueprint(demand_api_blueprint, url_prefix='/myapi')
app.register_blueprint(design_api_blueprint, url_prefix='/myapi')
app.register_blueprint(basic_data_api_blueprint, url_prefix='/myapi')
app.register_blueprint(mapping_api_blueprint, url_prefix='/myapi')
app.register_blueprint(interface_api_blueprint, url_prefix='/myapi')
app.register_blueprint(condition_api_blueprint, url_prefix='/myapi')


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
