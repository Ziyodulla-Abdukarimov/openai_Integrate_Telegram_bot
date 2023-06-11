from googletrans import Translator


def detect_language(text):
    translator = Translator()
    result = translator.detect(text)
    lang = result.lang
    return lang
