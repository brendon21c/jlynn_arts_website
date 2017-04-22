from django.shortcuts import render
from .models import Art


# Create your views here.

def homepage(request):

    collection = Art.objects.all()

    return render(request, 'home_page.html', {'collection' : collection })
