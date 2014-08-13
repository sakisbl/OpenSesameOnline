# -*- coding: ascii -*-
"""
#==============================================================================
#title           :multiline.py
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

class Multiline(Statement):
    """ This class models a multi-line variable for open sesame.
    It begins with __variable-name__ and ends with __end__
    This subclasses Statement
    """

    is_multiline = True

    @staticmethod
    def _get_pattern():
        """ Gets the pattern that defines a multiline start """
        pattern = r"^__(.+)__$"
        pattern = re.compile(pattern)
        return pattern

    def addline(self, line):
        """ Adds a line to this multiline statement
        This sets done to true if __end__ is encountered
        line -- the line to be added
        """
        if not line == "__end__":
            if not self.done:
                if not self.parameters['lines'] == "":
                    self.parameters['lines'] += "\n"
            self.parameters['lines'] += line
        else:
            self.done = True

    def is_done(self):
        """ Gets wheter this multiline has been closed """
        return self.done

    def __init__(self, line):
        """ Initialize with a valid string that fits the pattern for this class
        If this fails, a Value error will be thrown
        """
        self.done = False
        pattern = self._get_pattern()
        exp = pattern.match(line)
        if not exp:
            raise ValueError("The provided line was not a valid Multiline")
        # Strip the quotes from the name
        self.os_type = "multi-line"
        self.parameters = {}
        self.parameters['name'] = exp.group(1)
        self.parameters['lines'] = ""

        Statement.__init__(self, self.os_type, self.parameters)
