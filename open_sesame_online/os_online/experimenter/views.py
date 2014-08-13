# -*- coding: ascii -*-
"""
#==============================================================================
#title           :view.py
#description     :This module implements all views that are important for an
                 :OpenSesameOnline experimenter. The implemented views are:
                  - list_view   (List all experiments and show the options)
                  - upload_view (Upload a new experiment)
                  - edit_view   (change experiment parameters)
                  - create_token (Creates a number of tokens for a private exp)
                  - token_list_view (Shows all active, expired and permalinks)
                  - show_results (Shows a table of experiment results)
                  - delete_view  (Deletes the referenced experiment)
                  - export_csv   (Export the exp results as a csv file)
#author          :OpenSesame group of GipHouse 2014, Radboud University
#date            :2014-06-16
#version         :0.2
#notes           :
#python_version  :2.7
#python_version  :1.6
#==============================================================================
"""
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db.models import Max, Q
from django.contrib.auth.decorators import login_required
from os_online.experimenter.forms import UploadFileForm, EditForm,\
        CreateTokenForm
from os_online.experimenter.models import Experiment, Token, Result
import os_online.experimenter.file_handler as handler
import os, shutil, csv
from django.utils import timezone
from collections import defaultdict


# pylint: disable=no-value-for-parameter
# pylint: disable=no-member
# This class includes a lot of Django model initialization. This is not parsed
# correctly in pylint. Therefore this warning is disabled
@login_required
def list_view(request):
    """ This is the main view for an experimenter. Lists all his experiments"""
    exps = Experiment.objects.filter(experimenter_id=request.user.id)
    return render_to_response('experimenter/list.html', \
            {'exps': exps}, context_instance=RequestContext(request))

def find_max_subject_id(exp):
    """ Finds the maximum subject number for an experiment with pk = exp"""
    max_person = Token.objects.all().filter(experiment=exp)\
        .aggregate(Max('subject_nr'))['subject_nr__max']
    if not max_person:
        return 1
    else:
        return max_person + 1

@login_required
def upload_view(request):
    """ If POST, upload the given experiment if it passes all checks.
    Else serve the upload view"""
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # If the form is valid, handle the uploaded data
            # The random path will be the folder name in /media/
            random_path = handler.make_random_path()
            out_file_name = \
                os.path.join(settings.MEDIA_ROOT, random_path, random_path)
            in_file_name = out_file_name + '.opensesame'

            # Handle the uploaded file. If it is a tar.gz, it gets extracted
            handler.handle_uploaded_file(
                request.FILES['docfile'],
                random_path)

            # Check if the uploaded script can be translated
            handler.try_translation(in_file_name, out_file_name)

            # Set all the parameters for a new experiment
            exp = Experiment()
            exp.experimenter_id = request.user.id
            exp.is_open = True
            exp.title = form.cleaned_data['title']
            exp.slug = random_path
            exp.start_date = form.cleaned_data['start_date']
            exp.end_date = form.cleaned_data['end_date']
            exp.is_public = form.cleaned_data['is_public']
            exp.js_file = out_file_name

            #Check if the start date is before the end date
            if exp.start_date and exp.end_date:
                if exp.start_date > exp.end_date:
                    form = UploadFileForm()
                    return render_to_response('experimenter/upload.html',\
                        {'form': form,\
                        'error_message':\
                        "Your start date is after or on your end date!",},\
                        context_instance=RequestContext(request))

            # Check if start date is not in the past
            if exp.start_date:
                if exp.start_date < timezone.now().date():
                    form = UploadFileForm()
                    return render_to_response('experimenter/upload.html',\
                        {'form': form,\
                        'error_message':\
                        "Your start date is earlier then today!",},\
                        context_instance=RequestContext(request))
            exp.save()

            # Create a permalink token for this experiment
            token = Token()
            token.experiment = exp
            token.perma_token = True
            token.subject_nr = 0
            token.save()
            exp.permalink = token
            exp.save()
            
            # For public experiments add one token for participants
            if form.cleaned_data['is_public']:
                token = Token()
                token.experiment = exp
                token.subject_nr = 1
                token.save()

            # Serve the list view after a succesful upload
            return HttpResponseRedirect(
                reverse('os_online.experimenter.views.list_view'))
    else:
        form = UploadFileForm()

    # If there is no post request, show the upload form
    return render_to_response('experimenter/upload.html',\
            {'form': form}, context_instance=RequestContext(request))

