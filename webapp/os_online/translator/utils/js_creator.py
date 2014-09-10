# -*- coding: ascii -*-
"""
#==============================================================================
#title           :js_creator.py
#description     :Create JavaScript from a list of OpenSesame statements
#author          :OpenSesame group of GipHouse 2014, Radboud University
#programmers     :Ben Bruecker, Laurens van Bercken
#date            :20140419
#version         :0.1
#usage           :python ../translator.py
#notes           :
#python_version  :2.7
#==============================================================================
"""
import os_online.translator.utils.strings.os_global as str_global
import os_online.translator.utils.strings.os_statement as str_state
import os_online.translator.utils.strings.string_literals as strlit

# pylint: disable=too-few-public-methods
class JSCreator(object):
    """ This class will create a JavaScript file suitable for the OpenSesame
    web application from a list of statements from the .opensesame file
    """

    def __init__(self, statements, comments=False):
        """ Initialize this class with a set of valid OpenSesame Statements.
        It will produce the associated JS on creation, and it will be stored
        in self.file_text
        Retrieve the js with the get_js() function
        statements -- A list of OpenSesame statements
        comments   -- Specifies whether debug comments should be in the result
        """
        self.file_text = []
        self.statements = statements
        self.comments = comments
        dependencies = self._collect_dependencies(statements)

        self.file_text.append(self._get_initial_text(dependencies))
        self.file_text.append(self._get_global_text(dependencies['global']))
        self.file_text.append(self._get_independent_text(dependencies['indep']))
        self.file_text.append(self._get_dependent_text(dependencies['dep']))
        self.file_text.append(self._get_end_of_file(dependencies['global']))

    @staticmethod
    def _get_initial_text(dependencies):
        """ Gets the initial text for the top of the JS output"""
        g_vars = dependencies['global']
        width = None
        height = None
        for var in g_vars:
            if var.os_type == 'set':
                if var.get('name') == 'height':
                    height = var.get('value')
                elif var.get('name') == 'width':
                    width = var.get('value')
        if width and height:
            return str_global.get_initial_text(width, height)
        else:
            return strlit.ERROR_GLOBAL

    @staticmethod
    def _collect_dependencies(statements):
        """
        This function puts all statements into one of three categories.
        - dep for statements where dependencies matter
        - indep for statements where dependencies do not matter
        - global for global statements
        """
        glob = [x for x in statements if x.os_type == 'set']
        dep = [x for x in statements if x.os_type == 'define' and
                                 x.get('type') in ('loop', 'sequence')]
        indep = [x for x in statements if x not in glob and x not in dep]
        dependencies = {}
        dependencies['dep'] = dep
        dependencies['indep'] = indep
        dependencies['global'] = glob
        return dependencies

    def _get_global_text(self, global_statements):
        """ This function will write the global variables to the JS file """
        text = ""
        if self.comments:
            text = strlit.GLOBAL_TEXT
        return text + str_global.get_global_js(global_statements)

    def _get_independent_text(self, independent_statements):
        """ Creates the javascript from the associated independent variables"""
        text = ""
        if self.comments:
            text = strlit.INDEP_TEXT
        for statement in independent_statements:
            text += str_state.get_js(statement) + "\n"
        text += "\n"
        return text
    
    def _get_dependency_map(self, dependent_statements):
        """ Gets dependency map for dependent_statements, which is a dictionary
        that shows exactly which statement is dependent on which """
        dep_map = {}
        for s in dependent_statements:
            temp_list = []
            if s.attributes:
                for item in s.attributes:
                    if item.os_type == 'run':
                        temp_list.append(item.get('name'))
                        dep_map[s.get('name')] = temp_list
            else:
                dep_map[s.get('name')] = temp_list
        return dep_map


    def _has_dependency(self, i, dependent_statements, dependency_map):
        """ Returns True when there is a statement with a higher index number 
        than i that is dependent on the statement on position i. Being dependent
        on another statement means that you will called by another statement, so
        you have to be created earlier than the statement you are dependent on. """
        for item in dependency_map[dependent_statements[i].get('name')]:
            for j in range(i, len(dependent_statements)):
                if item == dependent_statements[j].get('name'):
                    return True    
        return False

    def _order_dependencies(self, dependent_statements):
        """ Orders the dependent_statements by continously popping an element
        and appending it to the end of dependent_statements when this element has
        a dependency.'i' will only be incremented when the current element does not
        have a dependency. When it does have a dependency, it will be popped from the
        front of the list, so 'i' now points to the element that was second in the list
        before popping the first element and should not be incremented """
        dependency_map = self._get_dependency_map(dependent_statements)
        i = 0
        while i < len(dependent_statements):
            if self._has_dependency(i, dependent_statements, dependency_map):
                dependent_statements.append(dependent_statements.pop(i))
            else:
                i += 1
        return dependent_statements

    def _get_dependent_text(self, dependent_statements):
        """ Creates the javascript from the associated dependent variables 
            Before doing that, the order has to be determined """
        text = ""
        dependent_statements = self._order_dependencies(dependent_statements)
        for statement in dependent_statements:
            text += str_state.get_js(statement) + "\n"
        return text

    @staticmethod
    def _get_end_of_file(global_statements):
        """ Gets the closing text for this JS file """
        found = False
        for statement in global_statements:
            if statement.get('name') == 'start':
                xp_start = statement.get('value')
                found = True
                break
        if not found:
            raise Exception("No starting point was defined")

        text = strlit.CLOSING_TEXT
        return text.format(xp_start)


    def get_js(self):
        """Simple function, just to return the produced js"""
        return self.file_text