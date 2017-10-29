import pymongo
from script.config import MONGODB_URI


def connectDB():
    client = pymongo.MongoClient(MONGODB_URI,
                                 connectTimeoutMS=30000,
                                 socketTimeoutMS=None,
                                 socketKeepAlive=True)
    db = client.get_default_database()
    return db


"""
{
    "category_id": 101,
    "sub_category_id": 10001,
    "product_id": 100001
}

"""


class Ids:
    def __init__(self):
        self.db = connectDB()
        self.collection = self.db['ids']

    def get_new_category_id(self):
        category_id = self.collection.find_and_modify(update={"$inc": {"category_id": 1}}, new=True).get(
            "category_id")
        return category_id

    def get_new_subcategory_id(self):
        sub_category_id = self.collection.find_and_modify(update={"$inc": {"sub_category_id": 1}}, new=True).get(
            "sub_category_id")
        return sub_category_id

    def get_new_product_id(self):
        product_id = self.collection.find_and_modify(update={"$inc": {"product_id": 1}}, new=True).get("product_id")
        return product_id


    def get_new_image_id(self):
        image_id = self.collection.find_and_modify(update={"$inc": {"image_id": 1}}, new=True).get("image_id")
        return image_id

"""
{
    id:
    category:
    type:  #0: parent 1: children
    parent_id: #parent id, if type 0, then parent_id is 0
}
"""


class Category:
    def __init__(self):
        self.db = connectDB()
        self.collection = self.db['category']

    def insert(self, data):
        id = Ids().get_new_category_id()
        data['id'] = id
        self.collection.insert_one(data)
        data.__delitem__('_id')
        return data

    def get(self):
        cursor = self.collection.find()
        ret_list = []
        for doc in cursor:
            doc.__delitem__('_id')
            ret_list.append(doc)
        return ret_list

    def get_all_root_category_descript(self):
        cursor = self.collection.find({"type": 0})
        ret_list = []
        for doc in cursor:
            doc.__delitem__('_id')
            ret_list.append(doc)
        return ret_list

    def get_all_sub_category_from_parent(self, category_id):
        cursor = self.collection.find({"parent_id": category_id})
        ret_list = []
        for doc in cursor:
            doc.__delitem__('_id')
            ret_list.append(doc)
        return ret_list

    def search(self, query_json):
        cursor = self.collection.find(query_json)
        ret_list = []
        for doc in cursor:
            doc.__delitem__('_id')
            ret_list.append(doc)
        return ret_list

    def delete(self, query_json):
        self.collection.remove(query_json)

    def update(self, query_json, set_json):
        self.collection.update(
            query_json,
            {"$set": set_json}
        )


"""
{
    "title":
    "price":
    "description":
    "icon_pictures":
    "intro_pictures":
    "category":
    "sub_category":
}
"""


class Product:
    def __init__(self):
        self.db = connectDB()
        self.collection = self.db['products']

    def insert(self, data):
        id = Ids().get_new_product_id()
        data['id'] = id
        self.collection.insert_one(data)
        data.__delitem__('_id')
        return data

    def get(self):
        cursor = self.collection.find()
        ret_list = []
        for doc in cursor:
            doc.__delitem__('_id')
            ret_list.append(doc)
        return ret_list

    def get_and_sort(self, qry_list):
        cursor = self.collection.find().sort(qry_list)
        ret_list = []
        for doc in cursor:
            doc.__delitem__('_id')
            ret_list.append(doc)
        return ret_list


    def search(self, query_json):
        cursor = self.collection.find(query_json)
        ret_list = []
        for doc in cursor:
            doc.__delitem__('_id')
            ret_list.append(doc)
        return ret_list

    def delete(self, query_json):
        self.collection.remove(query_json)

    def update(self, query_json, set_json):
        self.collection.update(
            query_json,
            {"$set": set_json}
        )


class ImageOpr:
    def __init__(self):
        self.db = connectDB()
        self.collection = self.db['image']

    def insert(self, data):
        id = Ids().get_new_image_id()
        data['id'] = id
        self.collection.insert_one(data)
        data.__delitem__('_id')
        return data

    def get(self):
        cursor = self.collection.find()
        ret_list = []
        for doc in cursor:
            doc.__delitem__('_id')
            ret_list.append(doc)
        return ret_list

    def search(self, query_json):
        cursor = self.collection.find(query_json)
        ret_list = []
        for doc in cursor:
            doc.__delitem__('_id')
            ret_list.append(doc)
        return ret_list

    def delete(self, query_json):
        self.collection.remove(query_json)

    def update(self, query_json, set_json):
        self.collection.update(
            query_json,
            {"$set": set_json}
        )