from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from . import serializers
from .models import User
from rooms.models import Room
from reviews.models import Review
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound, NotAuthenticated, ParseError, PermissionDenied 
from rest_framework.permissions import IsAuthenticated
 
from rooms.serializers import RoomListSerializer
from reviews.serializers import ReviewSerializer

class Me(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user=request.user
        serializer=serializers.PrivateUserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user=request.user
        serializer=serializers.PrivateUserSerializer(
            user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            user=serializer.save()
            serializer = serializers.PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)    

class Users(APIView):#user가 새로운 계정을 만들려고 할떄 
    
    def post(self, request):
        password=request.data.get('password')#user가 새로운 계정을 만들때 password를 안보내면, 에러 발생 
        if not password:#password유효성 검사 check!
            raise ParseError('password must be inserted')
            

        serializer=serializers.PrivateUserSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()#user를 DB에 저장, 이때까지는 user가 password를 갖고 있지 않음 
            user.set_password(password)#입력 받은 password를 해쉬화(django가 알아서 함) 하여 저장
            user.save()#user는 이제 비밀번호를 갖고 있어 
            serializer=serializers.PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)    

class PublicUser(APIView): #공개 프로필을 보고 싶어하는 사람들을 위함(누군가의 프로필을 보고 싶어)  
    def get(self, request, username):
        try:
            user=User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound
        
        serializer=serializers.PublicUserSerializer(user)
        return Response(serializer.data)


class PublicUserRooms(APIView): #1.사용자를 불러와야 함. 2. 불러온 사용자의 room field를 불러옴 
    
    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExists:
            raise NotFound 

    def get(self, request, username):
        user = self.get_object(username)
        serializer=RoomListSerializer( 
            user.rooms.all(),
            context={"request": request},
            many=True,
        )
        return Response(serializer.data)      

class PublicUserReviews(APIView):
    
    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExists:
            raise NotFound 

    def get(self, request, username):
        user = self.get_object(username)
        serializer = ReviewSerializer(
            user.reviews.all(),
            many=True,
        )
        return Response(serializer.data)        
class ChangePassword(APIView):
        
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user=request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        if not old_password or not new_password:
            raise ParseError
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
            {"old_password":"admin", "new_password":"12345"}

class LogIn(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            raise ParseError
        user = authenticate(
            request,
            username = username,
            password = password,
        )    
        if user:
            login(request, user)
            return Response({"ok":"Welcome!"})
        else:
            return Response({"error":"wrong Password"})


class LogOut(APIView):
    
    permission_classes=[IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"ok good bye":"See You!"})
