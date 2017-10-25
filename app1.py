import hashlib
import datetime
import flask
import pymongo
import bson.binary
import bson.objectid
import bson.errors
from io import BytesIO
from PIL import Image

app = flask.Flask(__name__)
app.debug = True

from script.config import MONGODB_URI
client = pymongo.MongoClient(MONGODB_URI,
                             connectTimeoutMS=30000,
                             socketTimeoutMS=None,
                             socketKeepAlive=True)
db = client.get_default_database().test

allow_formats = set(['jpeg', 'png', 'gif'])


def save_file(f):
    content = BytesIO(f.read())
    try:
        mime = Image.open(content).format.lower()
        if mime not in allow_formats:
            raise IOError()
    except IOError:
        flask.abort(400)
    sha1 = hashlib.sha1(content.getvalue()).hexdigest()
    c = dict(
        image_id=100001,
        content=bson.binary.Binary(content.getvalue()),
        mime=mime,
        time=datetime.datetime.utcnow(),
        sha1=sha1,
    )
    try:
        db.files.save(c)
    except pymongo.errors.DuplicateKeyError:
        pass
    return sha1


@app.route('/f/<sha1>')
def serve_file(sha1):
    try:
        f = db.files.find_one({'sha1': sha1})
        if f is None:
            raise bson.errors.InvalidId()
        if flask.request.headers.get('If-Modified-Since') == f['time'].ctime():
            return flask.Response(status=304)
        resp = flask.Response(f['content'], mimetype='image/' + f['mime'])
        resp.headers['Last-Modified'] = f['time'].ctime()
        return resp
    except bson.errors.InvalidId:
        flask.abort(404)


@app.route('/upload', methods=['POST'])
def upload():
    f = flask.request.files['uploaded_file']
    sha1 = save_file(f)
    return flask.redirect('/f/' + str(sha1))


@app.route('/')
def index():
    return '''
  <!doctype html>
  <html>
  <body>
  <form action='/upload' method='post' enctype='multipart/form-data'>
     <input type='file' name='uploaded_file'>
     <input type='submit' value='Upload'>
  </form>
  '''


if __name__ == '__main__':
    app.run(port=7777)
