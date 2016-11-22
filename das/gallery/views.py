from django.shortcuts import render
from django.views import View
from .models import *
from .forms import FileFieldForm
from django.conf import settings
from extern import *
import os
from os import walk

path_img = os.path.join(settings.BASE_DIR, "images")
face = Face()
n = Net()
o = Output()

def handle_uploaded_file(f, name):
    with open(name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

class CreateGallery(View):

    def post(self, request):
        cats, dogs, faces = create_categories()
        files = request.FILES.getlist('file_field')
        form = FileFieldForm(request.POST, request.FILES)
        if form.is_valid():
            for f in files:
                handle_uploaded_file(f, os.path.join(path_img, f.name))
            for (dirpath, dirnames, filenames) in walk(path_img):
                for f in filenames:
                    print(f)
                    path_image = os.path.join(path_img,f)
                    d = Input(path_image)
                    if len(face.detect(d.getImage(Input.FACES))) > 0:
                       p = Picture.objects.create(name=f, path=path_image,category=faces)
                    d, c = n.result(d.getImage(Input.PREDICTION))
                    o.outAnimals(d,c)
            
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
