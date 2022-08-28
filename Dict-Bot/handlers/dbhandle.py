import sqlite3
CONN = sqlite3.connect("file:database.sqlite3?mode=ro", uri=True)
def search(conn,word:str):
    sql = 'SELECT definition FROM enDictionary WHERE word = "{0}"'
    cursor = conn.cursor()
    cursor.execute(sql.format(word))
    result = cursor.fetchall()
    cursor.close()
    if len(result) == 0:
        return None
    else:
        return [word.strip() for word in result[0][0].split(',')]
def suggetions(conn, word:str):
    cursor = conn.cursor()
    sql = 'SELECT word FROM enDictionary WHERE word LIKE "{0}%"'
    count = -1
    while True:
        cursor.execute(sql.format(word[:count].lower()))
        result = cursor.fetchall()
        if len(result) >= 1:
            break
        else:
            count-=1
            if len(word[:count]) == 0:
                break
    cursor.close()
    return [result [i[0]][0] for i in enumerate(result) if i[0] <= 20]
def join_search(conn,word:str):
    if search(conn, word) is None:
        return False,suggetions(conn, word)
    else:
        return True,search(conn, word)