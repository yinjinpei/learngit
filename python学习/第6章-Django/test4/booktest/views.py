# coding:utf-8
from django.shortcuts import render
from django.db.models import Max,F,Q
from .models import *
# Create your views here.


def index(request):
    return render(request, 'booktest/index.html')