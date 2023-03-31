from django.utils import timezone

from rest_framework import serializers
from rest_framework.serializers import ValidationError
from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import ParseError

from .models import Experience , Perk
from users.serializers import TinyUserSerializers
from categories.serializers import CategorySerializer
 

class ExperienceSerializer(ModelSerializer):
    host = TinyUserSerializers(read_only=True)
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model=Experience
        fields = (
            "id",
            "name",
            "perks",
            "host",
            "category",
            "start",
            "end",
        )


class ExperienceDetailSerializer(ModelSerializer):
    host = TinyUserSerializers(read_only=True)
    category = CategorySerializer(read_only=True)
    
    books_cnt=serializers.SerializerMethodField()

    class Meta:
        model=Experience
        exclude=("perks",)

    def get_books_cnt(self, obj):
        return obj.books.count()

    def validate_price(self, value):
        if value<0:
            raise ValidationError("Price must be positive")
        else: return value

    def validate_start(self, value): #Custom-validation 
        now=timezone.localtime(timezone.now()).time()
        if now > value:
            raise serializers.ValidationError("OOPS! Start Time not in the past")
        else: return value

    def validate_end(self, value):
        now=timezone.localtime(timezone.now()).time()
        if now > value:
            raise serializers.ValidationError("OOPS! End Time not in the past")
        else: return value
    
    def validate(self, value): 
       
        if not(value.get("start") or value.get("end")):
            return value
        if value.get("start") and value.get("end"):
            if value.get("end") <= value['start']:
                raise serializers.ValidationError("End time is should be later than Start time")
            else: return value
        
        else: raise ValidationError("must be required both")

class PerkSerializer(ModelSerializer):
    class Meta:
        model = Perk
        fields = "__all__"
