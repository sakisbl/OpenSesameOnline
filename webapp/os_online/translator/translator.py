# -*- coding: ascii -*-
"""
#==============================================================================
#title           :translator.py
#description     :This module translates a .opensesame script into a JavaScript
                  file suitable for OpenSesame Online
#author          :OpenSesame group of GipHouse 2014, Radboud University
#programmers     :Ben Bruecker, Laurens van Bercken
#date            :20140419
#version         :0.1
#usage           :python ../translator.py
#notes           :
#python_version  :2.7
#==============================================================================
"""
import sys
import os_online.translator.utils.file_handler as handler
from os_online.translator.utils.file_handler import Reader
from os_online.translator.utils.parser import process_file
from os_online.translator.os_modules.variable import Variable
from os_online.translator.os_modules.comment import Comment
from os_online.translator.os_modules.define import Define
from os_online.translator.os_modules.log import Log
from os_online.translator.os_modules.setcycle import Setcycle
from os_online.translator.os_modules.draw import Draw
from os_online.translator.os_modules.widget import Widget
from os_online.translator.os_modules.multiline import Multiline
from os_online.translator.os_modules.run import Run
from os_online.translator.utils.js_creator import JSCreator

# Important! When adding new modules, add them to the imports up top,
# and to the collect_module_list function!

def _collect_module_list():
    """ Append the modules you want to check for here """
    module_list = []
    module_list.append(Variable)
    module_list.append(Comment)
    module_list.append(Define)
    module_list.append(Log)
    module_list.append(Setcycle)
    module_list.append(Draw)
    module_list.append(Widget)
    module_list.append(Multiline)
    module_list.append(Run)
    return module_list

def main(infile, outfile, comments=False):
    """ Reads the infile and processes it to JavaScript for the outfile
    if comments=True, then comments with unimplemented functions will
    be produced
    """
    # Read the os script
    reader = Reader(infile)
    module_list = _collect_module_list()
    # Parse the file, given the listed modules
    statements = process_file(reader, module_list)
    # Create the Javascript and write it to file
    filetext = JSCreator(statements, comments).get_js()
    handler.write(filetext, outfile)

if __name__ == "__main__":
    # The main function, it takes 2 arguments:
    # -Infile: The OS Script to be read
    # -Outfile: The produces Javascript corresponding to the experiment
    # -OPTIONAL -c parameter to produce comments
    # This function reads the infile, parses it, transforms it to JS and then
    # writes it to Outfile. It will exit when the input is malformed
    if not len(sys.argv) in (3, 4):
        print "Please provide 2 parameters: Infile Outfile (optional -c)"
        sys.exit(-1)
    INFILE = sys.argv[1]
    OUTFILE = sys.argv[2]

    COMMENTS = False
    try:
        HAS_COM = sys.argv[3]
    except IndexError:
        pass
    else:
        if HAS_COM == '-c':
            COMMENTS = True
    main(INFILE, OUTFILE, COMMENTS)
