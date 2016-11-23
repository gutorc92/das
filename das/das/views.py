from django.shortcuts import render
from gallery.forms import FileFieldForm

def index(request):
	form = FileFieldForm()
	return render(request, 'gallery/index.html', {'form': form})