# -*- coding: ascii -*-
"""
#==============================================================================
#title           :urls.py
#description     :This module adds the token url pattern to view an experiment
#author          :OpenSesame group of GipHouse 2014, Radboud University
#date            :2014-06-17
#version         :0.2
#notes           :
#python_version  :2.7
#python_version  :1.6
#==============================================================================
"""
from django.conf.urls import patterns, url
from django.views.generic import TemplateView

# pylint: disable=invalid-name
urlpatterns = patterns('os_online.view_exp.views',\
    url(r'^thank_you/$', TemplateView.as_view(\
        template_name='thank_you'), name='thank_you'),
    url(r'(?P<exp_token>\w+)/$', 'view_experiment', name='view_experiment'),\
)
