from django.contrib import admin
from os_online.experimenter.models import Experiment, Result, Token

admin.site.register(Experiment)
admin.site.register(Result)
admin.site.register(Token)
