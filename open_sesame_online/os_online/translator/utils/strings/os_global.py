# -*- coding: ascii -*-
"""
#==============================================================================
#title           :os_global.py
#description     :Create JavaScript literals global OpenSesame output
#author          :OpenSesame group of GipHouse 2014, Radboud University
#programmers     :Ben Bruecker, Laurens van Bercken
#date            :20140419
#version         :0.1
#usage           :python ../translator.py
#notes           :
#python_version  :2.7
#==============================================================================
"""
import os_online.translator.utils.strings.string_literals as strlit

def get_initial_text(width, height):
    """ Get the initial text for the top of the JS file.
    width  -- The window width in px
    height -- the window height in px
    """
    return strlit.INITIAL_TEXT.format(width, height)

def get_global_js(statements):
    """ Gets the JS for the global variables
    statements -- a list of 'set' statements
    """
    result = ""
    f_string = strlit.JS_DICT['global_var']
    for statement in statements:
        if not statement.os_type == 'set':
            raise Exception('Not a global statement!')
        if not result == '':
            result += '\n'
        result += f_string.format(statement.get('name'),\
                                  statement.get('value'))
    result = strlit.GLOBAL_VARS.format(result)
    return result

