# -*- coding: ascii -*-
"""
#==============================================================================
#title           :setcycle.py
#description     :This class represents an OpenSesame Setcycle statement
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

class Setcycle(Statement):
    """ This class models a setsycle statement for open sesame.
    It consist of the word setcycle, the number of the cycle,
    the variable name and last value.
    This subclasses Statement
    """

    @staticmethod
    def _get_pattern():
        """ Gets the pattern representing a setcycle """
        key = r"^(setcycle)\s+"
        cyclenumber = r"(\d+)\s+"
        name = r"(\w+)\s+"
        value = r"(\w+$|\'.+\'$|\".+\"$)"
        pattern = re.compile(key+cyclenumber+name+value)
        return pattern

    def __init__(self, line):
        """ Initialize with a valid string that fits the pattern for this class
        If this fails, a Value error will be thrown
        """
        pattern = self._get_pattern()
        exp = pattern.match(line)
        if not exp:
            raise ValueError("The provided line was not a valid setcycle")

        self.os_type = "setcycle"
        self.parameters = {}
        self.parameters['cyclenumber'] = exp.group(2)
        self.parameters['name'] = exp.group(3)
        self.parameters['value'] = exp.group(4)

        Statement.__init__(self, self.os_type, self.parameters)
