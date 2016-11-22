from django.shortcuts import render
from django.views import View
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
        files = request.FILES.getlist('file_field')
        form = FileFieldForm(request.POST, request.FILES)
        if form.is_valid():
            for f in files:
                handle_uploaded_file(f, os.path.join(path_img, f.name))
            for (dirpath, dirnames, filenames) in walk(path_img):
                for f in filenames:
                    print(f)
                    d = Input(os.path.join(path_img,f))
                    o.outFaces(face.detect(d.getImage(Input.FACES)))
                    dogs,cats = n.result(d.getImage(Input.PREDICTION))
                    o.outAnimals(dogs,cats)

            vectors, img_files = load_dataset(path_img)
            KNN = NearestNeighbors(Xtr=vectors, img_files=img_files, images_path=path_img, labels=labels)

# Freeing memory:
            del vectors
            return self.get(request)

        else:
            return render(request, "gallery/create.html",{'form': form})
     
    def get(self, request):
        form = FileFieldForm()
        return render(request, "gallery/create.html",{'form': form})
        

# Create your views here.
