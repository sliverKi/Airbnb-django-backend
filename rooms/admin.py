from django.contrib import admin
from .models import Room, Amenity

# action을 만들기 위해서는 admin.action decorator를 적용한 함수를 만들어야 한다.
# description :: 관리자 패널에 나타나 (in action-searchfield)
@admin.action(description="Set all prices to zero")
def reset_prices(model_admin, request, rooms):  # queryset  # (model_admin :: 해당 action을 호출하는 클래스,
    # request:: 액션을 요청하는 user의 요청,
    # queryset :선택한 요소들을 리스트형태로 보여줌)
    # print(model_admin)
    # print(dir(request.user))
    # print(queryset)
    # pass
    for room in rooms.all():
        room.price = 0
        room.save()


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    actions = (reset_prices,)

    list_display = (  # 속성과 메서드 적을 수 있음
        "name",
        "price",
        "kind",
        "total_amenities",
        "rating",
        "owner",
        "description",
        "rooms",
        "created_at",
    )
    list_filter = (
        "country",
        "city",
        "toilets",
        "amenities",
        "kind",
        "price",
        "updated_at",
        "created_at",
    )

    def total_amenities(self, room):
        return room.amenities.count()

    # def total_rating(self, room):
    #     return room.reviews.set()
    ##검색창 만들기
    search_fields = (
        # "^name",
        # "^price"
        "owner__username",  # owner의 username으로 검색
        # ^, = 활용가능
    )
    # name: ==__contains__
    # ^name: ==__startswith__ / ~으로 시작하는 이름으로 찾고 싶어
    # =name: equals / 100%같은 값
    # ^price: 검색창에 2라고 쳤을때, 2로 시작하는 가격만 나옴


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "updated_at",
        "created_at",
    )
    readonly_fields = (
        "updated_at",
        "created_at",
    )
