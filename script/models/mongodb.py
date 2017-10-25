import pymongo


def connect(mongodb_url):
    client = pymongo.MongoClient(mongodb_url,
                                 connectTimeoutMS=30000,
                                 socketTimeoutMS=None,
                                 socketKeepAlive=True)
    return client


def insert(client, id_collection, collection, data):
    db = client.get_default_database()
    id = db[id_collection].find_and_modify(update={"$inc": {"id": 1}}, new=True).get("id")
    data['id'] = id
    db[collection].insert_one(data)

    ret_data = data
    ret_data.__delitem__('_id')
    return ret_data

def get(client, collection):
    db = client.get_default_database()
    cursor = db[collection].find()
    ret_list = []
    for doc in cursor:
        doc.__delitem__('_id')
        ret_list.append(doc)
    return ret_list


def search(client, collection, query_json):
    db = client.get_default_database()
    cursor = db[collection].find(query_json)
    ret_list = []
    for doc in cursor:
        doc.__delitem__('_id')
        ret_list.append(doc)
    if ret_list:
        return ret_list[0]
    else:
        return ''


def delete(client, collection, query_json):
    db = client.get_default_database()
    db[collection].remove(query_json)


def update(client, collection, query_json, set_json):
    db = client.get_default_database()
    db[collection].update(
        query_json,
        {"$set": set_json}
    )
