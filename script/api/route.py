# -*-coding:utf-8-*-
from flask import jsonify, request
from . import api
from script.config import MONGODB_URI
from script.models.mongodb import Category


@api.route('/test')
def test():
    return jsonify(msg='success')


"""
{
    id:
    category:
    type:  #0: parent 1: children
    parent_id: #parent id, if type 0, then parent_id is 0
}
"""


@api.route('/addNewCategory', methods=['POST'])
def addNewCategory():
    request.get_json(force=True)
    req_json = request.json
    print(req_json)
    if req_json and isinstance(req_json, dict):
        category = Category()
        ret_data = category.insert(req_json)
    return jsonify(data=ret_data)


@api.route('/getRootCategory', methods=['GET'])
def getRootCategory():
    category = Category()
    ret_data = category.get_all_root_category_descript()
    return jsonify(data=ret_data)


@api.route('/getSubCategoryById/<id>', methods=['GET'])
def getSubCategoryById(id):
    if id.__str__().isdigit():
        category = Category()
        ret_data = category.get_all_sub_category_from_parent(int(id))
        return jsonify(data=ret_data)
    else:
        return jsonify(data=[])

@api.route('/deleteCategoryAndSubCategoryById', methods=['POST'])
def deleteCategoryAndSubCategoryById():
    request.get_json(force=True)
    category_id = request.json["id"]

    print(request.json)
    category = Category()
    category.delete({"id": category_id})
    category1 = Category()
    category1.delete({"parent_id": category_id})
    return jsonify(success=True)


@api.route('/deleteSubCategoryById', methods=['POST'])
def delSubCategoryById():
    request.get_json(force=True)
    qry_json = request.json
    category = Category()
    category.delete(qry_json)
    return jsonify(success=True)


@api.route('/getCategoryInfo')
def getAllCategoryInfo():
    category = Category()
    category_list = category.get()
    rootCategoryList = []
    subCategoryList = []
    for c in category_list:
        if c["type"] == 0:
            rootCategoryList.append(c)
        else:
            subCategoryList.append(c)

    for rc in rootCategoryList:
        rc["sub_category"] = []
        for sc in subCategoryList:
            if rc["id"] == sc["parent_id"]:
                rc["sub_category"].append(sc)

    return jsonify(rootCategoryList=rootCategoryList)


# @api.route('/todo/create', methods=['POST'])
# def todo_create():
#     request.get_json(force=True)
#     req_json = request.json
#     ret_data = None
#     if req_json and isinstance(req_json, dict):
#         try:
#             client = connect(MONGODB_URI)
#             ret_data = insert(client, 'id_collection', 'my_test', req_json)
#             msg = 'success'
#         except Exception as e:
#             msg = str(e)
#     else:
#         msg = 'request json: ' + req_json.__str__()
#     return jsonify(msg=msg, ret_data=ret_data)
#
#
# @api.route('/todo', methods=['GET'])
# def todo():
#     ret_list = []
#     try:
#         client = connect(MONGODB_URI)
#         ret_list = get(client, 'my_test')
#     except Exception as e:
#         pass
#
#     return jsonify(ret_list)
#
#
# @api.route('/todo/<int:id>', methods=['GET'])
# def one_todo(id):
#     ret_json = {}
#     try:
#         client = connect(MONGODB_URI)
#         ret_json = search(client, 'my_test', {'id': id})
#     except Exception as e:
#         pass
#
#     return jsonify(ret_json)
#
#
# @api.route('/todo/delete/<int:id>', methods=['DELETE'])
# def todo_delete(id):
#     try:
#         client = connect(MONGODB_URI)
#         delete(client, 'my_test', {'id': id})
#         msg = 'Success'
#     except Exception as e:
#         msg = e
#     return jsonify(msg)
#
#
# @api.route('/todo/put/<int:id>', methods=['PUT'])
# def todo_update(id):
#     request.get_json(force=True)
#     req_json = request.json
#     try:
#         client = connect(MONGODB_URI)
#         update(client, 'my_test', {'id': id}, req_json)
#         msg = 'Success'
#     except Exception as e:
#         msg = e
#     return jsonify(msg)
