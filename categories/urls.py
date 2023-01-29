from django.urls import path
from . import views


urlpatterns = [
    path(
        "",
        views.CategoryViewSet.as_view(
            {  # ACTION정의~> ViewSet의 메서드와 - HTTP 메서드 연결
                "get": "list",
                "post": "create",
            },
        ),
    ),  # as_view()::class를 가져오려면 as_view()를 해줘야 함 ==장고 규칙
    path(
        "<int:pk>",
        views.CategoryViewSet.as_view(
            {
                "get": "retrieve",
                "put": "partial_update",
                "delete": "destroy",
            },
        ),
    ),
]


"""VERSION2
urlpatterns = [
    path("", views.Categories.as_view()),  # as_view()::class를 가져오려면 as_view()를 해줘야 함 ==장고 규칙
    path("<int:pk>", views.CategoryDetail.as_view()),
]
# as_view() :: 요청이 GET이면 def get(~)code실행
# as_view() ::  요청이 POST이면 def post(~)code실행
"""

"""VERSION1
urlpatterns = [
    path("", views.categories),
    path("<int:pk>", views.category)
]
"""
