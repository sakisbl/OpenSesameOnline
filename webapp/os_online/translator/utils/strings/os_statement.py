# -*- coding: ascii -*-
"""
#==============================================================================
#title           :js_strings.py
#description     :Create JavaScript literals for OpenSesame Online
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
import os_online.translator.utils.strings.string_literals as strlit
import os_online.translator.utils.strings.os_comment as comment


def get_js(item):
    """ Gets the JavaScript associated with a single OpenSesame statement
    item    -- The OpenSesame Statement
    """
    os_type = item.os_type
    if os_type == 'define':
        result = get_js_define(item)
    elif os_type == 'set':
        result = get_js_variable(item)
    elif os_type == 'run':
        result = get_js_run(item)
    elif os_type == '#':
        result = get_js_comment(item)
    elif os_type == 'setcycle':
        result = get_js_setcycle(item)
    elif os_type == 'multi-line':
        result = get_js_multiline(item)
    else:
        result = strlit.ERROR_JS.format(os_type)
    return result

def get_js_multiline(item):
    """ Gets the JS representation of a multiline item
    newlines will be replaced by \n
    """
    f_string = strlit.JS_DICT[item.os_type]
    result = f_string.format(item.get('lines'))
    return result.replace('\n', '\\n')

def get_js_comment(item):
    """ Gets the JavaScript representation of a comment """
    f_string = strlit.JS_DICT[item.os_type]
    return f_string.format(item.get('comment'))

def get_js_variable(item):
    """ Gets the JavaScript representation of a variable """
    f_string = strlit.VARIABLE_DICT[item.get('name')]
    value = item.get('value')
    itemname = item.get('name')
    """ if itemname in ('allowed_responses', 'correct_response'):
        # Character variables get special treatment. We split them and
        # represent them as their ascii values
        
        # TEMPORARY VAR CHECK
        if not re.match(r'^\[.*\]$', value):
        #END TEMP CHECK
        
            value = re.sub(r'^"|^\'|"$|\'$', '', value)
            val = ""
            for char in re.split(' |;|,', value):
                if not val == "":
                    val += " "
                if char in strlit.KEYMAP:
                    char = strlit.KEYMAP[char]
                print char
                val += str(ord(char))
            value = val
    """
    if itemname == 'column_order':
        # Column order variables get represented as a lit
        val = item.get('value')
        if not val == '':
            columns = val.split(';')
            str_out = ''
            for col in columns:
                str_out = seperator(str_out)
                str_out += strlit.JS_DICT['js_list_quotes'].format(col)
            value = str_out
    elif itemname == 'break_if':
        # Break vars need to translate the given condition
        value = get_condition(value)
    return f_string.format(value)

def get_js_run(item):
    """ Gets the JavaScript representation of the run function """
    f_string = strlit.JS_DICT[item.os_type]
    return f_string.format(item.get('name'))

def get_js_draw(item, name):
    """ Gets the JavaScript for a draw statement
    item -- a draw statement
    name -- the name of this draw statement
    """
    f_string = strlit.JS_DICT[item.os_type]
    d_type = strlit.DRAW_NAME_DICT[item.get('type')]
    params = ""
    for current_p in strlit.DRAW_PARAM_DICT[item.get('type')]:
        params = seperator(params)
        p_item = item.get(current_p)
        if current_p == 'show_if':
            params += strlit.JS_DICT['js_quotes'].format(get_condition(p_item))
        else:
            params += strlit.JS_DICT['js_quotes'].format(str(p_item))
    return f_string.format(name, d_type, params)

def get_js_setcycle(item):
    """ Gets the JavaScript representation of the setcycle function """
    f_string = strlit.JS_DICT[item.os_type]
    return f_string.format(item.get('name'), item.get('value'))

def get_js_setcycles(items, cyclename):
    """ Creates the setcycle variable needed for the loop define statement.
    items       -- The list of setcycle items that the loop consists of
    cyclename   -- The name for the current cycle variable
    """
    if items == []:
        return ""
    f_string_function = strlit.JS_DICT['setcycle_function']
    f_string_iteration = strlit.JS_DICT['setcycle_iteration']
    iterations = ""
    while items:
        item = items[0]
        counter = item.get('cyclenumber')
        current = [x for x in items if x.get('cyclenumber') == counter]
        result = get_js_iteration(current)
        iterations = seperator(iterations)
        iterations += f_string_iteration.format(result)
        # Remove the items from this cycle.
        items = [x for x in items if not x.get('cyclenumber') == counter]
    return f_string_function.format(cyclename, iterations)

def get_js_iteration(items):
    """ Creates the Javascript for a single iteration of a setcycle.
    items -- A list of setcyce items with identical cycle numbers
    """
    if items == [] or None:
        return ""
    iteration = ""
    for item in items:
        iteration = seperator(iteration, ',\n')
        iteration += get_js_setcycle(item)
    return iteration

def get_condition(condition):
    """ Replaces os condition strings with js conditions
    condition -- A statement from a run condition
    """
    c_map = strlit.CONDITION_MAP
    for key in c_map:
        condition = re.sub(key, c_map[key], condition)
    return condition

def get_js_define(item):
    """ Creates the Javascript for a single Define statement.
    Because a define contains other OpenSesame statements, this function
    will also create the associated js for each statement in the define.
    /Begin: IMPORTANT!
    strlit.DEFINE_PARAM_MAP denotes the order of parameters for each type of
    define. if a define type is not included in this dictionary, then only
    a associated comment will be produced instead of the Javascript.
    Also, parameters tat are present but not in the dictionary will be
    commented.
    /End: IMPORTANT!
    """
    p_map = strlit.DEFINE_PARAM_DICT[item.get('type')]
    if p_map or p_map == []:
        precurser = []
        draw_counter = 0
        found_multiline = False
        var_list = [strlit.JS_DICT['js_quotes'].format(item.get('name'))]
        for par in p_map:
            if item.attributes:
                p_vars = [x for x in item.attributes if\
                                    x.os_type == 'set' and # Variable
                                    x.get('name') == par or
                                    x.os_type == par]        # Function
            else:
                p_vars = []
            if item.get('type') == 'text_display'\
                    and par == 'multi-line':
                found_multiline = True
            
            if par == 'setcycle':
                _define_case_setcycle(p_vars, item, precurser, var_list)
            elif par == 'run' and item.get('type') == 'sequence':
                _define_case_run(p_vars, var_list)
            elif par == 'draw' and item.get('type') == 'sketchpad':
                draw_counter = _define_case_draw(p_vars, item,\
                        precurser, draw_counter, var_list)
            elif par == 'log' and item.get('type') == 'logger':
                _define_case_log(p_vars, var_list)
            elif par == 'use_quotes' and item.get('type') == 'logger':
                _define_case_log_quotes(p_vars, var_list)
            elif p_vars == []:
                _define_case_error(par, item, var_list, found_multiline)
            else:
                # Normal case: Just append the item
                var_list.extend(p_vars)

        parameters = _define_var_list_to_string(var_list)

        f_string = strlit.JS_DICT[item.os_type]
        java_script = f_string.format(item.get('name'), item.get('type'),\
                                        parameters)
        unimp = comment.get_unimp(item, p_map)
        prec = _define_precurser_string(precurser)
        return prec + java_script + unimp

    else: # If this function was not in p_map, just add it as a comment
        return comment.get_comment(item)

def _define_case_setcycle(p_vars, item, precurser, var_list):
    """ Special case #1: Setcycles, create js for setcycle"""
    name = strlit.JS_DICT['cyclename']
    cyclename = name.format(item.get('name'))
    setcycles = get_js_setcycles(p_vars, cyclename)
    if setcycles == "":
        var_list.append("undefined")
    else:
        precurser.append(setcycles)
        var_list.append(cyclename)

