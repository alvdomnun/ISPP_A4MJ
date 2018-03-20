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

	cajas = []
	parameters = []
	parameters.append(Parameters("1"))
	parameters.append(Parameters("2"))
	parameters.append(Parameters("3"))

	cajas.append(Box("Texto","Textooooooooooooo",1))
	cajas.append(Box("Ilustracion","https://media1.tenor.com/images/039ef9592d0eb63596f695c1f65c2502/tenor.gif?itemid=9989174",2,parameters))
	cajas.append(Box("Codigo","2+1;",3))
	context = {
		'cajas' : cajas,
	}

	return HttpResponse(template.render(context, request))


class Box():
	def __init__(self, tipo=None, content=None, order=None, parameters=[]):
		self.tipo = tipo
		self.content = content
		self.order = order
		self.parameters = parameters

class Parameters():
	def __init__(self, id=None):
		self.id = id