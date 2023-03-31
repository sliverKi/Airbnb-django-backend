from rest_framework.views import APIView
from .models import Photo
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.permissions import IsAuthenticated 
class PhotoDetail(APIView):
    
    permission_classes=[IsAuthenticated]
    def get_object(self,pk):
        try:
            return Photo.objects.get(pk=pk)
             
        except Photo.DoesNotFound:
            raise NotFound

    def delete(self, request, pk):
        photo=self.get_object(pk)
        
       
       #사진은 두 가지의 타입을 가질수 있다. 1.방 사진 2. 경험(일상)사진 
       #~> 따라서 일단 두가지의 경우를 나누어 생각 
       #~> 우선 사진이 있는지, 그리고 그 사진이 유저 or 호스트와 동일한 지 확인
       #~> 사진>방>주인 == 요청의 유저  / 사진 > 경험 > 호스트  
        if (photo.room and photo.room.owner!=request.user) or (photo.experience and photo.experience.host!=request.user): 
            raise PermissionDenied
        photo.delete()
        return Response(status=HTTP_200_OK)
