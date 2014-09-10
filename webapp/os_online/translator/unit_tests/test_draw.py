# -*- coding: ascii -*-
"""
#==============================================================================
#title           :test_draw.py
#description     :Test the os_modules.draw.py module
#author          :OpenSesame group of GipHouse 2014, Radboud University
#programmers     :Ben Bruecker, Laurens van Bercken
#date            :20140505
#version         :0.1
#usage           :python ../translator.py
#notes           :
#python_version  :2.7
#==============================================================================
"""
import unittest
from os_online.translator.os_modules.draw import Draw
import os_online.translator.unit_tests.os_module_util as util

class DrawTestCase(unittest.TestCase):
    """ This testcase tests the os_modules.draw class
    """

    # pylint: disable=too-many-public-methods
    # There are many public methods because of inheritance from TestCase
    def setUp(self):
        """ This function is always run before every test case """
        succes_patterns = [
        # draw with 4 numbers followed by keyword(s): ellipse, line and arrow
        ['draw', 'ellipse', 'number', 'number', 'number', 'number', 'keyword'],
        ['draw', 'line', 'number', 'number', 'number', 'number', 'keyword'],
        ['draw', 'arrow', 'number', 'number', 'number', 'number', 'keyword'],
        # draw element with 3 numbers followed by keyword(s): circle
        ['draw', 'circle', 'number', 'number', 'number', 'keyword'],
        # draw element with 2 numbers followed by a text: textline and image
        ['draw', 'textline', 'number', 'number', 'text'],
	['draw', 'image', 'number', 'number', 'text'],
        # draw element with 2 numbers: gabor, noise and fixdot
	['draw', 'gabor', 'number', 'number'],
        ['draw', 'noise', 'number', 'number'],
        ['draw', 'fixdot', 'number', 'number'],
        ]
        fail_patterns = [
	    ['draw', 'notcircle', 'number', 'number', 'number', 'keyword'],
            ['draw', 'circle', 'number_inc', 'number', 'number', 'keyword'],
	    ['draw', 'circle', 'number', 'number_inc', 'number', 'keyword'],
	    ['draw', 'circle', 'number', 'number', 'number_inc', 'keyword'],
	    ['draw', 'circle', 'number', 'number', 'number', 'keyword_inc']
            ['notdraw', 'fixdot', 'number', 'number'],
            ] # there are a lot of other fail patterns!
        self.samples = util.os_mod_set_up(succes_patterns, fail_patterns)

    def test_correct_initialization(self):
        """ Checks whether draw succesfully inits for success cases """
        util.test_correct_initialization(self, self.samples[0], Draw,\
                'draw', ['type', 'x', 'y'])

    def test_correct_failure(self):
        """ Tests if incorrect strings indeed throw errors """
        util.test_correct_failure(self, Draw, self.samples[1])

if __name__ == '__main__':
    unittest.main()
