from django.conf.urls import url
from .views import CreateGallery, AddPicture, ListPictures

urlpatterns = [
    url(r'create/', CreateGallery.as_view(), name="create"),
    url(r'newpicture/', AddPicture.as_view(), name="newpicture"),
    url(r'listpictures/(?P<id>\d+)/', ListPictures.as_view(), name="listpicture"),

]
