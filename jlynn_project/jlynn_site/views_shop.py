from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from .models import Art

def art_store(request):

    collection = Art.objects.all()


    if request.method == 'POST':

        print("got here, art_store")


    return render(request, 'store_page.html', {'collection' : collection})
