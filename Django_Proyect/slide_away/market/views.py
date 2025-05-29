from django.shortcuts import render
from django.http import HttpResponse
import requests
def ver_inicio(request):
    return render(request,"inicio.html")