from django.urls import path
from . import views

urlpatterns = [
    path("", views.Categories.as_view()),  # as_view()::class를 가져오려면 as_view()를 해줘야 함 ==장고 규칙
    path("<int:pk>", views.CategoryDetail.as_view()),
]
# as_view() :: 요청이 GET이면 def get(~)code실행
# as_view() ::  요청이 POST이면 def post(~)code실행

"""
urlpatterns = [
    path("", views.categories),
    path("<int:pk>", views.category)
]
"""
