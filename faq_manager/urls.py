from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin
from .views import faq_list

urlpatterns = [
    path("faqs/", faq_list, name="faq_list"),
    path("ckeditor/", include("ckeditor_uploader.urls")), 
    path("admin/", admin.site.urls),  # Fix: Directly reference `admin.site.urls`
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
