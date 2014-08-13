# -*- coding: ascii -*-
"""
#==============================================================================
#title           :view.py
#description     :This module either shows an experiment, or saves the results
                  for the same viewed experiment
#author          :OpenSesame group of GipHouse 2014, Radboud University
#date            :2014-06-16
#version         :0.2
#notes           :
#python_version  :2.7
#python_version  :1.6
#==============================================================================
"""
import os
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import Max
from os_online.experimenter.models import Token, Result
import json

def handle_post(request, tok, exp):
    """ Handles the post re uest for experiment results. Invalidates the token
    if it is private, and stores the JSON results in Results
    """
    if tok.perma_token:
        # This case is called when experiment is private, but
        # you are using the token for testing purposes
       return render_to_response('view_exp/thank_you.html')

    if not exp.is_public:
        # If it is not a permanent token, set this token to used and
        # update the number of participants in the corresponding experiment
        tok.used = True
        tok.save(update_fields=['used'])
        active = Token.active_objects.filter(experiment=exp.pk)
        inactive = Token.expired_objects.filter(experiment=exp.pk)
        exp.nr_participants = inactive.count()
        exp.max_participants = active.count() + inactive.count()
        exp.save(update_fields=['nr_participants', 'max_participants'])
        # On private experimetns, associate the participant Nr.
        subject = tok.subject_nr

    if exp.is_public:
        # If it is a public experiment update the participant count by +1
        exp.nr_participants = exp.nr_participants + 1
        exp.save(update_fields=['nr_participants'])
        # On public experiments add a new person to the db
        max_p = Result.objects.all().filter(experiment=exp)\
                .aggregate(Max('person'))
        subject = max_p['person__max']
        if subject is None:
            subject = 0
        else:
            subject = subject + 1
    postdata = json.loads(request.POST.get('postdata'))

    for dict_name in postdata:
        value_list = postdata[dict_name]
        list_length = len(value_list)
        for state_nr in range(0, list_length):
            value = value_list[state_nr]
            # pylint: disable=no-value-for-parameter
            # pylint: disable=unexpected-keyword-arg
            res = Result(experiment=exp, var_name=dict_name,\
                var_value=value, state=state_nr, person=subject)
            res.save()
        return render_to_response('view_exp/thank_you.html')

def view_experiment(request, exp_token):
    """ View_experiment serves an experiment that is associated with the given
    token, if that token is still valid.
    If this view is called with a POST request containing results. Then
    invalidate this token (If it was private) and save the results.
    """
    tok = Token.objects.get(token=exp_token)
    if tok.used:
        return render_to_response('view_exp/used.html')
    exp = tok.experiment

    # If POST, then this is the result of an experiment coming in
    if request.method == 'POST':
        return handle_post(request, tok, exp)
    # if NOT POST serve the experiment associated with this token
    else:
        slug = tok.experiment.slug
        scriptname = '%s/%s' % (slug, slug)
        pool = '%s/pool/' % slug
        images = json.dumps(get_dir(pool, [".jpg", ".png"]))   
        context = {'scriptname':scriptname, 'pool':pool, 'images':images}
        return render_to_response('view_exp/show.html', context,\
            context_instance=RequestContext(request))

def get_dir(dir, file_extensions):
    """ This returns all filenames in 'dir' that have a file extension that is in
    'file_extensions'. Returns [] when directory does not exist or no matching files found
    """
    path = os.path.join(settings.MEDIA_ROOT, dir)
    contents = []
    if os.path.isdir(path):
        for f in os.listdir(path):
            if os.path.splitext(f)[1] in file_extensions:
                contents.append(f)
    return contents 
