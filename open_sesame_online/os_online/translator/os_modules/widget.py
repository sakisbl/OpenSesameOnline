# -*- coding: ascii -*-
"""
#==============================================================================
#title           :widget.py
#description     :This class represents an OpenSesame Widget statement
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

class Widget(Statement):
    """ This class models a widget statement for open sesame.
    It consist of the word widget followed by:
    4 integers: [column] [row] [column span] [row span]
    widget type and a list of keywords
    This subclasses a Statement
    """

    # The pattern for extra keywords that can be added to a widget instance,
    # It follows the form: word=(word or number or text in parentheses)
    KEYWORD_PAT = re.compile(r"^(\w+)=(-?\d+\.\d+|-?\d+|\w+|\".+\"|\'.+\')$")

    @staticmethod
    def _get_pattern():
        """ Possible widget types are: button, checkbox, image,
        image_button, label, rating_scale and text_input
        """
        key = r"^(widget)\s+"
        column = r"(\d+)\s+"
        row = r"(\d+)\s+"
        column_span = r"(\d+)\s+"
        row_span = r"(\d+)\s+"
        widget_type = r"(button|checkbox|image|image_button|label|\
        rating_scale|text_input)"
        keywords = r"(?P<keywords>.+)?"
        pattern = re.compile(key+column+row+column_span+
                             row_span+widget_type+keywords)
        return pattern

    def _get_keywords(self, keywords_list):
        """ When a list of keyword pair strings (in the form key="word" etc)
        is supplied, this function will return a dictionary of key value pairs
        """
        keywords = {}
        for keyword in keywords_list:
            match = self.KEYWORD_PAT.match(keyword)
            name = match.group(1)
            value = match.group(2)
            keywords[name] = value
        return keywords

    def __init__(self, line):
        """ Initialize with a valid string that fits the pattern for this class
        If this fails, a Value error will be thrown
        """
        pattern = self._get_pattern()
        exp = pattern.match(line)
        if not exp:
            raise ValueError("The provided line was not a valid widget")
        self.os_type = "widget"
        self.parameters = {}
        self.parameters['column'] = exp.group(2)
        self.parameters['row'] = exp.group(3)
        self.parameters['column_span'] = exp.group(4)
        self.parameters['row_span'] = exp.group(5)
        self.parameters['type'] = exp.group(6)

        self.keywords = {}
        try:
            keyword_list = exp.group('keywords')
        except IndexError:
            pass
        else:
            if keyword_list:
                self.keywords = self._get_keywords(keyword_list.split())

        Statement.__init__(self, self.os_type, self.parameters, self.keywords)
