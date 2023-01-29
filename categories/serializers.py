from rest_framework import serializers
from .models import Category

# Category를 어떻게 Serialize 할지(번역) 결정
#  Category가 어떻게 API바깥으로 나갈때 표시되는 방법을 정할 수 있다.
# 1, 어떻게 번역할것인지
# 2, 무엇을 번역할것인지 :: 무엇을 보여주고 무엇을 안보여줄지


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        # serializer가 나의 category model을 위한 serializer를 만들고
        # 추가로 create-Method, update-Method를 만들어줌.

        # fields = ("name","kind","created_at",)  # want show fields one by one
        # exclude = ("created_at",)  # exclude this fields
        fields = ("name", "kind")  # want show all fields from category model
