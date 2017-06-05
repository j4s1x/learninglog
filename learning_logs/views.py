from django.shortcuts import render
from .models import Topic, Entry
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required
def check_topic_owner(topic,request):
    if topic.owner != request.user:
        raise Http404
def index(request):
    '''the home page for learning log'''
    return render(request, 'learning_logs/index.html')
@login_required
def topics(request):
    '''Show all topics.'''
    topics = Topic.objects.filter(owner = request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)
@login_required
def topic(request, topic_id):
    '''show a single topic and all its entries.'''
    topic = Topic.objects.get(id = topic_id)
    #make sure topic belongs to current user
    check_topic_owner(topic, request)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)
@login_required
def new_topic(request):
    '''add a new topic'''
    if request.method != 'POST':
        #no data submitted create blank form
        form = TopicForm() #yeah, create that blank from from forms.py
    else:
        #POST data submitted; process data.
        form = TopicForm(request.POST)
        if form.is_valid(): #topic title shouldn't be above 200 characters as stated in another module somewhere
            new_topic = form.save(commit = False)
            new_topic.owner = request.user #associates new topics made with current user
            new_topic.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)  #show the page
@login_required
def new_entry(request, topic_id):
    '''add new entry for specific topic'''
    topic = Topic.objects.get(id = topic_id)
    check_topic_owner(topic, request)
    if request.method != 'POST':
        #create blank form
        form = EntryForm()
    else:
        #data submitted, process data
        form = EntryForm(data = request.POST)
        if form.is_valid():
            new_entry = form.save(commit = False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args = [topic_id]))
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)
@login_required
def edit_entry(request, entry_id):
    '''edit an existing entry'''
    entry = Entry.objects.get(id = entry_id)
    topic = entry.topic
    check_topic_owner(topic, request)
    if request.method != 'POST':
        #initial request, prefill form with current entry
        form = EntryForm(instance = entry)
    else:
        #POST data submitted, process data
        form = EntryForm(instance = entry, data = request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args = [topic.id]))
    context = {'entry': entry, 'topic':topic, 'form':form}
    return render(request, 'learning_logs/edit_entry.html', context)
