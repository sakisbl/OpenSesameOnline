# -*- coding: ascii -*-
"""
#==============================================================================
#title           :file_handler.py
#description     :This file is now very simple for testing purposes, it should
                  implement its functions a lot stricter once this is migrated
                  to the webapplication.
#author          :OpenSesame group of GipHouse 2014, Radboud University
#programmers     :Ben Bruecker, Laurens van Bercken
#date            :20140419
#version         :0.1
#usage           :python ../translator.py
#notes           :
#python_version  :2.7
#==============================================================================
"""
from django.core.files import File
import collections

def read_file(fname):
    """ This simple function should be extended later on. Now it just checks
    the file extension before opening and returning it wich is fine
    for local testing
    fname -- The filename to read
    """
    if not fname.endswith('.opensesame'):
        print 'Please provide a opensesame script file'
        exit()
    return open(fname, 'r')

def write(text, fname):
    """ Very naive write class to write the given text to a file
    Needs to be extended for the webapplication
    """
    outfile = open(fname, 'w')
    writable = File(outfile)
    for line in text:
        writable.write(line)
    writable.close()

class Reader(object):
    """ Defines a reader that reads all lines from a given filename
    It has methods to peek or pop the next line
    """

    linenumber = 0

    def __init__(self, fname):
        o_file = read_file(fname)
        self.lines = o_file.readlines()

    def peek_line(self):
        """ Return the first line, stripped from the newline char """
        if len(self.lines) > 0:
            return self.lines[0].rstrip('\r\n')
        return None

    def pop_line(self):
        """ Return a tuple of the first line and the linenumver.
        Removes the line, increases nr
        """
        line = collections.namedtuple('line', ['content', 'number'])
        if len(self.lines) > 0:
            self.linenumber += 1
            return line(self.lines.pop(0).rstrip('\r\n'), self.linenumber)
        return None
