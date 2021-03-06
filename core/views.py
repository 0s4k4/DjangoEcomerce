from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

#se añade la function de home
def home(request) :
    return render(request, 'home.html', {'name' : 'andika'})