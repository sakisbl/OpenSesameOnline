# -*- coding: ascii -*-
"""
#==============================================================================
#title           :test_define.py
#description     :Test the os_modules.define.py module
#author          :OpenSesame group of GipHouse 2014, Radboud University
#programmers     :Ben Bruecker, Laurens van Bercken
#date            :20140419
#version         :0.1
#usage           :python ../translator.py
#notes           :
#python_version  :2.7
#==============================================================================
"""
import unittest
from os_online.translator.os_modules.define import Define
import os_online.translator.unit_tests.os_module_util as util

class DefineTestCase(unittest.TestCase):
    """ This testcase tests the os_modules.define class
    """

    # pylint: disable=too-many-public-methods
    # There are many public methods because of inheritance from TestCase
    def setUp(self):
        """ This function is always run before every test case """
        succes_patterns = [
        ['define', 'name', 'name'],
        ]
        fail_patterns = [
        ['notdef', 'name', 'name'],
        ['define', 'name_inc', 'name_inc'],
        ['define', 'name', 'name_inc'],
        ['define', 'name_inc', 'name'],
        ]
        self.samples = util.os_mod_set_up(succes_patterns, fail_patterns)

    def test_correct_initialization(self):
        """ Checks whether define succesfully inits for success cases """
        util.test_correct_initialization(self, self.samples[0], Define,\
                'define', ['name', 'type'], has_attributes=True)

    def test_correct_failure(self):
        """ Tests if incorrect strings indeed throw errors """
        util.test_correct_failure(self, Define, self.samples[1])

if __name__ == '__main__':
    unittest.main()
