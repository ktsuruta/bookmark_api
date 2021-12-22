import os
from flask import Flask, jsonify, request 
from flask_cors import CORS
from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS = ['html']
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'html', 'csv'}

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/api/link_preview")
def home():
    from linkpreview import link_preview
    url = request.args.get('url')
    print(url)
    if url == '':
        url = 'https://note.com/takehilo/n/ndc168569f64c'
    preview = link_preview(url)
    print(preview)
    result = {"title": preview.title, "description": preview.description, "image": preview.image, "force_title": preview.force_title, "absolute_image": preview.absolute_image}
    print(result)
    return jsonify(result)

@app.route("/api/bookmark")
def get_bookmark():
    import json
    import common.mongodbConnecter as mongodbConnecter
    path = request.args.get('path')
    db = mongodbConnecter.connect_database('test')
    bookmark_list = mongodbConnecter.find_many(db.bookmarks, {'path':path})
    # print(bookmark_list)
    print(json.dumps(bookmark_list, default=str, ensure_ascii=False))
    return json.dumps(bookmark_list, default=str, ensure_ascii=False)

@app.route("/api/bookmark/search")
def search_bookmark():
    import json
    import common.mongodbConnecter as mongodbConnecter
    query = request.args.get('query')
    print(query)
    db = mongodbConnecter.connect_database('test')
    bookmark_list = mongodbConnecter.find_many(db.bookmarks, {'title': {'$regex': query}})
    # print(bookmark_list)
    print(json.dumps(bookmark_list, default=str, ensure_ascii=False))
    return json.dumps(bookmark_list, default=str, ensure_ascii=False)


@app.route("/api/folder")
def get_folder():
    import common.mongodbConnecter as mongodbConnecter
    import json
    db = mongodbConnecter.connect_database('test')
    path_list = mongodbConnecter.get_path(db.bookmarks)
    print(json.dumps(path_list, default=str, ensure_ascii=False))
    return json.dumps(path_list, default=str, ensure_ascii=False)



def __allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload/bookmarks', methods=['POST'])
def upload_file():
    import pprint
    import bookmarks_parser

    if request.method == 'POST':
        # check if the post request has the file part
        print("Post")
        print(request.files['file'])
        if 'file' not in request.files:
            return """No file"""
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return '''No file selected'''
        if file and __allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            bookmarks = bookmarks_parser.parse(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            # Connect to the database
        try:
            import json
            import common.mongodbConnecter as mongodbConnecter
            db = mongodbConnecter.connect_database('test')
            mongodbConnecter.insert_element_of_json(bookmarks, '/', db)
            return '''OK'''
        except:
            return '''Inserting json to Mongodb failed'''
 