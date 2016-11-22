from django.conf.urls import url
from .views import CreateGallery

urlpatterns = [
    url(r'create/', CreateGallery.as_view(), name="create"),

]
