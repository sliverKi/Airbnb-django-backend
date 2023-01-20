from django.contrib import admin
from .models import Review


class WordFilter(admin.SimpleListFilter):
    title = "Filter by words"
    parameter_name = "words"  # url에 나타나

    def lookups(self, request, model_admin):
        # lookups :: tuple의 list를 return해야 하는 함수
        # return('url에 나타나는 요소', "user가 보고 필터링할 단어")
        return [
            ("good", "Good"),
            ("great", "Great"),
            ("awesome", "Awesome"),
        ]

    def queryset(self, request, reviews):
        # queryset::필터링된 객체
        # self::를 받아야 하는 이유 :: class의 method이기 때문

        word = self.value()  # print(self.value())
        # request.GET=={'words': '[good]'}
        # dict안의 list의 value값을 추출하기 위하여 객체.value()에 접근
        if word == "good":
            return reviews.filter(payload__contains=word).filter(rating__gt=2)
        else:
            return reviews


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "payload",
    )
    list_filter = (
        WordFilter,
        "rating",
        "user__is_host",
        "room__category",
        "room__pet_friendly",
    )


# user의 FK를 기반으로 리뷰를 필터링 할 수 있다.
