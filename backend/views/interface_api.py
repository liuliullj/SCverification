from flask import Blueprint, jsonify, request
from datetime import datetime
from db_connect import fetch_all, fetch_one, insert, delete, update
# 创建一个蓝图对象
interface_api_blueprint = Blueprint('interface_api', __name__)


@interface_api_blueprint.route('/getInterface', methods=['POST'])
def getInterfaceData():
    page = request.form.get('currentPage', default=1, type=int)
    print(page)
    size = request.form.get('size', default=10, type=int)
    offset = (page - 1) * size
    projecname = request.form.get('projectname')
    table_name = f"{projecname}Interface"
    fetch_sql = f"SELECT * FROM `{table_name}` LIMIT %s OFFSET %s"
    interfaces = fetch_all(fetch_sql,(size,offset))
    count_sql = f"SELECT COUNT(*) AS total FROM `{table_name}`"
    total = fetch_one(count_sql, None)['total']
    print(interfaces)
    return jsonify({"list": interfaces, "total": total})


@interface_api_blueprint.route('/createInterface', methods=['POST'])
def createInterface():
    projectname = request.form.get('projectname')
    interfaceName = request.form.get('interfaceName')
    interfaceMember = request.form.get('interfaceMember')
    interfaceMethods = request.form.get('interfaceMethods')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    tablename = projectname + "Interface"
    get_id_sql = f"SELECT id FROM `{tablename}` ORDER BY id DESC LIMIT 1"
    row = fetch_one(get_id_sql, None)
    max_id = row['id'] if row else 0
    id_sql = f"ALTER TABLE `{tablename}` AUTO_INCREMENT = {max_id + 1}"
    update(id_sql, None)
    insert_sql = f"INSERT INTO `{tablename}` (interfaceName, interfaceMember, interfaceMethods, creattime) VALUES (%s, %s, %s, %s)"
    insert(insert_sql, (interfaceName, interfaceMember, interfaceMethods, current_time))
    print("add interface!")
    return jsonify({"message": "接口类型创建成功"}), 200


@interface_api_blueprint.route('/updateInterface', methods=['POST'])
def updateInterface():
    projectname = request.form.get('projectname')
    interfaceName = request.form.get('interfaceName')
    interfaceMember = request.form.get('interfaceMember')
    interfaceMethods = request.form.get('interfaceMethods')
    id = request.form.get('id')
    table_name = projectname+"Interface"
    sql = f"UPDATE `{table_name}` SET `interfaceName` = '{interfaceName}', `interfaceMember` = '{interfaceMember}' , `interfaceMethods` = '{interfaceMethods}' WHERE `id` = {id};"
    update(sql, None)
    print("update interface!")
    return jsonify({"message": "接口类型更新成功"}), 200


@interface_api_blueprint.route('/deleteInterface', methods=['POST'])
def deleteInterface():
    projectname = request.form.get('projectname')
    id = request.form.get('id')
    table_name = projectname+"Interface"
    sql = f"DELETE FROM `{table_name}` WHERE `id` = {id};"
    delete(sql, None)
    print("delete interface!")
    return jsonify({"message": "接口类型删除成功"}), 200
