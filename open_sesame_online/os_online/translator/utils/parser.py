# -*- coding: ascii -*-
"""
#==============================================================================
#title           :parser.py
#description     :This module parses through an open_sesame file and creates a
                  list of opensesame Statements from this.
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

def _check_indentation(line):
    """ This function checks if the current line stats with a tab """
    return re.match(r'^\t', line)

def _custom_error(linenumber, message=None):
    """ Throws a custom error message for the parser,
    so you know where there is a bug the message can be empty,
    but the linenumber will always be printed.
    IMPORTANT! Calling this function will exit the program
    """
    print "Error on line " + str(linenumber)
    if message:
        print message
    exit(-1)


def process_file(reader, module_list):
    """ This function checks all lines of a open sesame script and checks if
    they are valid according to the registered modules.
    When a match is found for every line, then this returns a list of
    statements corresponding to the script file. If not it throws an error
    message and exits the program.
    """
    statements = []
    define_mode = False # Items starting with define have indented attributes
    define_item = None  # The last define item where attr can be added

    while reader.peek_line() is not None:
        # This loop reads all lines and tries to find a matching pattern for
        # each. If it is unable to find a rule, it will call custom_error
        current = reader.pop_line() # Gets a new line and linenr
        current_line = current.content
        match_found = False

        # Check if we are in define mode by checking the indent
        if define_mode and not _check_indentation(current_line):
            define_mode = False
        elif define_mode:
            current_line = current_line.strip() # If we are, strip the tab

        for module in module_list: # Check all patterns
            try:
                item = module(current_line)
            except ValueError:
                continue

            match_found = True
            if not define_mode and item.has_extra_attributes:
                statements.append(item)
                define_mode = True
                define_item = item
            elif not define_mode and not item.has_extra_attributes:
                statements.append(item)
                define_item = None
                define_mode = False

            else: # Do this part if we are in define mode
                if hasattr(item, 'is_multiline'):
                    while reader.peek_line() is not None\
                            and not item.is_done():
                        current = reader.pop_line() # Gets a new line and linenr
                        current_line = current.content
                        item.addline(current_line.strip())
                    if not item.is_done():
                        _custom_error(current.number, "Parsing of file ended"
                                      "without closing multi-line variable")
                if item.has_extra_attributes: # If extra parameters can be added
                    _custom_error(current.number,\
                                  "You cannot do a define inside a define")
                define_item.append(item)
            break
        _handle_match_finding(match_found, current)

    return statements

def _handle_match_finding(found, current):
    """ This function specifies what happens when a match was found or
    not found.
    """
    if not found and current.content is not "":
        _custom_error(current.number, "No rule found for \""\
                                           + current.content + "\"")