@login_required
def create_token(request, experiment_pk):
    """ If post, creates a nr of tokens for the given experiment_pk equal
    to 'nr_tokens' from the form.
    Else serve the create tokens view"""
    
    # If the experimenter is not the owner of experiment_pk send him to error
    exp = Experiment.objects.get(pk=experiment_pk)
    if not exp.experimenter_id == request.user.id:
        return render_to_response('experimenter/not_owner.html')
    
    if request.method == 'POST':
        # A Post re uest happens if the create token form was posted
        form = CreateTokenForm(request.POST, request.FILES)
        if form.is_valid():

            #For 0 upto nr_tokens add a single valid token to tokens
            for _ in xrange(0, form.cleaned_data['nr_tokens']):
                token = Token()
                token.experiment = exp
                token.subject_nr = find_max_subject_id(exp)
                token.save()

            # Update the participant count
            active = Token.active_objects.filter(experiment=experiment_pk)
            inactive = Token.expired_objects.filter(experiment=experiment_pk)
            exp.nr_participants = inactive.count()
            exp.max_participants = active.count() + inactive.count()
            exp.save(update_fields=['nr_participants', 'max_participants'])

            return HttpResponseRedirect(
                reverse('os_online.experimenter.views.token_list_view',\
                kwargs={'experiment_pk':experiment_pk}))
    
    # If not a POST reauest, serve the Create Token form
    else:
        form = CreateTokenForm()
    return render_to_response('experimenter/create_token.html', \
        {'form': form, 'exp_id':experiment_pk},\
        context_instance=RequestContext(request))

@login_required
def token_list_view(request, experiment_pk):
    """ View the permalink and all available and unavailable tokens
    for the given experiment"""
    exp = Experiment.objects.get(pk=experiment_pk)
    # If the experimenter is not the owner of experiment_pk send him to error
    if not exp.experimenter_id == request.user.id:
        return render_to_response('experimenter/not_owner.html')
    
    perma_token = Token.objects.get(experiment=experiment_pk, perma_token=True)
    
    # If the experiment is not public, show the permalink, the active and 
    # expired tokens
    if not Experiment.objects.get(pk=experiment_pk).is_public:
        active_tokens = Token.active_objects.filter(experiment=experiment_pk)
        inactive_tokens = Token.expired_objects\
            .filter(experiment=experiment_pk)
        return render_to_response('experimenter/private_token_list.html', \
            {'active_tokens': active_tokens,\
            'inactive_tokens': inactive_tokens,\
            'perma_token': perma_token,\
            'exp_id':experiment_pk},\
            context_instance=RequestContext(request))
    
    # On public experiments only show the permalink
    else:
        participant_token = Token.active_objects.get(experiment=experiment_pk)
        return render_to_response('experimenter/public_token_list.html',\
            {'perma_token': perma_token,\
            'exp_id':experiment_pk,
            'participant_token': participant_token},\
            context_instance=RequestContext(request))

@login_required
def edit_view(request, experiment_pk):
    """ If POST, edit the given experiment,
    Else show the edit view"""
    exp = Experiment.objects.get(pk=experiment_pk)
    # If the experimenter is not the owner of experiment_pk send him to error
    if not exp.experimenter_id == request.user.id:
        return render_to_response('experimenter/not_owner.html')
    
    # If there is a post request, handle the changed experiment parameters
    if request.method == 'POST':
        form = EditForm(request.POST)
        if form.is_valid():
            exp.title = form.cleaned_data['title']
            exp.start_date = form.cleaned_data['start_date']
            exp.end_date = form.cleaned_data['end_date']
            exp.save()
            return HttpResponseRedirect(
                reverse('os_online.experimenter.views.list_view'))
    
    # If no post request, show the edit experiment form
    else:
        form = EditForm()
    return render_to_response('experimenter/edit.html',\
        {'form': form, 'experiment_id': experiment_pk, 'exp': exp},\
        context_instance=RequestContext(request))

