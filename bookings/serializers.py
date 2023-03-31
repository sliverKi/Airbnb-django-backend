from django.utils import timezone

from rest_framework import serializers
from .models import Booking

class CreateExperienceBookingSerializer(serializers.ModelSerializer):
    
    experience_time = serializers.DateTimeField()

    class Meta:
        model = Booking
        fields=(
            "guests",
            "experience_time",
        )
   
    def validate_experience_time(self, value):
        now=timezone.localtime(timezone.now())
        print(value)
        if value<now:
            raise serializers.ValidationError("OOPS! Can't book in the past")
        else: return value


class CreateRoomBookingSerializer(serializers.ModelSerializer):
#data를 생성만을 위한 serializer
    
    check_in = serializers.DateField() #model을 보게되면 check_in/out은
    check_out = serializers.DateField() # 필수 항목이 아니여서(null & blank =True) 여기에서 덮어씀
    

    class Meta:
        model=Booking
        fields=(#user에게 받고 싶은 data
            "check_in",
            "check_out",
            "guests",
        )
    
    def validate_check_in(self, value): #Custom-validation 
        now=timezone.localtime(timezone.now()).date()
        if value < now:
            raise serializers.ValidationError("OOPS! Can't book in the past")
        return value

    def validate_check_out(self, value):
        now=timezone.localtime(timezone.now()).date()
        if value < now:
            raise serializers.ValidationError("OOPS! Are you sure you check-out past?")
        return value
        
    def validate(self, data):
        print(data)
        if data['check_out'] <= data['check_in']:
            raise serializers.ValidationError("Check in should be smaller than check out")
        
        if Booking.objects.filter(
            check_in__lte=data['check_out'],
            check_out__gte=data['check_in'],
            ).exists():
            raise serializers.ValidationError("Those (or some) of those dates are already taken.")
        return data     

class PublicBookingSerializer(serializers.ModelSerializer):
#data를 보여주기 위한 serializer
    class Meta:
        model=Booking
        fields=(
            "pk",
            "check_in",
            "check_out",
            "experience_time",
            "guests",
        )