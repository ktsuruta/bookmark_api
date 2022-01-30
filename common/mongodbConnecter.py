from linkpreview import link_preview


def connect_database(database_name):
    from pymongo import MongoClient
    import pymongo

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb://bookmark_organizer_db_1:27017"
    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client[database_name]

def insert_element_of_json(json_object, parent_folder, db):

    if type(json_object) == list:
        for el in json_object:
            insert_element_of_json(el, '', db)
    elif 'children' in json_object:
        for child in json_object['children']:
            folder = parent_folder + '/' + json_object['title'] 
            insert_element_of_json(child, folder, db)
    else:
        try:
            url = (json_object['url'])
            preview = link_preview(url)
            print(preview)
            result = {"path": parent_folder,
                        "url": json_object['url'],
                        "bookmark_name": json_object['title'],
                        "title": preview.title, 
                        "description": preview.description, 
                        "image": preview.image, 
                        "force_title": preview.force_title, 
                        "absolute_image": preview.absolute_image,
                        "link_preview": True
                        }
            
            db.bookmarks.insert_one(result)

        except:
            result = {"path": parent_folder,
                        "url": json_object['url'],
                        "bookmark_name": json_object['title'],
                        "title": '',
                        "description": '', 
                        "image": '', 
                        "force_title": '', 
                        "absolute_image": '',
                        "link_preview": False
                        }
            
            db.bookmarks.insert_one(result)

def find_many(collection, filter=None, sort=None):
    bookmarks = collection.find(filter=filter,sort=sort)
    bookmark_list = []
    for bookmark in bookmarks:
        bookmark_list.append(bookmark)
    return bookmark_list


def get_path(collection):
    paths = collection.find().distinct('path')
    path_list = []
    for path in paths:
        path_list.append(path)
    return path_list


# This is added so that many files can reuse the function connect_database()
if __name__ == "__main__":    
    
 
    import pprint
    import bookmarks_parser

    # bookmarks = bookmarks_parser.parse("data/bookmarks.html")
    # pprint.pprint(bookmarks)

    # Connect to the database
    db = connect_database('test')
    # insert_element_of_json(bookmarks, '/', db)

    # bookmark_list = find_many(db.bookmarks, {'path':'/Bookmarks bar'})
    # print(bookmark_list)
 
    # path_list = get_path(db.bookmarks)
    # print(path_list)

    bookmark_list = find_many(db.bookmarks, {'title': {'$regex': 'vue'}})
    print(bookmark_list)
