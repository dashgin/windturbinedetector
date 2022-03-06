from django.contrib import admin
from django.urls import path
from app.views import DetectLocationAPIView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/locations/", DetectLocationAPIView.as_view(), name="locations"),
]
