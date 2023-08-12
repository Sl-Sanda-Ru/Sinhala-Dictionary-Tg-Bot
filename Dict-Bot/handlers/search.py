import re
import requests
from googletrans import Translator

def gtranslator(word:str, other_langs=False) -> str:
    translator = Translator()
    translation = translator.translate(word, dest='si')
    if other_langs:
        return translation.text if word != translation.text else False
    if translation.src != 'en' and word != translation.text:
        return 'no'
    return translation.text if translation.src == 'en' and word != translation.text else False

def get_cooks():
    r = requests.get('https://www.helakuru.lk/dictionary',
                     headers={
                         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
                     })
    cooks = r.cookies.get('esp-ak')
    return cooks

COOKS = get_cooks()

def get_define(word:str) -> list:
    '''Return Codes: 0 No result,
    1 No result but similar words
    2 have results'''
    r = requests.post('https://www.helakuru.lk/dictionary/get-dictionary-search',
                      cookies={'esp-ak':COOKS},
                      data={'word': word, 'csrf': COOKS},
                      headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
                     })
    if r.json()['STATUS'] == True and r.json()['FIRST_DATA']['word'] != word:
        return 1, re.findall("searchThis\('([^']+)'", #Pattern provided by chatgpt
            r.json()['VIEW'])
    elif r.json()['STATUS'] == True and r.json()['FIRST_DATA']['word'] == word:
        return 2, r.json()['FIRST_DATA']['meaning'].split(", ")
    return 0, []


def definitions(word:str, other_langs=False) -> tuple:
    fmatted = word.lower().strip()
    if len(fmatted.split()) > 1:
        tra = gtranslator(fmatted,other_langs)
        if tra == 'no':
            return tra
        return tra if tra else None
    else:
        tra = get_define(fmatted)
        if tra[0] == 2:
            return tra[1]
        elif tra[0] == 1:
            return tra
        gtra = gtranslator(fmatted)
        return gtra if gtra else None

def result_format(result) -> str:
    if isinstance(result, str):
        return f'✅ {result} \nBot By :\t@Sl_Sanda_Ru'
    else:
        return '✅ ' + '\n✅ '.join(result) + '\nBot By :\t@Sl_Sanda_Ru'