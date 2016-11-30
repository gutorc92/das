from django.shortcuts import render
from django.views import View
from .models import *
from .forms import FileFieldForm
from django.conf import settings
from extern import *
import os

path_img = os.path.join(settings.BASE_DIR, "images")

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
        create_categories()
        categories = Category.objects.all()
        return render(request, "gallery/create.html",{'form': form, 'categories':categories})


def create_categories():
   cats,  created = Category.objects.get_or_create(name="Cats")
   dogs,  created = Category.objects.get_or_create(name="Dogs")
   faces, created = Category.objects.get_or_create(name="Faces")
   return cats, dogs, faces
