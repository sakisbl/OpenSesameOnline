from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render

def baseurl(request):
        """
        Return a BASE_URL template context for the current request.
        """
        if request.is_secure():
            scheme = 'https://'
        else:
            scheme = 'http://'                                                
        return {'BASE_URL': scheme + request.get_host(),}
