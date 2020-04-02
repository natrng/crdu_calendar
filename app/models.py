from django.db import models
from django.db import models
from django.contrib import messages
from django.contrib.messages import get_messages
from datetime import datetime as dt
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validator(self, data):
        errors = {}
        if len(data['fname'])<2:
            errors['fname'] = 'First must be at least 2 characters'
        if len(data['lname'])<2:
            errors['lname'] = 'Last must be at least 2 characters'
        if not EMAIL_REGEX.match(data['email']):
            errors['email'] = 'Email is invalid'
        if len(data['password'])<8:
            errors['password'] = 'Password must be at least 8 characters'
        if data['password']!=data['cpassword']:
            errors['cpassword'] = 'Passwords much match'
        
        return errors

class EventManager(models.Manager):
    def validator(self, data):
        errors = {}
        if len(data['title'])==0:
            errors['title'] = 'Title cannot be empty'
        if data['start']=="":
            errors['start'] = 'Starting time cannot be empty'
        else:
            if dt.strptime(data['start'], '%Y-%m-%d') < dt.today():
                errors['start'] = 'Date cannot be in the past'
            if dt.strptime(data['start'], '%Y-%m-%d')>dt.strptime(data['end'], '%Y-%m-%d'):
                errors['start'] = 'Starting time cannot be before ending time'
        if data['end']=="":
            errors['end'] = 'Ending time cannot be empty'
        else:
            if dt.strptime(data['end'], '%Y-%m-%d') < dt.today():
                errors['end'] = 'Date cannot be in the past'
            if dt.strptime(data['start'], '%Y-%m-%d')>dt.strptime(data['end'], '%Y-%m-%d'):
                errors['start'] = 'Starting time cannot be before ending time'
        if data['time_end']=="":
            errors['time_end'] = 'Ending time cannot be empty'
        if data['time_start']=="":
            errors['time_start'] = 'Ending time cannot be empty'
        if data.get('urgent') is None and data.get('urgentE') is None:
            errors['urgent'] = 'Must define urgency'
        return errors
        

class User(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.CharField(max_length=60)
    password = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start = models.DateTimeField()
    time_start = models.TimeField()
    end = models.DateTimeField()
    time_end = models.TimeField()
    urgent = models.CharField(max_length=100)
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    objects = EventManager()