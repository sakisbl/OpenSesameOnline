# -*- coding: ascii -*-
"""
#==============================================================================
#title           :view.py
#description     :This module implements managers for the Experiment Tokens.
                  ActiveTokenManager will fetch the tokens that are not yet
                  invalidated. (But not the permalink)
                  ExpiredTokenManager will fetch the expired tokens
#author          :OpenSesame group of GipHouse 2014, Radboud University
#date            :2014-06-16
#version         :0.2
#notes           :
#python_version  :2.7
#python_version  :1.6
#==============================================================================
"""
from django.db.models import Manager, Q

#pylint: disable=too-many-public-methods
class ActiveTokenManager(Manager):
    """ Manager for active tokens (not expired).
    """
    def get_queryset(self):
        """ Gets the set of active tokens (excludes the permalink)"""
        queryset = super(ActiveTokenManager, self).get_queryset()
        return queryset.filter(Q(used=False), Q(perma_token=False))

class ExpiredTokenManager(Manager):
    """ Manager for expired tokens.
    """
    def get_queryset(self):
        """ Gets the set of expired tokens"""
        queryset = super(ExpiredTokenManager, self).get_queryset()
        return queryset.filter(Q(used=True))

