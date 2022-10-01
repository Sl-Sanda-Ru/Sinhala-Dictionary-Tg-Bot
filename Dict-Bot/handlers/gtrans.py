from googletrans import Translator
def gtrans(word:str):
	translator = Translator()
	translation = translator.translate(word, dest='si')
	return translation.text if word != translation.text else False