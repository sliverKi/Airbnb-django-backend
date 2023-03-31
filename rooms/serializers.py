from rest_framework import  serializers
from rest_framework.serializers import ModelSerializer
from .models import Amenity, Room
from users.serializers import TinyUserSerializers
from categories.serializers import CategorySerializer
from reviews.serializers import ReviewSerializer
from medias.serializers import PhotoSerializer
from wishlists.models import Wishlist


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity  # 번역하고 싶은 model
        fields = (
            "name",
            "description",
        )  # 노출시키고 싶은 필드
    
class RoomDetailSerializer(serializers.ModelSerializer):
    owner = TinyUserSerializers(
        read_only=True,
    )
    # read_only=True :: 우리가 방을 생성할때 serializer는 owner에 대한 정보를 요구 하지 않음
    # owner를 serializer하는 경우 user폴더의 TinyUserSerializers 를 이용해라
    amenities = AmenitySerializer(
        read_only=True, 
        many=True,
    )
    category = CategorySerializer(
        read_only=True,
    )
    # many=True : CategorySerializer가 list or array 인 경우, many=True 를 사용,
    # but 단순 숫자 하나인 경우 many=True를 사용하지 않는다.
    # nested serializer :: Serializer 안에 또 다른 Serializer가 중첩된 형태
    # nested serializer :: owner(FK), amenities(MtM), category (FK)
    
   
    #rating, banana==내 serializer에 '추가적인 필드를 넣기 위해' 넣을 모델 안의 속성과 다른 이름으로 필드를 하나 생성함.
    #SerializerMethodField::  네가 potato의 값을 계산할 method를 만들거야.!를 의미
                            #현재 serializing하고 있는 오브젝트와 함께 호출함 
    rating = serializers.SerializerMethodField()
    is_liked= serializers.SerializerMethodField()
    #is_liked==is_on_wishlist(해당 방이 이미 wishlist에 있는지 없는지 user에게 보여주기 위함)
    is_owner=serializers.SerializerMethodField()#새로운 속성 만듦
        #유저에 따라 true,false..를 알려줌 
    reviews = ReviewSerializer(
        many=True,
        read_only=True,
    )
    photos=PhotoSerializer(
        many=True,
        read_only=True,
    )
    class Meta:
        model = Room
        fields = "__all__"
    
    def get_rating(self,room):#평점을 계산하기 위해 method생성 
                                   #method-covention:: 메서드 이름은 계산하려는 속성의 이름앞에 ,get_을 붙임  
        print(room)
        return room.rating()

    def get_is_owner(self, room):#어떤 유저가 방을 소유했는지 안했는지 알려주는 메서드 

        request=self.context['request']#context에서 request를 꺼내
        return room.owner==request.user#방의 owner가 요청을 보내 user와 동일한지 아닌지에 따라 
        #유저에 따라 true,false..를 알려줌 
    
    def get_is_liked(self,room):
        request=self.context['request'] # 어떤 user가 이 방을 보고 있는지 확인하기 위함
        return Wishlist.objects.filter(
            user=request.user, 
            room__pk=room.pk
        ).exists() #우선 user가 소유한 wishlist를 불러와야~> filter:: user가 여러개의 wishlist를 가질 수 있어 
        #user가 보고있는 방을 room_list 안에 있는 wishlist를 찾기
        #rooms__pk=room.pk :: user가 만든 wishlist중에 room_id가 있는 room_list를 포함한 wishlist를 찾아 
        


    
# IN VIEWS.PY >
# room = serializer.save(owner=request.user)
# USER-DATA로만 serilalizer를 하게 되면, create_method가 호출되어지고
# 이때 'owner=request.user. ~>  validated_data에 자동으로 추가되어 짐
#    def create(self, validated_data):
#        return Room.objects.create(**validated_data)
# ~> owner를 포함한 all_data를 가지고 방을 생성해줌
# create_method :: 항상 모델의 인스턴스를 리턴
class RoomListSerializer(serializers.ModelSerializer):
    
    rating= serializers.SerializerMethodField()#make field
    is_owner=serializers.SerializerMethodField()
    photos=PhotoSerializer(
        many=True,
        read_only=True,
    )
    
    class Meta:
        model = Room
        fields = (#노출할 필드 
            "pk",
            "name",
            "country",
            "city",
            "price",
            "rating",
            "is_owner",#views.py > Rooms-class의 get Method context에 접근
            "photos",
        )

        # depth = 1  # serialize를 통해 관계의 확장을 보여줌
        # django, rest_framework는 owner의 id 1에 해당하는 이 object를 serialize한 다음, 데이터를 넣음
        # id 1에 해당하는 숫자를 가지는 대신에 사용자의 전체를 갖게 된다.
        # 단점 : 한번에 이런 모든 data가 필요하지 않다.~>>customize불가

    def get_rating(self, room):#make method, (self, 내 serializer에 추가할 field가 속한 model명)
        print(self.context)
        return room.rating()

    def get_is_owner(self, room):
        request=self.context["request"]
        return request.user==room.owner

     