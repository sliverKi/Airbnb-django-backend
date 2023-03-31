from rest_framework import serializers
from .models import Review
from users.serializers import TinyUserSerializers

#reviewSerializer를 갖고 있고 방들이 rooms.reviews를 가지고 있다.
#~> 장고가 자동으로 역접근자를 두기 때문에 가능함
#room model이 reviews라는 property를 명시적으로 갖고 있지 않아도 
#장고는 reviews property를 두게 됨.

## 역접근자는 자동으로 추가가 되고, related_name을 이용하여 모양을 변경할 수 있다.
class ReviewSerializer(serializers.ModelSerializer):
    user=TinyUserSerializers(read_only=True,)
    #read_only=True :: request.data에 유저가 업슨 상태로 내 serializer가 유효하기 위해서 사용
    class Meta:
        model=Review
        fields=(
            "user",
            "payload",
            "rating",
        )