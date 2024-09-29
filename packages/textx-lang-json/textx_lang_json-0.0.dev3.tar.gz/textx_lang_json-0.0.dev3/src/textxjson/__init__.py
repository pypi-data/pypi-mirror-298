import os
from textx import metamodel_from_file
from textx import LanguageDesc
import textxjson.json


__VERSION__ = "0.0dev3"


__json_classes__ = [c for c in textxjson.json.__dict__.values() 
                    if (isinstance(c, type) and c.__module__ == textxjson.json.__name__)]


__PATH__ = os.path.dirname(__file__)


def textxjson_language():
    mm = metamodel_from_file(os.path.join(__PATH__, 'grammar', 'json.tx'), classes = __json_classes__, memoization = False)
    return mm



textxjson_lang = LanguageDesc('textxjson',
                           pattern=None,
                           description='Implementation of JSON standard using textX',
                           metamodel=textxjson_language)


