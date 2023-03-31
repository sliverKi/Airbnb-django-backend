from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Wishlist
from rooms.serializers import RoomListSerializer

class WishlistsSerializer(ModelSerializer):
    
    room=RoomListSerializer(
        many=True,
        read_only=True,
    )
    #우리는 유ㅓㅈㅈ가 위시리스트를 생성할때 우리에게 방을 보내는것을 원치 않음

    class Meta:
        model=Wishlist
        fields=(#노출 필드  
            "pk",
            "name", #~>우리는 user에게 위시리스트의 이름과
            "room", #~>위시리스트 안에 있는 방을 보여줌
        )
        #~>위시리스트의 소유자는 표시 안함 => 위시리스트를 보고 있는 유저가 바로 소유자이기 때문
        #~>본인이니까 유저의 프로필 보여줄 필요 없어 