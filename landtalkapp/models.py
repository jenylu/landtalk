from __future__ import unicode_literals

import datetime
import os
from uuid import uuid4
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

def path_and_rename(path, name):
        def wrapper(instance, filename):

            ext = filename.split('.')[-1]

            # get filename
            if instance.pk:
                filename = '{}.{}.{}'.format(instance.pk, name, instance.location)
            else:
                # set filename as random string
                filename = '{}.{}'.format(uuid4().hex, name)
            
            print "filename: ", filename
            # return the whole path to the file
            return os.path.join(path, filename)
        return wrapper

def defaultYear():
    return datetime.datetime.now().year

class Submission(models.Model):
    YEAR_CHOICES = [(r,r) for r in range(1900, datetime.datetime.now().year+1)]

    pub = models.BooleanField(('Publish'), default=False)
    # privkey = models.IntegerField(('PK'), default=-1)
    location = models.CharField(max_length=50) #char field?
    lat = models.FloatField(('Latitude')) #restrictions?
    lng = models.FloatField(('Longitude'))
    steward = models.ForeignKey(User)
    interviewer = models.CharField(max_length=50) #check this max length
    observer = models.CharField(max_length=50)
    videourl = models.URLField(('Video URL')) #check max length, default 200
    hist_img = models.ImageField(('History Image'), upload_to=path_and_rename('landtalk/', 'hist')) #default max length 100, specify height and width
    curr_img = models.ImageField(('Current Image'), upload_to=path_and_rename('landtalk/', 'curr'))
    
    time_submitted = models.DateTimeField(auto_now_add = True) 
    time_posted = models.DateTimeField(null = True) 
    hist_year = models.IntegerField(('History Year'), choices=YEAR_CHOICES, default=defaultYear())
    curr_year = models.IntegerField(('Current Year'), choices=YEAR_CHOICES, default=defaultYear())
    hist_caption = models.CharField(('History Caption'), max_length=200) #textfield? limit max_length?
    curr_caption = models.CharField(('Current Caption'), max_length=200)
    summary = models.TextField()
    key_words = models.TextField(('Key Words'))
    contact_org = models.URLField(('Contact Organization'))

    def save(self, *args, **kwargs):
        if self.pub is True:
            self.time_posted = timezone.now()
        else:
            self.time_posted = None
      
        # self.privkey = instance.pk
        
        # create folder for steward if does not exist
        # stewardPath = 'landtalk/' + str(self.steward)
        # if not os.path.exists(stewardPath):
        #     os.makedirs(str(self.steward))

        #upload images to steward folder and rename accordingly
        # self.hist_img = models.ImageField(('History Image'), upload_to=path_and_rename('/landtalk', 'hist'))
        # self.curr_img = models.ImageField(('Current Image'), upload_to=path_and_rename('/landtalk', 'curr'))

     # <marker id="1" name="Barrow" link="site/barrow.html" lat="71.2906" lng="-156.7886" youtube="https://www.youtube.com/embed/igVKR9--mbQ"/>

        super(Submission, self).save(*args, **kwargs)

    def publish(self):
        self.time_posted = timezone.now()
        self.save()

    def __str__(self):
        return self.location #?