def _define_case_run(p_vars, var_list):
    """ Special case #2: Conditions and names for run statements in sequence"""
    names = ''
    conditions = ''
    for current in p_vars:
        conditions = seperator(conditions)
        names = seperator(names)
        names += "JS" + current.get('name')
        conditions += strlit.JS_DICT['js_quotes'].format(get_condition(current.get('condition')))
    var_list.append(strlit.JS_DICT['run_pars'].format(names))
    var_list.append(strlit.JS_DICT['run_pars'].format(conditions))

def _define_case_draw(p_vars, item, precurser, draw_counter, var_list):
    """ Special case #3: Draw statements """
    names = ""
    conditions = ""
    for current in p_vars:
        name = strlit.JS_DICT['draw_name']
        name = name.format(item.get('name'),
                           current.get('type'),
                           str(draw_counter))
        draw_counter += 1
        precurser.append(get_js_draw(current, name))
        names = seperator(names) + name
    var_list.append(strlit.JS_DICT['js_list'].format(names))
    return draw_counter

def _define_case_log(p_vars, var_list):
    """ Special case #4: Logger, log item """
    names = ""
    for current in p_vars:
        name = strlit.JS_DICT['js_list_quotes'].format(current.get('name'))
        names = seperator(names) + name
    if names == "":
        var_list.append('undefined')
    else:
        var_list.append(strlit.JS_DICT['js_list'].format(names))

def _define_case_log_quotes(p_vars, var_list):
    """ Special case #4: Logger, use_quotes item """
    if p_vars == []:
        var_list.append('"no"')
    else:
        var_list.extend(p_vars)

def _define_case_error(par, item, var_list, found_multiline):
    """
    # Error Case: If an item was not found, append what item was
    # not found
    # when no multiline is found in text_display,
    # there may still be content,
    # so no error should be appended for not finding multi-line
    # when there is a multiline found in text_display,
    # no error should be appended for not finding content
    # when neither multi-line nor content is found,
    # only an error for not finding content is appended
    """
    if not (item.get('type') == 'text_display' and\
            par == 'multi-line' or found_multiline == True):
        var_list.append("undefined")

def _define_var_list_to_string(var_list):
    """ Transforms a list of variables into a comma seperated list"""
    parameters = ""
    for var in var_list:
        parameters = seperator(parameters)
        if isinstance(var, str):
            parameters += var
        else:
            parameters += get_js(var)
    return parameters

def _define_precurser_string(precurser):
    """ Transfors a list of precurser items into a newline seperated string"""
    prec = ""
    for pre in precurser:
        prec = seperator(prec, '\n') + pre
    return prec + '\n'

def seperator(string, delim=', '):
    """ Creates a comma after the given string if it is not empty. Also
    adds a newline if that parameter is true
    """
    if not string == "":
        string += delim
    return string
