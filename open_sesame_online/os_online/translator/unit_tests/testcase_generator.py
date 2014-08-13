# -*- coding: ascii -*-
"""
#==============================================================================
#title           :testcase_generator.py
#description     :This class can create a test sample set for os classes
#author          :OpenSesame group of GipHouse 2014, Radboud University
#programmers     :Ben Bruecker, Laurens van Bercken
#date            :20140419
#version         :0.1
#usage           :python ../translator.py
#notes           :
#python_version  :2.7
#==============================================================================
"""
from os_online.translator.unit_tests.string_gen import TestStringGenerator

class TestSet(object):
    """ Testset creates a set of test variables that can be used to test
    open sesame online modules
    """

    file_mapping = {
        'number' : './dict/numbers.txt',
        'number_inc' : './dict/incorrect_numbers.txt',
        'name' : './dict/names.txt',
        'name_inc' : './dict/incorrect_names.txt',
        'text' : './dict/text.txt',
        'text_inc' : './dict/incorrect_text.txt',
        'keyword' : './dict/keywords.txt',
        'keyword_inc' : './dict/incorrect_keywords.txt',
        'condition' : './dict/conditions.txt',
        'condition_inc' : './dict/incorrect_conditions.txt'
    }

    # pylint: disable=too-few-public-methods
    def __init__(self, amount, max_length):
        """ Initializes all values for a testcase. Amount is the number of
        samples to be generated for each category. Max length is the maximum
        word length to be tested
        """
        self.testset = {}
        TestStringGenerator(amount, max_length, self.file_mapping, force=True)
        self.init_testset()

    def init_testset(self):
        """ Initializes the testset """
        for key in self.file_mapping:
            self.testset[key] = CaseReader(self.file_mapping[key])

    def get_testcase(self, testcase):
        """ Gets a testcase. The testcase supplied should a list, for example
        ["set","name","number"]. if one of the values matches
        name, name_inc, text, text_inc, number, number_inc, keyword or
        keyword_inc, then a random value from that will be used, otherwise
        the name itself (set in this case) will be used literally
        """
        result = ""
        for case in testcase:
            if not result == "":
                result += " "
            if case in self.testset:
                to_add = self.testset[case].get_line()
                if not to_add:
                    self.init_testset()
                    to_add = self.testset[case].get_line()
                result += to_add
            else:
                result += case
        return result


class CaseReader(object):
    """ Very simple file reader for testcases """
    # pylint: disable=too-few-public-methods
    def __init__(self, fname):
        """ Initializes the reader
        IMPORTANT! Very naive function for testing. No checking
        on the file is done
        """
        self.filename = fname
        self.lines = open(fname, 'r').readlines()

    def get_line(self):
        """ Gets the next line from the reader.
        If that is the last line, will keep returning that
        """
        if len(self.lines) > 0:
            return self.lines.pop(0).rstrip('\n')