@login_required
def show_results(request, experiment_pk):
    """ This definition shows the results for a given experiment """
    exp = Experiment.objects.get(pk=experiment_pk)

    # If the experimenter is not the owner of experiment_pk send him to error
    if not exp.experimenter_id == request.user.id:
        return render_to_response('experimenter/not_owner.html')
    
    result_list = []
    # Create a list of all the uni  ue subjects
    subject_dict = defaultdict(list)
    for res in Result.objects.filter(experiment=experiment_pk):
        subject_dict[res.person].append(res)

    for subject in subject_dict:
        rows = []
        names = []
        name_dict = defaultdict(list)
        # find the maximum state (nr of result rows) for this subject
        max_state = Result.objects.all().filter(\
            Q(experiment=experiment_pk) &\
            Q(person=subject))\
            .aggregate(Max('state'))['state__max']
        for n_list in Result.objects.filter(Q(experiment=experiment_pk)\
                & Q(person=subject)):
            name_dict[n_list.var_name].append('')
        names = [name for name in name_dict]
        for c_state in xrange(0, int(max_state)+1):
            cols = []
            for name in name_dict:
                cols.append(Result.objects.get(\
                    Q(experiment=experiment_pk) &\
                    Q(person=subject) &\
                    Q(state=c_state) &\
                    Q(var_name=name))\
                    .var_value)
            rows.append(cols)
        result_list.append([subject, names, rows])
    return render_to_response('experimenter/resultlist.html',\
            {'results': result_list}, context_instance=RequestContext(request))

@login_required
def delete_view(request, experiment_pk):
    """ Deletes the experiment with pk=experiment pk from the database and
    from disk.
    """
    exp = Experiment.objects.get(pk=experiment_pk)
    if not exp.experimenter_id == request.user.id:
        return render_to_response('experimenter/not_owner.html')
    to_delete = Experiment.objects.get(pk=experiment_pk)
    del_file = str(to_delete.js_file)
    path = os.path.abspath(os.path.dirname(del_file))
    shutil.rmtree(path)
    to_delete.delete()
    exps = Experiment.objects.filter(experimenter_id=request.user.id)
    return render_to_response('experimenter/list.html', \
            {'exps': exps}, context_instance=RequestContext(request))

@login_required
def export_csv(request, experiment_pk):
    """ This definition exports the results of an experiment to a .csv file"""
    exp = Experiment.objects.get(pk=experiment_pk)

    # If the experimenter is not the owner of experiment_pk send him to error
    if not exp.experimenter_id == request.user.id:
        return render_to_response('experimenter/not_owner.html')
    res = Result.objects.all().filter(experiment=experiment_pk)

    # If there are no results yet, redirect the experimenter to the list view
    if not res:
        exps = Experiment.objects.filter(experimenter_id=request.user.id)
        return render_to_response('experimenter/list.html', \
            {'exps': exps}, context_instance=RequestContext(request))

    # Set up the respose so it will serve a csv file
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="subject_0.csv"'
    writer = csv.writer(response)

    # Collect and write the column names
    name_string = "subject,"
    for name in res.values_list('var_name').distinct():
        name_string += name[0] + ","
    writer.writerow([name_string[:-1]])

    # Find the number of participants for the given experiment
    max_person = Result.objects.all().filter(\
        experiment__id=experiment_pk)\
        .aggregate(Max('person'))['person__max']
    # Find the maximum number of rows for this experiment
    max_state = Result.objects.all().filter(\
        experiment__id=experiment_pk)\
        .aggregate(Max('state'))['state__max']

    # Loop over all subjects
    for sub in range(0, max_person+1):
        # Loop over all result rows for a subject
        for stat in range(0, max_state+1):
            result_row = res.values_list('var_value').filter(person=sub)\
                .filter(state=stat)
            result_row_string = ""
            for result in result_row:
                result_row_string += result[0] + ","
            if result_row_string != "":
                result_row_string = str(sub) + "," + result_row_string
                writer.writerow([result_row_string[:-1]])
    return response


@login_required
def export_token_csv(request, experiment_pk):
    """ This definition exports a list of tokens of an experiment to a .csv file"""
    exp = Experiment.objects.get(pk=experiment_pk)
    exp_title = exp.title
    print exp
    if not exp.experimenter_id == request.user.id:
        return render_to_response('experimenter/not_owner.html')
    tokens = Token.objects.all().filter(experiment=experiment_pk)[1:]
    if not tokens:
        exps = Experiment.objects.filter(experimenter_id=request.user.id)
        return render_to_response('experimenter/tokenlist.html', \
                {'exps': exps}, context_instance=RequestContext(request))

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = "attachment; filename=" + "" + exp_title + '.csv'
    writer = csv.writer(response)
    writer.writerow([str(exp_title)])
    name_string = 'Tokens,Token used,Subject no.'
    writer.writerow([name_string])
    for token in tokens:
        s = ""
        s += str(token.token) + ","
        s += str(token.used) + ","
        s += str(token.subject_nr)
        writer.writerow([s])
    return response

@login_required
def help_view(request):
    exps = Experiment.objects.filter(experimenter_id=request.user.id)
    return render_to_response('experimenter/help.html', \
            {'exps': exps}, context_instance=RequestContext(request))

