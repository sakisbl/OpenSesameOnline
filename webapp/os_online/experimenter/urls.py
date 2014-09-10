""" This is the file where all urls for
    the app experimenter are stored """
from django.conf.urls import patterns, url

urlpatterns = patterns(
    'os_online.experimenter.views',
    url(r'^list/$', 'list_view', name='list_view'),
    url(r'^tokenlist/(?P<experiment_pk>.+)/$', 'token_list_view', name='token_list_view'),
    url(r'^createtoken/(?P<experiment_pk>.+)/$', 'create_token', name='create_token'),
    url(r'^upload/$', 'upload_view', name='upload_view'),
    url(r'^edit/(?P<experiment_pk>.+)/$', 'edit_view', name='edit_view'),
    url(r'^delete/(?P<experiment_pk>.+)/$', 'delete_view', name='delete_view'),
    url(r'^resultlist/(?P<experiment_pk>.+)/$', 'show_results', name='show_results'),
    url(r'^resultdownload/(?P<experiment_pk>.+)/$', 'export_csv', name='export_csv'),
    url(r'^tokendownload/(?P<experiment_pk>.+)/$', 'export_token_csv', name='export_token_csv'),
    url(r'^help/$', 'help_view', name='help_view'),
)