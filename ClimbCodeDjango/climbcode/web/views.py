from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.

def index(request):
	template = loader.get_template('web/index.html')
	context = {}
	return HttpResponse(template.render(context, request))

def notebookv1(request):
	template = loader.get_template('web/notebookv1.html')
	context = {}
	return HttpResponse(template.render(context, request))

def notebookv1aux(request):
	template = loader.get_template('web/notebookv1aux.html')
	context = {}
	return HttpResponse(template.render(context, request))