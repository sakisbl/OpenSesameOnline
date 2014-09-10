# -*- coding: ascii -*-
"""
#==============================================================================
#title           :log.py
#description     :This class represents an OpenSesame Log statement
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

class Log(Statement):
    """ This class models a log statement for open sesame.
    It consist of the word log followed by a variable (name)
    This subclasses Statement
    """

    @staticmethod
    def _get_pattern():
        """ Gets the pattern that defines a Log statement """
        key = r"^(log)\s+"
        value = r"(\w+$|\'.+\'$|\".+\"$)"
        pattern = re.compile(key+value)
        return pattern

    def __init__(self, line):
        """
        Initialize with a valid string that fits the pattern for this class.
        If this fails, a Value error will be thrown
        """
        pattern = self._get_pattern()
        exp = pattern.match(line)
        if not exp:
            raise ValueError("The provided line was not a valid log statement")
        self.os_type = "log"
        self.parameters = {}
        self.parameters['name'] = exp.group(2)

        Statement.__init__(self, self.os_type, self.parameters)
