
from django.contrib import admin
from django.urls import path, include
from rooms import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/rooms/", include("rooms.urls")),
    # rooms 파일로 가서 -> urls.py를 찾음
    path("api/v1/categories/", include("categories.urls")),
    path("api/v1/experiences/", include("experiences.urls")),
    
    path("api/v1/medias/", include("medias.urls")),
    path("api/v1/wishlists/", include("wishlists.urls")),

    path("api/v1/users/", include('users.urls')),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
