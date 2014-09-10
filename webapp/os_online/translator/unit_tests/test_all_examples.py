""" Runs pylint against all files in this directory"""
import os
import re
import os_online.translator.translator as translator

for f_name in os.listdir("examples"):
    if f_name.endswith(".opensesame"):
        translator.main('examples/' + f_name,\
                        'examples.out/' + re.sub('.opensesame', '.js', f_name))
