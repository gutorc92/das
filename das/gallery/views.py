from django.shortcuts import render
from django.views import View
from .models import *
from .forms import FileFieldForm
from django.conf import settings
from extern import *
import os
from os import walk

path_img = os.path.join(settings.BASE_DIR, "images")

def handle_uploaded_file(f, name):
    with open(name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

class CreateGallery(View):

    def post(self, request):
        files = request.FILES.getlist('file_field')
        form = FileFieldForm(request.POST, request.FILES)
        if form.is_valid():
            return self.get(request)

        else:
            return render(request, "gallery/create.html",{'form': form})
     
    def get(self, request):
        form = FileFieldForm()
        return render(request, "gallery/create.html",{'form': form})
        

def create_categories():
   cats,  created = Category.objects.get_or_create(name="Cats")
   dogs,  created = Category.objects.get_or_create(name="Dogs")
   faces, created = Category.objects.get_or_create(name="Faces")
   return cats, dogs, faces
# Create your views here.
