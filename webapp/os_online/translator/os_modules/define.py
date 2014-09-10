# -*- coding: ascii -*-
"""
#==============================================================================
#title           :define.py
#description     :This class represents an OpenSesame Define statement
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

class Define(Statement):
    """ This class models a Define for open sesame.
    It has a name and a type, and a list of attributes
    This subclasses a Statement
    """

    @staticmethod
    def _get_pattern():
        """ The pattern for a define element """
        key = r"^\s*(define)\s+"
        ptype = r"(\w+)\s+"
        name = r"(\w+)\s*$"
        pattern = re.compile(key+ptype+name)
        return pattern

    def __init__(self, line):
        """
        Initialize with a valid string that fits the pattern for this class.
        If this fails, a Value error will be thrown
        """
        pattern = self._get_pattern()
        exp = pattern.match(line)
        if not exp:
            raise ValueError("{} was not a valid Define"\
                    .format(line))
        # Strip the quotes from the name
        self.os_type = "define"
        self.parameters = {}
        self.parameters['type'] = exp.group(2)
        self.parameters['name'] = exp.group(3)

        Statement.__init__(self, self.os_type, self.parameters,
                        has_extra_attributes=True)
