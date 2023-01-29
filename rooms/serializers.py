from rest_framework.serializers import ModelSerializer
from .models import Amenity, Room
from users.serializers import TinyUserSerializers
from categories.serializers import CategorySerializer


class RoomListSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
        )
        # depth = 1  # serialize를 통해 관계의 확장을 보여줌
        # django, rest_framework는 owner의 id 1에 해당하는 이 object를 serialize한 다음, 데이터를 넣음
        # id 1에 해당하는 숫자를 가지는 대신에 사용자의 전체를 갖게 된다.
        # 단점 : 한번에 이런 모든 data가 필요하지 않다.~>>customize불가


class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity  # 번역하고 싶은 model
        fields = (
            "name",
            "description",
        )  # 노출시키고 싶은 필드


class RoomDetailSerializer(ModelSerializer):
    owner = TinyUserSerializers(read_only=True)
    # read_only=True :: 우리가 방을 생성할때 serializer는 owner에 대한 정보를 요구 하지 않음
    # owner를 serializer하는 경우 user폴더의 TinyUserSerializers 를 이용해라
    amenities = AmenitySerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    # many=True : CategorySerializer가 list or array 인 경우, many=True 를 사용,
    # but 단순 숫자 하나인 경우 many=True를 사용하지 않는다.
    # nested serializer :: Serializer 안에 또 다른 Serializer가 중첩된 형태
    # nested serializer :: owner(FK), amenities(MtM), category (FK)

    class Meta:
        model = Room
        fields = "__all__"


# IN VIEWS.PY >
# room = serializer.save(owner=request.user)
# USER-DATA로만 serilalizer를 하게 되면, create_method가 호출되어지고
# 이때 'owner=request.user. ~>  validated_data에 자동으로 추가되어 짐
#    def create(self, validated_data):
#        return Room.objects.create(**validated_data)
# ~> owner를 포함한 all_data를 가지고 방을 생성해줌
# create_method :: 항상 모델의 인스턴스를 리턴
