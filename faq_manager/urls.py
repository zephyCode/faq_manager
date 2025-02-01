from django.contrib import admin
from django.urls import path
from .views import faq_list 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('faq/', faq_list, name='faq-list'),
]
