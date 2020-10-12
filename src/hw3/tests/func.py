"""
This script contains 10 unit tests
"""





import unittest
import re
from ..func import *

class AnalysisTestCase(unittest.TestCase):

    def test1(self):
        name = cap_and_split_names("pinkie")

        self.assertEqual(name, ['Pinkie', 'Pie'])

    def test2(self):
        name = cap_and_split_names("applejack")

        self.assertEqual(name,"Applejack")

    def test3(self):
        name = 'ice'
        flag = if_mentioend(name,compile_name_regex(name), "I like ice-cream.")

        self.assertEqual(flag,1)

    def test4(self):
        name = 'love'
        flag = if_mentioend(name,compile_name_regex(name), "I like ice-cream.")
        
        self.assertEqual(flag,0)

    def test5(self):
        name = 'ice'
        flag = if_mentioend(name,compile_name_regex(name), "Ilikeicecream.")

        self.assertEqual(flag,0)

    def test6(self):
        reg = compile_name_regex("name")

        self.assertNotEqual(reg, re.compile("name"))

    def test7(self):
        d = {'a': 0.1,'b': 0.2, 'c': 0.3}
        d1 = normalize_dict(d, target=1.0)

        #self.assertEqual(sum(list(d1.values())),1)
        self.assertEqual(sum([float(elem) for elem in list(d1.values())]),1)

    def test8(self):
        d = {'a': 1,'b': 2, 'c': 3}
        d1 = normalize_dict(d, target=1.0)

        #self.assertEqual(sum(list(d1.values())),1)
        self.assertEqual(sum([float(elem) for elem in list(d1.values())]),1)

    def test9(self):
        d = {'a': 1,'b': 2, 'c': 3}
        d1 = normalize_dict(d, target=2.0)

        self.assertEqual(sum([float(elem) for elem in list(d1.values())]),2)

    def test10(self):
        tmp_dict = create_analysis({'a': 0.1},{'b': 0.1},{'c': 0.1},{'d': 0.1})

        self.assertEqual(list(tmp_dict.keys()),['verbosity', 'mentions', 'follow_on_comments', 'non_dictionary_words'])
