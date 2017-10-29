# -*-coding:utf-8-*-
from . import main
from flask import url_for, request, render_template, redirect, abort, Response, jsonify
from script.models.mongodb import Ids, Category, connectDB, Product, ImageOpr
from pymongo.errors import DuplicateKeyError
from pymongo import DESCENDING, ASCENDING
import bson.binary
import bson.objectid
import bson.errors
from datetime import datetime
from io import BytesIO
from PIL import Image
import hashlib


@main.route('/ping')
def ping():
    return "ping OK!"


@main.route('/')
def index():
    rootCategoryList = get_category_detail()
    p_list = product_all()
    return render_template("products_display.html", rootCategoryList=rootCategoryList, product_list=p_list)


@main.route('/config')
def config():
    return render_template("config.html")


@main.route('/config/products')
def config_product():
    return render_template("config_products.html")


def save_file(f):
    allow_formats = set(['jpeg', 'png', 'gif', 'jpg'])
    content = BytesIO(f.read())
    try:
        mime = Image.open(content).format.lower()
        if mime not in allow_formats:
            raise IOError()
    except IOError:
        abort(400)
    sha1 = hashlib.sha1(content.getvalue()).hexdigest()

    img1 = ImageOpr()
    ret_list = img1.search({"sha1": sha1})
    if not ret_list:
        img2 = ImageOpr()
        input_json = dict(
            content=bson.binary.Binary(content.getvalue()),
            mime=mime,
            time=datetime.utcnow(),
            sha1=sha1,
        )
        try:
            img2.insert(input_json)
        except DuplicateKeyError:
            pass
    return sha1


"""
{
    "title":
    "price":
    "description":
    "category":
    "sub_category":
    "icon_pictures": []
    "intro_pictures": []
    ""
}
"""


@main.route('/config/product/new', methods=['POST'])
def upload_images():
    title = request.form.get('product_title')
    price = request.form.get('product_price')
    description = request.form.get('product_desc')
    category = int(request.form.get('product_category'))
    sub_category = int(request.form.get('product_sub_category'))

    icon_imgs_sha1_list = []
    for f in request.files.getlist("product_icon_imgs[]"):
        sha1 = save_file(f)
        icon_imgs_sha1_list.append(sha1)

    intro_imgs_sha1_list = []
    for f in request.files.getlist("product_intro_imgs[]"):
        sha1 = save_file(f)
        intro_imgs_sha1_list.append(sha1)

    p = Product()
    input_json = {
        "title": title,
        "price": price,
        "description": description,
        "category": category,
        "sub_category": sub_category,
        "icon_pictures": icon_imgs_sha1_list,
        "intro_pictures": intro_imgs_sha1_list
    }
    data = p.insert(input_json)
    return redirect(url_for('main.config_product'))


@main.route('/img/<sha1>')
def serve_file(sha1):
    try:
        img = ImageOpr()
        f_list = img.search({'sha1': sha1})
        if f_list is None:
            raise bson.errors.InvalidId()
        else:
            f = f_list[0]
            resp = Response(f['content'], mimetype='image/' + f['mime'])
            resp.headers['Last-Modified'] = f['time'].ctime()
            return resp
    except bson.errors.InvalidId:
        abort(404)


@main.route('/config/product/display/<category_type>_<category_id>', methods=['GET'])
def config_product_display(category_type, category_id):
    p = Product()
    if category_type.__str__() == "0":
        qry_json = {"category": int(category_id)}
    else:
        qry_json = {"sub_category": int(category_id)}

    product_list = p.search(qry_json)
    return render_template("config_products_display.html", product_list=product_list)


@main.route('/config/product/display/<product_id>', methods=['GET'])
def config_product_detail(product_id):
    p = Product()
    qry_json = {"id": int(product_id)}
    product_list = p.search(qry_json)
    return render_template("config_products_detail.html", product_list=product_list)


def product_all():
    p = Product()
    order_qry_list = [('category', ASCENDING), ('sub_category', ASCENDING)]
    p_list = p.get_and_sort(order_qry_list)
    return p_list


def product(product_id):
    p = Product()
    qry_json = {"id": int(product_id)}
    p_list = p.search(qry_json)
    return p_list


def get_category_detail():
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

    return rootCategoryList


@main.route('/product/detail/<product_id>', methods=['GET'])
def product_detail(product_id):
    rootCategoryList = get_category_detail()
    product_list = product(product_id)
    return render_template("products_detail.html", rootCategoryList=rootCategoryList, product_list=product_list)


@main.route('/product/display/<category_type>_<category_id>', methods=['GET'])
def product_display_by_category(category_type, category_id):
    rootCategoryList = get_category_detail()

    p = Product()
    if category_type.__str__() == "0":
        qry_json = {"category": int(category_id)}
    else:
        qry_json = {"sub_category": int(category_id)}

    p_list = p.search(qry_json)
    return render_template("products_display.html", rootCategoryList=rootCategoryList, product_list=p_list)