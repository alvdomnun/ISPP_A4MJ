from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.

def index(request):
	template = loader.get_template('welcome/index.html')
	context = {}
	return HttpResponse(template.render(context, request))

def web_index(request):
	template = loader.get_template('web/index.html')
	context = {}
	return HttpResponse(template.render(context, request))

def sample_dashboard(request):
	template = loader.get_template('samples/sampleDashboard.html')
	context = {}
	return HttpResponse(template.render(context,request))

def notebook(request):
	template = loader.get_template('notebook/notebookv1.html')
	context = {}
	return HttpResponse(template.render(context,request))