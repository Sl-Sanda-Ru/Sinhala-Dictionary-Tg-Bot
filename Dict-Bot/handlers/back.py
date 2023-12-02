from tinydb import Query, TinyDB
db = TinyDB('uids.json')
cursor = Query()

def insert(id:int, lang='', status=None):
    result = search(id)
    if result == None:
        db.insert({'ID': id, 'UNIVERSAL': False, 'LANG': ''})
    elif result[0] in (True, False) and status in (True, False):
        db.update({'UNIVERSAL': status}, cursor.ID == id)
    elif lang in ('sin', 'eng'):
        db.update({'LANG': lang}, cursor.ID == id)

def search(id):
    result = db.search(cursor.ID == id)
    if result:
        return result[0]['UNIVERSAL'], result[0]['LANG']
    else:
        return None