# -*- coding: ascii -*-
"""
#==============================================================================
#title           :run.py
#description     :This class represents an OpenSesame Run statement
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

class Run(Statement):
    """ This class models a Run for open sesame.
    This subclasses a Statement
    """

    @staticmethod
    def _get_pattern():
        """ Gets the regex pattern that identifies a run"""
        key = r"^(run)\s+"
        name = r"(\w+)\s*"
        value = r"(\w+|\".+\"|\'.+\')*\s*$"
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
            raise ValueError("The provided line was not a valid Run")

        self.os_type = "run"
        self.parameters = {}
        self.parameters['name'] = exp.group(2)
        try:
            self.parameters['condition'] = exp.group(3)
        except IndexError:
            pass

        Statement.__init__(self, self.os_type, self.parameters)
