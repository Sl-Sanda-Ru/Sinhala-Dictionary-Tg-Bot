from tinydb import Query, TinyDB
db = TinyDB('uids.json')
cursor = Query()

def insert(id:int, status=False):
    result = search(id)
    if result == None:
        db.insert({'ID': id, 'UNIVERSAL': status})
    if result in (True,False):
        db.update({'UNIVERSAL': status}, cursor.ID == id)

def search(id):
    result = db.search(cursor.ID == id)
    return result[0]['UNIVERSAL'] if result else None