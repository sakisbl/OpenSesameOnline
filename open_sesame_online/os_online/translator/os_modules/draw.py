# -*- coding: ascii -*-
"""
#==============================================================================
#title           :draw.py
#description     :This class represents an OpenSesame Draw statement
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
import shlex
from os_online.translator.os_modules.statement import Statement

class Draw(Statement):
    """ This class models a draw statement for open sesame.
    The draw statement has a couple of arguments.
    This depends on the first argument: what to draw
    Draw subclasses Statement
    """

    # The pattern for extra keywords that can be added to a draw instance,
    # follows the form: word=(word or number or text in parentheses)
    KEYWORD_PAT = re.compile(r"^(\w+)=(-?\d+\.\d+|-?\d+|" +
                             r"\w+|\".+?\"|\'.+?\'|\[\w+?\])$")
    SPLIT_PAT = re.compile(r'\w+=\w+|\w+=\".*?\"')

    def _get_patterns(self):
        """ Get a dictionaty  matching the draw types to patterns """
        patterns = {
        'ellipse' : self._compile_pattern('ellipse'),
        'line' : self._compile_pattern('line'),
        'arrow' : self._compile_pattern('arrow'),
        'circle' : self._compile_pattern('circle'),
        'textline' : self._compile_pattern('textline'),
        'image' : self._compile_pattern('image'),
        'gabor' : self._compile_pattern('gabor'),
        'noise' : self._compile_pattern('noise'),
        'fixdot' : self._compile_pattern('fixdot')
        }
        return patterns

    @staticmethod
    def _compile_pattern(pattern_type):
        """ Create a patterns suitable for the given type. Possible drawable
        types are:
        ellipse, line, arrow, circle, textline, image, gabor, noise and fixdot.
        """
        variable = r"\[\w+?\]"
        key = r"^(draw)\s+("+pattern_type+r")"
        number = r"\s+(-\d+\.\d+|-\d+|\d+\.\d+|\d+|"+variable+")"
        text = r"\s+(\w+|\".+?\"|\'.+?\'|"+variable+")"
        textstring = r"\s+(\w+|\".*?\"|\'.*?\'|"+variable+")"
        keywords = r"(?P<keywords>.+)?$"
        if pattern_type in ("ellipse", "line", "arrow"):
            return re.compile(key+number+number+number+number+keywords)
        elif pattern_type == "circle":
            return re.compile(key+number+number+number+keywords)
        elif pattern_type == "image":
            return re.compile(key+number+number+text+keywords)
        elif pattern_type == "textline":
            return re.compile(key+number+number+textstring+keywords)
        elif pattern_type in ("gabor", "noise", "fixdot"):
            return re.compile(key+number+number+keywords)
        return None

    def _get_match(self, line):
        """ This function will check if the given line matches any of the draw
        types. If it does, it this returns the matching regex
        line -- the line to match
        """
        patterns = self._get_patterns()
        for pattern in patterns.values():
            match = pattern.match(line)
            if match:
                try:
                    keywords = match.group('keywords')
                    words = re.findall(self.SPLIT_PAT, keywords)
                except ValueError:
                    return match
                for word in words:
                    key_match = self.KEYWORD_PAT.match(word)
                    if not key_match:
                        return None
                    return match
        return None

    def _get_keywords(self, keywords_list):
        """ When a list of keyword pair strings (in the form key="word" etc) is
        supplied, this function will return a dictionary of key value pairs
        """
        keywords = {}
        for keyword in keywords_list:
            match = self.KEYWORD_PAT.match(keyword)
            name = match.group(1)
            value = match.group(2)
            keywords[name] = value
        return keywords

    def __init__(self, line):
        """ Initialize with a valid string that fits the pattern for this class.
        If this fails, a Value error wil be thrown
        All parameters and keywords will be read from line and stored as
        instance variables in the parameters and keywords dicts.
        """
        exp = self._get_match(line)
        if not exp:
            raise ValueError("The provided line was not a valid draw statement")

        self.os_type = "draw"
        self.parameters = {}
        self.parameters['type'] = exp.group(2)

        # pylint: disable=bad-whitespace
        if self.parameters['type'] == 'ellipse':
            self.parameters['left']     = exp.group(3)
            self.parameters['top']      = exp.group(4)
            self.parameters['width']    = exp.group(5)
            self.parameters['height']   = exp.group(6)
        elif self.parameters['type'] == 'circle':
            self.parameters['x']        = exp.group(3)
            self.parameters['y']        = exp.group(4)
            self.parameters['radius']   = exp.group(5)
        elif self.parameters['type'] in ('line','arrow'):
            self.parameters['left']     = exp.group(3)
            self.parameters['right']    = exp.group(4)
            self.parameters['top']      = exp.group(5)
            self.parameters['bottom']   = exp.group(6)
        elif self.parameters['type'] == 'textline':
            self.parameters['x']        = exp.group(3)
            self.parameters['y']        = exp.group(4)
            self.parameters['text']     = exp.group(5)
        elif self.parameters['type'] == 'image':
            self.parameters['x']        = exp.group(3)
            self.parameters['y']        = exp.group(4)
            self.parameters['path']     = exp.group(5)
        elif self.parameters['type'] in ('gabor','noise','fixdot'):
            self.parameters['x']        = exp.group(3)
            self.parameters['y']        = exp.group(4)

        self.keywords = {}
        try:
            keyword_list  = exp.group('keywords')
        except IndexError:
            pass
        else:
            if keyword_list:
                splitted = re.findall(self.SPLIT_PAT, keyword_list)
                self.keywords = self._get_keywords(splitted)

        Statement.__init__(self, self.os_type, self.parameters, self.keywords)
