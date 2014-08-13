# -*- coding: ascii -*-
"""
#==============================================================================
#title           :test_variable.py
#description     :Test the os_modules.variable.py module
#author          :OpenSesame group of GipHouse 2014, Radboud University
#programmers     :Ben Bruecker, Laurens van Bercken
#date            :20140419
#version         :0.1
#usage           :python ../translator.py
#notes           :
#python_version  :2.7
#==============================================================================
"""
import random
from os_online.translator.unit_tests.testcase_generator import TestSet


def os_mod_set_up(succes_patterns, fail_patterns):
    """ This initializes success and fail strings for os_module tests"""
    pool_size = 500
    max_length = 60
    t_set = TestSet(pool_size, max_length)
    succes_s = []
    fail_s = []
    nr_of_tests = 50
    for _ in xrange(nr_of_tests):
        for pat in succes_patterns:
            succes_s.append(t_set.get_testcase(pat))
        for pat in fail_patterns:
            fail_s.append(t_set.get_testcase(pat))
    return(random.sample(succes_s, nr_of_tests), \
            random.sample(fail_s, nr_of_tests))

def test_correct_initialization(testcase, samples, os_mod, os_type, params,\
        has_keywords=None, has_attributes=False):
    # pylint: disable=too-many-arguments
    """ Checks whether variable succesfully inits for success cases """
    for sample in samples:
        var = os_mod(sample)
        testcase.assertIsInstance(var, os_mod)
        testcase.assertTrue(var.os_type == os_type)
        for param in params:
            testcase.assertIsNotNone(var.get(param))
        testcase.assertTrue(var.keywords == has_keywords)
        testcase.assertTrue(var.has_extra_attributes == has_attributes)

def test_correct_failure(testcase, os_mod, samples):
    """ Checks whether variable fails for all fail cases """
    for sample in samples:
        try:
            os_mod(sample)
        except ValueError:
            pass
        else:
            testcase.fail(sample + " did not raise a ValueError")
