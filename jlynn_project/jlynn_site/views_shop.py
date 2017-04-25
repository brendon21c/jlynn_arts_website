from django.shortcuts import render
from .models import Art

def art_store(request):

    collection = Art.objects.all()


    if request.method == 'POST':

        print("got here") # TODO need to figure out how to get what item was selected.


    return render(request, 'store_page.html', {'collection' : collection})
