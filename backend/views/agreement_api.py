from flask import Blueprint, jsonify, request
from datetime import datetime
from db_connect import fetch_all, fetch_one, insert, delete, update
# 创建一个蓝图对象
agreement_api_blueprint = Blueprint('agreement_api', __name__)

@agreement_api_blueprint.route('/getAgreement', methods=['POST'])
def getAgreementData():
    page = request.form.get('currentPage', default=1, type=int)
    print(page)
    size = request.form.get('size', default=10, type=int)
    offset = (page - 1) * size
    projecname = request.form.get('projectname')
    table_name = f"{projecname}Agreement"
    fetch_sql = f"SELECT * FROM `{table_name}` LIMIT %s OFFSET %s"
    agreements = fetch_all(fetch_sql,(size,offset))
    count_sql = f"SELECT COUNT(*) AS total FROM `{table_name}`"
    total = fetch_one(count_sql, None)['total']
    print(agreements)
    return jsonify({"list": agreements, "total": total})


@agreement_api_blueprint.route('/createAgreement', methods=['POST'])
def createAgreement():
    projectname = request.form.get('projectname')
    agreementName = request.form.get('agreementName')
    agreementInterfaces = request.form.get('agreementInterfaces')
    demandId = request.form.get('demandId')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    tablename = projectname + "Agreement"
    get_id_sql = f"SELECT id FROM `{tablename}` ORDER BY id DESC LIMIT 1"
    row = fetch_one(get_id_sql, None)
    max_id = row['id'] if row else 0
    id_sql = f"ALTER TABLE `{tablename}` AUTO_INCREMENT = {max_id + 1}"
    update(id_sql, None)
    insert_sql = f"INSERT INTO `{tablename}` (agreementName, agreementInterfaces, demandId, creatTime) VALUES (%s, %s, %s, %s)"
    insert(insert_sql, (agreementName, agreementInterfaces, demandId, current_time))
    print("add agreement!")
    return jsonify({"message": "合约约定类型创建成功"}), 200


@agreement_api_blueprint.route('/updateAgreement', methods=['POST'])
def updateAgreement():
    projectname = request.form.get('projectname')
    agreementName = request.form.get('agreementName')
    agreementInterfaces = request.form.get('agreementInterfaces')
    demandId = request.form.get('demandId')
    id = request.form.get('id')
    table_name = projectname+"Agreement"
    sql = f"UPDATE `{table_name}` SET `agreementName` = '{agreementName}', `agreementInterfaces` = '{agreementInterfaces}', `demandId` = '{demandId}' WHERE `id` = {id};"
    update(sql, None)
    print("update agreement!")
    return jsonify({"message": "合约约定类型更新成功"}), 200


@agreement_api_blueprint.route('/deleteAgreement', methods=['POST'])
def deleteAgreement():
    projectname = request.form.get('projectname')
    id = request.form.get('id')
    table_name = projectname+"Agreement"
    sql = f"DELETE FROM `{table_name}` WHERE `id` = {id};"
    delete(sql, None)
    print("delete agreement!")
    return jsonify({"message": "合约约定类型删除成功"}), 200
