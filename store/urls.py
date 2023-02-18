from django.contrib import admin
from django.urls import path,include
from store.views import Home,store,Payment
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('H',Home),
    path('S',Payment),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

