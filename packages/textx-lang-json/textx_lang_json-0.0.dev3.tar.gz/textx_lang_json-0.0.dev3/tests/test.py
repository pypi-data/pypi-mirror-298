''' test.py
(c) Jean-François Baget, 2024

Everything I thought about in order to test the decode() method. 
'''
import unittest
from textx import metamodel_for_language
import json
import unicodedata

def exists(character):
    ''' Tests if a character exists in the unicode table.
    '''
    try:
        unicodedata.name(character)
        return True
    except ValueError:
        return False


class TestNumbers(unittest.TestCase):

    def setUp(self):
        self.parser = metamodel_for_language('textxjson')

    def test_integers(self):
        ''' Testing some integers. They should be decoded as int, and should have the same result as json.loads().
        '''
        data = ['2', '-3', str(-(2**53)+1), str((2**53)-1), str(12*10**1500)]
        for rep in data:
            textx = self.parser.model_from_str(rep).decode()
            python = json.loads(rep)
            self.assertIsInstance(textx, int)
            self.assertIsInstance(python, int)
            self.assertEqual(textx, python)

            
    def test_floats(self):
        data = ['2.0', '-3.7', '3.141592653589793238462643383279', '1e-3', '1E+3', '1E3', '0.627E-1500']
        for rep in data:
            textx = self.parser.model_from_str(rep).decode()
            python = json.loads(rep)
            self.assertIsInstance(textx, float)
            self.assertIsInstance(python, float)
            self.assertEqual(textx, python)

class TestLiterals(unittest.TestCase):

    def setUp(self):
        self.parser = metamodel_for_language('textxjson')

    def test_true(self):
        rep = 'true'
        textx = self.parser.model_from_str(rep).decode()
        python = json.loads(rep)
        self.assertEqual(textx, python)
        self.assertEqual(textx, True)

    def test_false(self):
        rep = 'false'
        textx = self.parser.model_from_str(rep).decode()
        python = json.loads(rep)
        self.assertEqual(textx, python)
        self.assertEqual(textx, False)

    def test_null(self):
        rep = 'null'
        textx = self.parser.model_from_str(rep).decode()
        python = json.loads(rep)
        self.assertEqual(textx, python)
        self.assertEqual(textx, None)

class TestStrings(unittest.TestCase):

    def setUp(self):
        self.parser = metamodel_for_language('textxjson')

    def test_escaped_chars(self):
        data = ['"\\""', r'"\""', '"\\\\"', r'"\\"', '"\\/"', r'"aaaa\b\b\bbb"', r'"\f"', r'"\r"', r'"\n"', r'"\t"']
        for rep in data:
            textx = self.parser.model_from_str(rep).decode()
            python = json.loads(rep)
            self.assertEqual(textx, python)

    def test_all_existing_utf8_characters(self):
        listchars = ['"', chr(0x20), chr(0x21)]
        listchars.extend([chr(n) for n in range(0x23, 0x5C) if exists(chr(n))])
        listchars.extend([chr(n) for n in range(0x5D, 0x110000) if exists(chr(n))])
        listchars.append('"')
        bigstr = "".join(listchars)
        textx = self.parser.model_from_str(bigstr).decode()
        python = json.loads(bigstr)
        self.assertEqual(textx, python)

    def test_a_non_existing_utf8_character(self):
        missing = chr(0x07B8)
        if exists(missing):
            print("Should change the test, there has been a unicode change.")
        else:
            strmissing = '"{}"'.format(missing)
            textx = self.parser.model_from_str(strmissing).decode()
            python = json.loads(strmissing)
            self.assertEqual(textx, python)

    def test_utf16_surrogate_pairs(self):
        surrogate = r'"\uD834\uDD1E"'
        character = r'"𝄞"'
        textxsurr = self.parser.model_from_str(surrogate).decode()
        pythonsurr = json.loads(surrogate)
        textxchar = self.parser.model_from_str(character).decode()
        pythonchar = json.loads(character)
        self.assertEqual(textxsurr, pythonsurr)
        self.assertEqual(pythonsurr, textxchar)
        self.assertEqual(textxchar, pythonchar)

    def test_utf8_surrogates_interaction(self):
        ''' Tests triples of utf8 encodings that can be L (leading), T (trailing) or otherwise S (standard).
        A pair LT can be known (k) , or unknown (u), as can any singleton that is not in such a pair.
        '''
        data = [
                r'"\uD834\uDD1E\uD834"', # (LT)kL
                r'"\uD834\uDD1E\uDD1E"', # (LT)kT
                r'"\uD834\uDD1E\u0022"', # (LT)kSk
                r'"\uD834\uDD1E\uFFFF"', # (LT)kSu
                r'"\uD800\uDC69\uD834"', # (LT)uL
                r'"\uD800\uDC69\uDD1E"', # (LT)uT
                r'"\uD800\uDC69\u0022"', # (LT)uSk
                r'"\uD800\uDC69\uFFFF"', # (LT)uSu
                r'"\uD834\uD834\uDD1E"', # L(LT)k
                r'"\uDD1E\uD834\uDD1E"', # T(LT)k
                r'"\u0022\uD834\uDD1E"', # Sk(LT)k
                r'"\uFFFF\uD834\uDD1E"', # Su(LT)k
                r'"\uD834\uD800\uDC69"', # L(LT)u
                r'"\uDD1E\uD800\uDC69"', # T(LT)u
                r'"\u0022\uD800\uDC69"', # Sk(LT)u
                r'"\uFFFF\uD800\uDC69"', # Su(LT)u
            ]
        for rep in data:
            textx = self.parser.model_from_str(rep).decode()
            python = json.loads(rep)
            self.assertEqual(textx, python)


class TestArrays(unittest.TestCase):

    def setUp(self):
        self.parser = metamodel_for_language('textxjson')

    def test_some_arrays(self):
        data = [
            '[]',
            '[1, 2, 3, 4]',
            '[[1, 2], [3, 4]]',
            r'["\uFFFF\uD800\uDC69"]'
        ]
        for rep in data:
            textx = self.parser.model_from_str(rep).decode()
            python = json.loads(rep)
            self.assertEqual(textx, python)

class TestObjects(unittest.TestCase):

    def setUp(self):
        self.parser = metamodel_for_language('textxjson')

    def test_some_objects(self):
        data = [
            '{}',
            '{"a":1, "b" : 2 , "c" : 3, "d" : 4}',
            '{"a" : {"a" : 2}, "b" : {"b": 3}}',
            '{"a" : 1, "a" : 2}',
            r'{"\uFFFF\uD800\uDC69": "\uFFFF\uD800\uDC69"}'
        ]
        for rep in data:
            textx = self.parser.model_from_str(rep).decode()
            python = json.loads(rep)
            self.assertEqual(textx, python)

    def test_override_key_in_objects(self):
        self.assertEqual(len(json.loads('{"a" : 1, "a" : 2}')), 1)

class TestSomeRealStuff(unittest.TestCase):

    def setUp(self):
        self.parser = metamodel_for_language('textxjson')

    def test_some_gw2_files(self):
        files = ["tests/maps_en.json", "tests/maps_de.json", "tests/maps_fr.json", "tests/maps_es.json", "tests/maps_zh.json"]
        for file in files:
            textx = self.parser.model_from_file(file).decode()
            with open(file, "r", encoding = 'utf-8') as f:
                python = json.load(f)
            self.assertEqual(textx, python)


    
        

   

        
        



if __name__ == '__main__':
    unittest.main()
