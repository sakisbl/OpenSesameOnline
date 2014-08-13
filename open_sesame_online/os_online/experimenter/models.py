"""This is the database model"""

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from managers import ActiveTokenManager, ExpiredTokenManager
import datetime
import hashlib


class Result(models.Model):
    """Result table"""
    experiment      = models.ForeignKey('Experiment')
    var_name        = models.CharField(max_length=50)
    var_value       = models.CharField(max_length=50)
    state           = models.PositiveIntegerField()
    person          = models.PositiveIntegerField()
    objects = models.Manager()

    def __unicode__(self):
        return self.var_value

class Token(models.Model):
    experiment = models.ForeignKey('Experiment')
    token = models.CharField(max_length=20, editable=False)
    used = models.BooleanField(('Token Used?'), default=False)
    perma_token = models.BooleanField(('Permanent Token?'), default=False)
    subject_nr = models.PositiveIntegerField()

    active_objects = ActiveTokenManager()
    expired_objects = ExpiredTokenManager()
    objects = models.Manager()
    def __unicode__(self):
        return u"%s" % (self.token)
    
    def generate_hash(self):
        """
        Create a unique SHA token/hash using the project SECRET_KEY, URL,
        email address and current datetime.
        """
        hash = hashlib.sha1(settings.SECRET_KEY\
                + unicode(datetime.datetime.now()) ).hexdigest()
        return hash[::2]

    """ if token doesn't exist create it on save """
    def save(self, **kwargs):
        if not self.pk:
            self.token = self.generate_hash()
        super(Token, self).save(**kwargs)
    
    """ make the url, token and associated email immutable """
    def __setattr__(self, name, value):
        if name in ['token']:
            if getattr(self, name, None): return
        super(Token, self).__setattr__(name, value)

class Experiment(models.Model):
    """Experiment table"""
    experimenter    = models.ForeignKey(User)
    title           = models.CharField(max_length=50)
    slug            = models.SlugField(unique=True)
    js_file         = models.FileField(upload_to='experiments/out/%Y%m%d')
    start_date      = models.DateField(null=True)
    end_date        = models.DateField(null=True)
    nr_participants = models.PositiveIntegerField(blank=True, editable=False, default=0)
    max_participants= models.PositiveIntegerField(blank=True, editable=False, default=0)
    is_open         = models.BooleanField(editable=False)
    is_public       = models.BooleanField()
    permalink       = models.OneToOneField(Token, related_name='is_permalink_of', null=True)
    def __unicode__(self):
        return self.title

    def startdate_after_enddate(self):
        return self.start_date >= self.end_date
