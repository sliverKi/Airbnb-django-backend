from django.urls import path
# ExperienceBookDetail,
from .views import (
    Experiences, ExperienceDetail, 
    ExperiencePerk, ExperienceBook, ExperienceBookDetail, 
    Perks, PerkDetail
)
urlpatterns = [
    path("", Experiences.as_view()),
    path("<int:pk>", ExperienceDetail.as_view()),
    path("<int:pk>/perks",ExperiencePerk.as_view()),
    path("<int:pk>/bookings",ExperienceBook.as_view()),
    path("<int:pk>/bookings/<int:pk>", ExperienceBookDetail.as_view()),
    path("perks/", Perks.as_view()),
    path("perks/<int:pk>", PerkDetail.as_view()),
]