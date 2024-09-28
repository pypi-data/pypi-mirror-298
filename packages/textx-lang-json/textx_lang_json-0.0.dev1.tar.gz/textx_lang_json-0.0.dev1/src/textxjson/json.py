''' json.py
(c) Jean-François Baget, 2024

Custom classes specializing the ones automatically generated when instanciating the Json grammar metamodel.
This is mainly used to provide the decode() method.
'''
from __future__ import annotations
from typing import Any

import re
from abc import ABC, abstractmethod

class JsonText():
    ''' A container class for models built from a Json text.
    '''

    def __init__(self, value: JsonValue) -> None:
        self.value = value

    def decode(self) -> Any:
        ''' Returns the python standard encoding of a JsonText object.
        '''
        return self.value.decode()

class JsonValue(ABC):
    ''' An abstract class for all possible Json values, that must implement the resolve() method.
    '''

    def __init__(self, parent: Any, value: Any) -> None:
        self.parent, self.value = parent, value

    @abstractmethod
    def decode(self) -> Any:
        '''Returns the standard python representation of a Json value.'''
        pass

class JsonLiteral(JsonValue):
    ''' The class of objects represented by the strings 'true', 'false' or 'null'.
    '''

    def decode(self) -> Any:
        ''' Returns the python object associated with the JsonLiteral:
        'true' -->  True, 'false' --> False, 'null' -->  None
        '''
        if self.value == "true":
            return True
        elif self.value == "false":
            return False
        else: # the grammar ensures that self.value == 'null'
            return None

class JsonNumber(JsonValue):
    '''The class of objects whose string representation encode a number.
    '''

    def decode(self) -> int | float:
        ''' Returns an int or a float, according to the value.
        '''
        try:
            return int(self.value)
        except ValueError:
            return float(self.value) # thanks to the grammar, should not return a ValueError
    
class JsonString(JsonValue):
    ''' The class of objects whose string representation s enclosed in double quotes.
    '''

    ESCAPED_CHARS_DICT = { # see https://www.rfc-editor.org/rfc/rfc8259, page 9
            '"'  : chr(0x22),
            '\\' : chr(0x5C), # in python, the \ must be escaped
            '/'  : chr(0x2F),
            'b'  : chr(0x08),
            'f'  : chr(0x0C),
            'n'  : chr(0x0A),
            'r'  : chr(0x0D),
            't'  : chr(0x09)
        }
    
    # a constant used when resolving utf16 surrogate pairs
    SURROGATE_OFFSET = 0x10000 - (0xD800 << 10) - 0xDC00 # thanks to https://datacadamia.com/data/type/text/surrogate

    # some regular expressions
    ESCAPED_CHAR_REGEXP = r'\\(["\\/bfnrt])'
    ESCAPED_UTF8_REGEXP = r'\\u([0-9A-Fa-f]{4})'
    ESCAPED_UTF16_SURROGATE_REGEXP = r'\\u([Dd][89abAB][0-9A-Fa-f]{2})\\u([dD][c-fC-F][0-9A-Fa-f]{2})'


    def decode(self) -> str:
        ''' Returns a normalized version of a Json string representation.
        * it is no more enclosed in double quotes
        * escaped characters ('\\n', ...) are replaced by the actual character they represent
        * escaped utf8 characters ('\\u0022') are replaced by the actual character they represent
        * utf16 surrogate pairs ('\\uD834\\uDD1E') are replaced by the actual character they represent
        '''
        return self.__sub_escaped_char(
                        self.__sub_escaped_utf8(
                                self.__sub_utf16_surrogates(self.value[1:-1])))

    
    @classmethod
    def __sub_escaped_char(cls, inpustr: str) -> str:
        def substitute(match):
            return cls.ESCAPED_CHARS_DICT[match.group(1)]
        return re.sub(cls.ESCAPED_CHAR_REGEXP, substitute, inpustr)
    
    @classmethod
    def __sub_escaped_utf8(cls, inputstr: str) -> str:
        def substitute(match):
            return chr(int(match.group(1), 16))
        return re.sub(cls.ESCAPED_UTF8_REGEXP, substitute, inputstr)
    
    @classmethod
    def __sub_utf16_surrogates(cls, inputstr: str) -> str:
        def substitute(match):
            #print("substituting: {}".format(match.group(0)))
            lead, trail = int(match.group(1), 16), int(match.group(2), 16)
            #if 0xD800 <= lead < 0xDC00 <= trail <= 0xDFFF:
            return chr((lead << 10) + trail + cls.SURROGATE_OFFSET)
            #else:
            #    return match.group(0).lower()
        return re.sub(cls.ESCAPED_UTF16_SURROGATE_REGEXP, substitute, inputstr)
    

class JsonObject(JsonValue):
    ''' The class of objects represented by a string of form '{name1: value1, name2: value2, ..., nameN: valueN}'.
    '''
    def decode(self) -> dict:
        ''' Returns a python dictionary.
        '''
        return {member.name.decode() : member.value.decode()  for member in self.value}

class JsonArray(JsonValue):
    ''' The class of objects represented by a string of form '[value1, value2, ..., valueN]'
    '''

    def decode(self) -> list:
        ''' Returns a python list.
        '''
        return [value.decode() for value in self.value]