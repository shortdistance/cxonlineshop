# -*-coding:utf-8-*-
from flask import jsonify, request
from . import api
from script.config import MONGODB_URI
from script.models.mongodb import connect, insert, get, search, delete, update


@api.route('/test')
def test():
    return jsonify(msg='success')


@api.route('/todo/create', methods=['POST'])
def todo_create():
    request.get_json(force=True)
    req_json = request.json
    ret_data = None
    if req_json and isinstance(req_json, dict):
        try:
            client = connect(MONGODB_URI)
            ret_data = insert(client, 'id_collection', 'my_test', req_json)
            msg = 'success'
        except Exception as e:
            msg = str(e)
    else:
        msg = 'request json: ' + req_json.__str__()
    return jsonify(msg=msg, ret_data=ret_data)


@api.route('/todo', methods=['GET'])
def todo():
    ret_list = []
    try:
        client = connect(MONGODB_URI)
        ret_list = get(client, 'my_test')
    except Exception as e:
        pass

    return jsonify(ret_list)


@api.route('/todo/<int:id>', methods=['GET'])
def one_todo(id):
    ret_json = {}
    try:
        client = connect(MONGODB_URI)
        ret_json = search(client, 'my_test', {'id': id})
    except Exception as e:
        pass

    return jsonify(ret_json)


@api.route('/todo/delete/<int:id>', methods=['DELETE'])
def todo_delete(id):
    try:
        client = connect(MONGODB_URI)
        delete(client, 'my_test', {'id': id})
        msg = 'Success'
    except Exception as e:
        msg = e
    return jsonify(msg)


@api.route('/todo/put/<int:id>', methods=['PUT'])
def todo_update(id):
    request.get_json(force=True)
    req_json = request.json
    try:
        client = connect(MONGODB_URI)
        update(client, 'my_test', {'id': id}, req_json)
        msg = 'Success'
    except Exception as e:
        msg = e
    return jsonify(msg)
