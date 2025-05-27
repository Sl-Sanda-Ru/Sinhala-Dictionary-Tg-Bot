import sqlite3
from googletrans import Translator
from langcodes import Language
from difflib import get_close_matches

translator = Translator()


def get_define(word: str) -> tuple:
    '''1 have results
    2 No result but similar words    
    3 no results probably src not english'''
    with sqlite3.connect('file:sin_en.db?mode=ro', uri=True) as CONN:
        CURSOR = CONN.cursor()
        CURSOR.execute(
            "SELECT en_to_sin_defs FROM en_to_sin WHERE en_to_sin_keys = ?", (word,))
        RESULT = CURSOR.fetchone()
        if RESULT is not None:
            return 1, RESULT[0].split('%')
        else:
            CURSOR.execute("SELECT en_to_sin_keys FROM en_to_sin")
            all_strings = [result[0] for result in CURSOR.fetchall()]
            suggest = get_close_matches(word, all_strings, n=10, cutoff=0.5)
            CURSOR.close()
            if suggest == []:
                return 3,
        return 2, suggest


def gtranslator(word, any=False):
    '''1: normal ok
    2: any disabled'''
    lan = translator.detect(text=word)
    if any:
        if lan.lang == 'si':
            return 1, translator.translate(text=word, dest='en').text
        else:
            return 1, translator.translate(text=word, dest='si').text
    elif lan.lang != 'en':
        lan_name = Language.make(language=lan.lang).display_name()
        return 2, lan_name
    else:
        return 1, translator.translate(text=word, dest='si').text


def join_search(word, any=False):
    if len(word.split(' ')) == 1:
        result = get_define(word)
        if result[0] == 3:
            result = gtranslator(word, any=any)
            return result
        else:
            return result
    else:
        result = gtranslator(word, any=any)
        return result


def result_format(result) -> str:
    if isinstance(result, str):
        return f'✅ {result} \nBot By :\t@Sl_Sanda_Ru'
    else:
        return '✅ ' + "\n✅ ".join(result) + "\nBot By :\t@Sl_Sanda_Ru"
