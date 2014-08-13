# -*- coding: ascii -*-
"""
#==============================================================================
#title           :test_widget.py
#description     :Test the os_modules.widget.py module
#author          :OpenSesame group of GipHouse 2014, Radboud University
#programmers     :Ben Bruecker, Laurens van Bercken
#date            :20140506
#version         :0.1
#usage           :python ../translator.py
#notes           :
#python_version  :2.7
#==============================================================================
"""
import unittest
from os_online.translator.os_modules.widget import Widget
import os_online.translator.unit_tests.os_module_util as util

class WidgetTestCase(unittest.TestCase):
    """ This testcase tests the os_modules.widget class
    """

    # pylint: disable=too-many-public-methods
    # There are many public methods because of inheritance from TestCase
    def setUp(self):
        """ This function is always run before every test case """
        succes_patterns = [
            # there are 7 types of widgets: button, checkbox, image,
            # image_button, label,
            # rating_scale and text_input
            ['widget', 'number', 'number', 'number',\
                    'number', 'button', 'keyword'],
            ['widget', 'number', 'number', 'number',\
                    'number', 'checkbox', 'keyword'],
            ['widget', 'number', 'number', 'number',\
                    'number', 'image', 'keyword'],
            ['widget', 'number', 'number', 'number',\
                    'number', 'image_button', 'keyword'],
            ['widget', 'number', 'number', 'number',\
                    'number', 'label', 'keyword'],
            ['widget', 'number', 'number', 'number',\
                    'number', 'rating_scale', 'keyword'],
            ['widget', 'number', 'number', 'number',\
                    'number', 'text_input', 'keyword'],
            ]
        fail_patterns = [
            ['notwidget', 'number', 'number', 'number',\
                    'number', 'button', 'keyword'],
	    ['widget', 'number_inc', 'number', 'number',\
                    'number', 'button', 'keyword'],
        ]
        self.samples = util.os_mod_set_up(succes_patterns, fail_patterns)

    def test_correct_initialization(self):
        """ Checks whether widget succesfully inits for success cases """
        util.test_correct_initialization(self, self.samples[0], Widget,\
                'widget', ['column', 'row', 'column_span', 'row_span',\
                'type', 'keywords'])

    def test_correct_failure(self):
        """ Tests if incorrect strings indeed throw errors """
        util.test_correct_failure(self, Widget, self.samples[1])

if __name__ == '__main__':
    unittest.main()
