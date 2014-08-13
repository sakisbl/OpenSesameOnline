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
from collections import defaultdict

#pylint: disable=bad-whitespace

# This is the default dictionary for JS literals
# The Format string parameters are in the comments after each line
JS_DICT = defaultdict(lambda: None, {
    'define'            : 'var JS{} = new {}({});',     #name, type, params
    'js_list'           : '[{}]',                    #list_items
    'js_list_quotes'    : '"[{}]"',                  #list_items
    'js_quotes'         : '"{}"',                    #item
    '#'                 : '// {}',                   #comment
    'run'               : 'JS{}',                      #name
    'draw'              : 'var {} = new {}({});',    #name, type, params
    'draw_name'         : '{}_{}_{}',                #def_name, type, ctr
    'multi-line'        : '"{}"',                    #lines
    'global_var'        : 'globalVars["{}"] = "{}";',#name, value
    'cyclename'         : '{}_cycle',                #name
    'setcycle'          : '\t\t"[{}]" : "{}"',       #name, value
    'setcycle_function' : 'var {} = [{}\n];\n\n',    #setcycle_iteration
    'setcycle_iteration': '\n\t{{\n{},\n\t}}',       #setcycle
    'run_pars'          : '[{}]',                    #names
    'run_conditions'    : '"globalVars["{}"] {} {}"'})#conditions

# This is the default dictionary for JS comments
# The Format string parameters are in the comments after each line
COMMENT_DICT = defaultdict(lambda: "/*NotImplemented*/",{
    'set'               : "//\t{} = {}",            #name, value
    'run'               : "//\trun: {}",            #name
    '#'                 : "//\t{}",                 #comment
    'define'            : "/*\n\tUnimplemented: {} {}" \
                          "- with attributes:\n*/"})  #name, type

# This dictionary defines how variables should be represented
VARIABLE_DICT = defaultdict(lambda: '"{}"',{ # Default, value with quotes
    'column_order'      : "[{}]",   # Value surrounded by brackets
    'timeout'           : '"{}"',     # These types return the raw value
    'repeat'            : "{}",
    'cycles'            : "{}"})

# translates the names of the os draw types into types used in the JS
DRAW_NAME_DICT = defaultdict(lambda: "/*Unimplemented*/,",{
    'image'             : 'img',
    'ellipse'           : 'ellipse',
    'circle'            : 'circle',
    'line'              : 'line',
    'arrow'             : 'arrow',
    'textline'          : 'textline',
    'gabor'             : 'gabor',
    'noise'             : 'noise',
    'fixdot'            : 'fixdot'})

# Define what the order of parameters for draw statements is
DRAW_PARAM_DICT = {
    'image'             : ['x','y','path', 'scale', 'center', 'show_if'],
    'ellipse'           : ['left','top','width','height'],
    'circle'            : ['x','y','radius'],
    'line'              : ['left','right','top','bottom'],
    'arrow'             : ['left','right','top','bottom'],
    'textline'          : ['x','y','text','center','color'\
                           ,'font_family','font_size','font_italic'
                           ,'font_bold','show_if'],
    'gabor'             : ['x','y'],
    'noise'             : ['x','y'],
    'fixdot'            : ['x','y', 'color', 'show_if']}

# This map specifies the parameter order for the different defines.
DEFINE_PARAM_DICT = defaultdict(lambda: None,{
    'text_display'      : ['foreground',
                           'font_size',
                           'align',
                           'multi-line',
                           'content',
                           'background',
                           'duration',
                           'font_family'],
    'keyboard_response' : ['correct_response',
                           'allowed_responses',
                           'timeout'],
    'loop'              : ['repeat',
                           'skip',
                           'offset',
                           'run',
                           'break_if',
                           'column_order',
                           'cycles',
                           'order',
                           'setcycle'],
    'sequence'          : ['run'],
    'logger'            : ['log'],
    'sketchpad'         : ['duration',
                           'draw'],
    'reset_feedback'    : []})


# Mapping of OS key name values to the actual string representation
KEYMAP = {
    'exclamation'   : '!',
    'doublequote'   : '"',
    'hash'          : '#',
    'dollar'        : '$',
    'ampersand'     : '&',
    'quoteleft'     : '\'',
    'asterisk'      : '*',
    'plus'          : '+',
    'comma'         : ',',
    'minus'         : '-',
    'slash'         : '/',
    'colin'         : ':',
    'semicolon'     : ';',
    'equal'         : '=',
    'greater'       : '>',
    'question'      : '?',
    'at'            : '@',
    'bracketleft'   : '[',
    'backslash'     : '\\',
    'bracketright'  : ']',
    'underscore'    : '_'}

# This map translates from os notation to js notation
CONDITION_MAP = {
    '='         : '==',
    ' and '     : ' && ',
    ' or '      : ' || ',
    'always'    : 'true',
    'never'     : 'false'}

# The top of the OpenSesame JavaScript output file
# -Format String parameters:
# -width  -- window width in px
# -height -- window height in px
INITIAL_TEXT = ("// This is the statically generated Javascript code"
     " for an OpenSesame Script.\n\nutils.canvasInit({}, {});"
     "\nvar CANVAS = new fabric.StaticCanvas(\"canvas\");\n\n")

# Descriptive text for the global parameters
GLOBAL_TEXT = ("// ==========GLOBAL PART==========\n"
     "// These global variables are not yet used, but are present\n"
     "// in the OpenSesame script:\n")

# Descriptive text for the global variables
GLOBAL_VARS = "globalVars=[];\n{}\n\n"

# Descriptive text for independent parameters
INDEP_TEXT = ("\n// ==========INDEPENDENT PART==========\n"
     "// The independent parts are defined below.\n"
     "// Unimplemented functions and parameters will be commented\n\n")

# Descriptive text for dependent parameters
DEP_TEXT = ("\n// ==========DEPENDENT PART==========\n"
     "// The dependent parts are defined below.\n"
     "// Unimplemented functions and parameters will be commented\n\n")

# The bottom of the OpenSesame Javascript output file
# Format String parameters:
# - Name of the experiment starting point (from global var named 'start'
CLOSING_TEXT = ("\n//=========MASTER experiment==========\n"
     "var _firstSeq_ = JS{};\n"
     "var MASTER = new Experiment(_firstSeq_);\n"
     "$(window).bind('load', function() {{\n"
     "\t$('#loader').remove();\n"
     "\tMASTER.run();\n"
     "}});")

# Descriptive text for unused features
UNUSED = "\n//\tUnused features:\n{}"

# Descriptive text for unimplemented comments
# Format String parameters:
# - Name of the unimplemented function
ERROR_COMMENT = "//\tWARNING! No comment yet implemented for {}"

# Descriptive text for unimplemented JavaScript
# Format String parameters:
# - Name of the unimplemented function
ERROR_JS = "//\tWARNING! No js yet implemented for {}"

# JavaScript error for the case that a parameter was not in the OS script
# Format String parameters:
# - Name of the unimplemented function
ERROR_TEXT = "[] /*WARNING: {} not present! */"

# Javascript error for missing height or with in global text
ERROR_GLOBAL  = "/* ERROR: No width or height was defined */"