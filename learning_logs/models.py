from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
    '''a topic the user is learning about'''
    text = models.CharField(max_length = 200) #topic length max 200 characters
    date_added = models.DateTimeField(auto_now_add = True) #set to true which sets this to the current time
    owner = models.ForeignKey(User)
    def __str__(self):
        '''return a string representation of the model'''
        return self.text
class Entry(models.Model):
    '''something specific learned about a topic'''
    topic = models.ForeignKey(Topic)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add = True)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        '''return a string representation of the model'''
        if len(self.text) < 50:#from crash course book
            return self.text    #if the entry is less than 50 characters no ellipsis shown
        else:
            return self.text[:50] + '...'
