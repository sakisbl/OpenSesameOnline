#! /usr/bin/env python
"""Module that runs pylint on all python scripts found in a directory tree.
"""

import os
import re
import sys

def check(module):
    """ apply pylint to the file specified if it is a *.py file
    """
    local_count = 0
    local_total = 0.0

    if module[-11:] == "__init__.py":
        print "IGNORING ", module + '\n'

    elif module[-3:] == ".py":
        print "CHECKING ", module
        pout = os.popen('pylint --load-plugins pylint_django %s'% module, 'r')
        for line in pout:
            if  re.match(r".:.+:.+", line):
                print line.strip()
            if "Your code has been rated at" in line:
                print line
                score = re.findall(r"\d.\d\d|\d\d.\d\d", line)[0]
                local_total += float(score)
                local_count += 1
    return (local_total, local_count)

if __name__ == "__main__":
    try:
        print sys.argv
        BASE_DIRECTORY = sys.argv[1]
    except IndexError:
        print "no directory specified, defaulting to current working directory"
        BASE_DIRECTORY = os.getcwd()

    TOTAL = 0.0
    COUNT = 0
    print "looking for *.py scripts in subdirectories of ", BASE_DIRECTORY
    for root, dirs, files in os.walk(BASE_DIRECTORY):
        for name in files:
            filepath = os.path.join(root, name)
            result = check(filepath)
            TOTAL += result[0]
            COUNT += result[1]


    print "==" * 50
    print "%d modules found"% COUNT
    if COUNT > 0:
        print "AVERAGE SCORE = %.02f"% (TOTAL / COUNT)
    else:
        print "AVERAGE SCORE = 0"
