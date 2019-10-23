# from django.shortcuts import render
# Create your views here.
from django.http import *


def index():
    return HttpResponse('hello world!')