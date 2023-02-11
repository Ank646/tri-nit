from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime
# Create your models here.

User = get_user_model()


class ngo(models.Model):
    ngoname = models.ForeignKey(User, on_delete=models.CASCADE)
    ngoregid = models.TextField()
    ngofield = models.TextField(blank=True)
    ngoaddress = models.TextField(blank=True)
    ngofundneeds = models.TextField(blank=True)
    ngotype = models.CharField(max_length=100, blank=True)
    ngocity = models.TextField(blank=True)
    ngostate = models.TextField(blank=True)
    ngowork = models.TextField(blank=True)
    ngoplan = models.TextField(blank=True)
    ngoendgoal = models.TextField(blank=True)
    ngogoal = models.TextField(blank=True)
    ngowork = models.TextField(blank=True)
    ngovision = models.TextField(blank=True)
    ngoabout = models.TextField(blank=True)
    ngofb = models.TextField(blank=True)
    ngoinsta = models.TextField(blank=True)
    ngolinked = models.TextField(blank=True)
    ngotwitter = models.TextField(blank=True)
    ngoweb = models.TextField(blank=True)

    def __str__(self):
        return self.ngoname.username


class userpro(models.Model):
    userid = models.TextField(blank=True)
    userbio = models.TextField(blank=True)
    firstname = models.TextField(blank=True)
    lastname = models.TextField(blank=True)
    password = models.TextField(blank=True)
    kindofngo = models.TextField(blank=True)
