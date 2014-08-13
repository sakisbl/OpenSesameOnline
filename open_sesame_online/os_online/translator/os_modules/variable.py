# -*- coding: ascii -*-
"""
#==============================================================================
#title           :variable.py
#description     :This class represents an OpenSesame Variable statement
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
from os_online.translator.os_modules.statement import Statement

class Variable(Statement):
    """ This class models a variable for open sesame.
    This subclasses a Statement
    """

    @staticmethod
    def _get_pattern():
        """ Gets the regex pattern that identifies a variable"""
        key = r"^(set)\s+"
        name = r"(\w+)\s+"
        value = r"(-?\d+\.\d+|-?\d+|\w+|\".*?\"|\'.*?\')\s*$"
        pattern = re.compile(key+name+value)
        return pattern

    def __init__(self, line):
        """
        Initialize with a valid string that fits the pattern for this class.
        If this fails, a Value error will be thrown
        """
        pattern = self._get_pattern()
        exp = pattern.match(line)
        if not exp:
            raise ValueError("(" + line+ ") was not a valid Variable")

        self.os_type = "set"
        self.parameters = {}
        self.parameters['name'] = exp.group(2)
        self.parameters['value'] = exp.group(3)

        Statement.__init__(self, self.os_type, self.parameters)

