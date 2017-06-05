'''Defines URL patterns for learning_logs'''
from django.conf.urls import url
from . import views

urlpatterns = [
    #home page
    url(r'^$', views.index, name = 'index'),
    #show all topics.
    url(r'^topics/$', views.topics, name = 'topics'),
    #detail page for a single topic
    url(r'^topics/(?P<topic_id>\d+)/$', views.topic, name = 'topic'),
    #page for adding a new topic
    url(r'^new_topic/$', views.new_topic, name = 'new_topic'),
    #page for adding a new entry, forgot to make this...hard to debug
    url(r'^new_entry/(?P<topic_id>\d+)/$', views.new_entry, name = 'new_entry'),
    #page for editing an entry
    url(r'^edit_entry/(?P<entry_id>\d+)/$', views.edit_entry, name = 'edit_entry'),
    
]
