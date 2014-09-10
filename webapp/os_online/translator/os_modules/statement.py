# -*- coding: ascii -*-
"""
#==============================================================================
#title           :statement.py
#description     :This class represents an OpenSesame statement
#author          :OpenSesame group of GipHouse 2014, Radboud University
#programmers     :Ben Bruecker, Laurens van Bercken
#date            :20140419
#version         :0.1
#usage           :python ../translator.py
#notes           :
#python_version  :2.7
#==============================================================================
"""
import re

class Statement(object):
    """ This is a superclass for all types of OpenSesame statements
    It provides a get, append and debug print method
    """

    def __init__(self, os_type, parameters, keywords=None,
                 has_extra_attributes=False):
        """ Initialize this statement
        os_type
        parameters
        keywords
        has_extra_attributes
        """
        self.os_type = os_type
        self.parameters = parameters
        self.keywords = keywords
        self.has_extra_attributes = has_extra_attributes
        self.attributes = None

    def get(self, name):
        """ Gets a variable by looking up its name, first in the parameters,
        then in the keywords.
        If there is a match, return a float, int or string, depending on a
        naive pattern match of the variable. If nothing fits return None
        """
        float_pattern = re.compile(r'^\d+\.\d+$')
        int_pattern = re.compile(r'^\d+$')
        text_pattern = re.compile(r'^\w+$|^\'\w+\'$|\^"\w+\"$')
        comment_pattern = re.compile(r'.+')
        value = None
        if name in self.parameters:
            value = self.parameters[name]
        elif self.keywords:
            if name in self.keywords:
                value = self.keywords[name]
        if value:
            if float_pattern.match(value):
                return float(value)
            elif int_pattern.match(value):
                return int(value)
            elif text_pattern.match(value):
                return re.sub(r'^"|^\'|\'$|"$', '', value)
            elif comment_pattern.match(value):
                return re.sub(r'^"|^\'|\'$|"$', '', value)
        return None

    def append(self, statement):
        """ Appends a statement to a statement that can have extra attributes
        statement -- the statement to append
        """
        if not self.has_extra_attributes:
            raise ValueError("You try to append a statement to " +\
                             self.os_type +
                             " that is not able to have extra attributes")
        if not self.attributes:
            self.attributes = []
        self.attributes.append(statement)

    def print_self(self, _is_attribute=False):
        """ For debugging, prints the values of this instance """
        spacing = ""
        if _is_attribute:
            print "----Attribute:----"
            spacing = "    "

        print spacing + self.os_type + ":"
        if self.parameters:
            for key in self.parameters:
                print spacing + "--P: " + key + " = " + str(self.get(key))
        if self.keywords:
            for key in self.keywords:
                print spacing + "--K: " + key + " = " + str(self.get(key))
        if self.attributes:
            for attr in self.attributes:
                attr.print_self(True)
