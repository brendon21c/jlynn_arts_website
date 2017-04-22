from django.shortcuts import render
from .models import Art


# Create your views here.

def homepage(request):


    return render(request, 'home_page.html')
