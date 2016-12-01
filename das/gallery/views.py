from django.shortcuts import render
from django.views import View
from .models import *
from .forms import FileFieldForm
from django.conf import settings
from extern import *
import os

path_img = os.path.join(settings.BASE_DIR, "images")

def handle_uploaded_file(files):
    for f in files:
        with open(os.path.join(path_img,f.name), 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

def create_gallery():
    for file_name in os.listdir(path_img):
        category_labels = creating_gallery(os.path.join(path_img,file_name))
        nr_id, name = category_labels[0].split(" ", 1)
        category, created = Category.objects.get_or_create(nr_id=nr_id,name=name)
        print(category.pk)
        p, created = Picture.objects.get_or_create(name=file_name,
                                          path = os.path.join(path_img,file_name),
                                          category=category)


class CreateGallery(View):

    def post(self, request):
        files = request.FILES.getlist('file_field')
        form = FileFieldForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(files) 
            create_gallery()
            return self.get(request)
        else:
            return render(request, "gallery/create.html",{'form': form})

    def get(self, request):
        form = FileFieldForm()
        categories = Category.objects.all()
        return render(request, "gallery/create.html",{'form': form, 'categories':categories})


def create_categories():
   cats,  created = Category.objects.get_or_create(name="Cats")
   dogs,  created = Category.objects.get_or_create(name="Dogs")
   faces, created = Category.objects.get_or_create(name="Faces")
   return cats, dogs, faces
