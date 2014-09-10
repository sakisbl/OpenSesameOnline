# -*- coding: ascii -*-
"""
#==============================================================================
#title           :comment_strings.py
#description     :Create Comment literals for OpenSesame Online
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

def get_comment(item):
    """ Gets the Comment representation for a os_online statement """
    f_string = strlit.COMMENT_DICT[item.os_type]
    if item.os_type == 'set':
        return f_string.format(item.get('name'), item.get('value'))
    elif item.os_type == 'comment':
        return f_string.format(item.get('comment'))
    elif item.os_type == 'run':
        value = item.get('name')
        if item.get('condition'):
            value += " " + item.get('condition')
        return f_string.format(value)
    elif item.os_type == 'define':
        value = f_string.format(item.get('type'), item.get('name'))
        if item.attributes:
            for attr in item.attributes:
                value += get_comment(attr) + '\n'
        return value
    else:
        return f_string

def get_unimp(define, p_map):
    """ Generates JavaScript comments for unimplemented parameters of a
    define
    define -- a OS Define statement
    p_map  -- the parameter map for this type of define statement
    """
    if not define.attributes:
        return ""
    c_string = ""
    unimp = [x for x in define.attributes if not (x.os_type == 'set' and\
                                             x.get('name') in p_map) and
                                             not x.os_type in p_map]
    for current in unimp:
        c_string = seperator(c_string, ',\n')
        c_string += get_comment(current)
    if not c_string == "":
        c_string = strlit.UNUSED.format(c_string)
    return c_string

def seperator(string, delim=', '):
    """ Creates a comma after the given string if it is not empty. Also
    adds a newline if that parameter is true
    """
    if not string == "":
        string += delim
    return string
