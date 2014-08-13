# -*- coding: ascii -*-
"""
#==============================================================================
#title           :comment.py
#description     :This class represents an OpenSesame Comment statement
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

class Comment(Statement):
    """ This class models a comment for open sesame.
    It consists of a # followed by text
    This subclasses a statement
    """

    @staticmethod
    def _get_pattern():
        """ Gets the regex pattern that identifies a comment"""
        key = r"^\s*#"
        value = r"(.*)"
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
            raise ValueError("The provided line was not a valid comment")
        self.os_type = "#"
        self.parameters = {}
        self.parameters['comment'] = exp.group(1)

        Statement.__init__(self, self.os_type, self.parameters)
