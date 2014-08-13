""" These are all the forms used in the experimenter app """
from django import forms

class UploadFileForm(forms.Form):
    """ This is the upload form, for uploading OS-scripts and
    creating an online experiment """
    docfile = forms.FileField(label='Select a file')
    title = forms.CharField(label='Choose a title')
    start_date = forms.DateField()
    end_date = forms.DateField(required=False)
    is_public = forms.BooleanField(required=False)

class EditForm(forms.Form):
    """ This is the edit form, for editing an excisting online
    experiment """
    title = forms.CharField(label='Choose a title')
    start_date = forms.DateField(required=False)
    end_date = forms.DateField(required=False)

class CreateTokenForm(forms.Form):
    """ This is the upload form, for uploading OS-scripts and
    creating an online experiment """
    nr_tokens = forms.IntegerField(max_value=1000, min_value=1)
