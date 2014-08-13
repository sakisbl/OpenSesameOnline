# -*- coding: ascii -*-
"""
#==============================================================================
#title           :test_multiline.py
#description     :Test the os_modules.multiline.py module
#author          :OpenSesame group of GipHouse 2014, Radboud University
#programmers     :Ben Bruecker, Laurens van Bercken
#date            :20140514
#version         :0.1
#usage           :python ../translator.py
#notes           :
#python_version  :2.7
#==============================================================================
"""
import unittest
import random
from os_online.translator.os_modules.multiline import Multiline
from os_online.translator.unit_tests.testcase_generator import TestSet
import os_online.translator.unit_tests.os_module_util as util

class MultilineTestCase(unittest.TestCase):
    """ This testcase tests the os_modules.multiline class
    """

    # pylint: disable=too-many-public-methods
    # There are many public methods because of inheritance from TestCase
    def setUp(self):
        """ This function is always run before every test case """
        succes_patterns = [
            ['text'],
            ]
        fail_patterns = [
            ['text_inc'],
            ]
        self.samples = util.os_mod_set_up(succes_patterns, fail_patterns)

    def create_ml_testcase(self):
        """ Creates a special multi-line testcase """
        pool_size = 500
        max_length = 60
        t_set = TestSet(pool_size, max_length)
        succes = []
        for _ in xrange(0, 50):
            s_tests = []
            s_tests.append('__' + t_set.get_testcase('name') + '__')
            for _ in xrange(0, random.randint(0, 50)):
                if not self.samples[0]:
                    s_tests.append(self.samples[0].pop())
            s_tests.append('__end__')
            succes.append(s_tests)
        return s_tests

    def test_correct_initialization(self):
        """ Checks whether multiline succesfully inits for success cases """
        s_tests = self.create_ml_testcase()
        for _ in s_tests:
            util.test_correct_initialization(self, self.samples[0], Multiline,\
                'multi-line', ['name', 'lines'])

    def test_correct_failure(self):
        """ Tests if incorrect strings indeed throw errors """
        util.test_correct_failure(self, Multiline, self.samples[1])

if __name__ == '__main__':
    unittest.main()
