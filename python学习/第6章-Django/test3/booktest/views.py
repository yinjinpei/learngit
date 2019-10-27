from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
    return HttpResponse('hello index !!')

def index2(request):
    return HttpResponse('hello booktest index2 !!')

def detail(request,number):
    return HttpResponse(number)
