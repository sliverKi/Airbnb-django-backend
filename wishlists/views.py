from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated 
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_200_OK
from .models import Wishlist
from .serializers import WishlistsSerializer
from rooms.models import Room


class Wishlists(APIView):
    permission_classes = [IsAuthenticated]


    def get(self,request):#유저가 생성한 모든 위시리스트를 해당 유저에게 보여주는 get메서드
        all_wishlists=Wishlist.objects.filter(user=request.user)
        #filter: 유저에게 해당 유저가 만든 위시리스트만 보여줘
        #request(=유저data).user(중의 user)
       
        serializer=WishlistsSerializer(
            all_wishlists, 
            many=True,
            context={"request":request},
        ) 
        #모든 위시리스트를 번역하기 위해서는 serializer를 만들어야 함
        return Response(serializer.data)
    
    def post(self, request):#post=생성
        serializer=WishlistsSerializer(data=request.data) 
        if serializer.is_valid():
            wishlist=serializer.save(
                user=request.user,
            )
            serializer=WishlistsSerializer(wishlist)
            return Response(serializer.data)
        else: return Response(serializer.errors)    
    #post == make wishlist 
    #~> name_field 만 필요, 방이랑 경험은 나중에 내가 수정가능한 필드, user는 request.user로 부터 옴(굳이 전달할 필요 없어 )
    
class WishlistDetail(APIView):
    permission_classes=[IsAuthenticated]


    def get_object(self, pk,user):
        try :
            return Wishlist.objects.get(pk=pk, user=user)
            #Wishlist는 private영역=> user만 볼 수 있음 따라서 user도 같이 받아와야
        except Wishlist.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        wishlist=self.get_object(pk, request.user)
        serializer=WishlistsSerializer(wishlist)
        return Response(serializer.data)

    def delete(self, request,pk):
        wishlist=self.get_object(pk, request.user)
        wishlist.delete()
        return Response(status=HTTP_200_OK)

    def put(self, request,pk):
        wishlist=self.get_object(pk, request.user)
        serializer=WishlistsSerializer(
            wishlist, 
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            wishlist=serializer.save()    
            serializer=WishlistsSerializer(wishlist)
            return Response(serializer.data)

        else:
            return Response(serializer.errors)

class WishlistToggle(APIView):
    
    def get_list(self, pk, user):
        try:
            return Wishlist.objects.get(pk=pk, user=user)
        except Wishlist.DoesNotExist:
            raise NotFound    

    def get_room(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound        

    def put(self, request, pk, room_pk):#self는 method라서, request는 view라서, pk는 wishlist, room_pk는 room_pk
        wishlist=self.get_list(pk, request.user)
        room=self.get_room(room_pk)
        #room이 wishlist에 있다면 삭제하고 없으면 추가 
        #우선, room이 wishlist에 있는지 확인부터 해야 함.
        #wishlist는 MTM-field인 room필드, 즉 room-list에 room이 있는지 확인이 가능하다.
        #MTM-field여서 all, filter를 가지고 있음

        if wishlist.room.filter(pk=room.pk).exists():#존재 여부만 확인
            wishlist.room.remove(room)
        else:
            wishlist.room.add(room)
        return Response(status=HTTP_200_OK)    




