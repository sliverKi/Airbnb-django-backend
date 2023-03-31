from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import User


class TinyUserSerializers(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "name",
            "avatar",
            "username",
        )
class PrivateUserSerializer(ModelSerializer):#본인 계정 
    class Meta:
        model=User
        exclude=(#본인 계정으로 접속하였을 때, user가  변경하면 안되는 사항들 
            "password",
            "is_superuser",
            "is_staff",
            "id",
            "is_active",
            "first_name",
            "last_name", 
            "groups",
            "user_permissions",
            )     


class PublicUserSerializer(ModelSerializer):
#1. code challenge(11.12)
# - 사람들이 내 프로필에서 리뷰를 볼 수 있게 하는 것 
# - 사람들이 내가 몇 개의 방을 가지고 있는지 
    my_reviews = serializers.SerializerMethodField()
    my_rooms = serializers.SerializerMethodField()

    class Meta:
        model=User
        fields = (
            "name",
            "avatar",
            "username",
            "my_reviews",
            "my_rooms",
        )     

    def get_my_rooms(self, obj):
        return obj.rooms.count() 
    def get_my_reviews(self, obj):
        return obj.reviews.count()
        
