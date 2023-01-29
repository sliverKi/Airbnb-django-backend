from rest_framework.views import APIView
from .models import Amenity, Room
from .serializers import AmenitySerializer, RoomListSerializer, RoomDetailSerializer
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, NotAuthenticated
from rest_framework.status import HTTP_204_NO_CONTENT


class Amenities(APIView):
    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = AmenitySerializer(all_amenities, many=True)

        return Response(
            serializer.data,
        )

    def post(self, request):
        serializer = AmenitySerializer(data=request.data)  # user-data로 serializer를 만들기 위해서는 유효성 검사를 해야 한다.
        if serializer.is_valid():
            amenity = serializer.save()  # Modelserializer가 자동으로 amenity를 만들게 하고 serializer.save()는 새로 만들어진 amenity를 리턴
            return Response(AmenitySerializer(amenity).data)  # 새로 만들어진 amenity를 번역한후 data화 함
        else:
            return Response(serializer.errors)


class AmenityDetail(APIView):
    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(amenity)
        return Response(
            serializer.data,
        )

    def put(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(
            amenity,  # DB-data
            data=request.data,  # user-data
            partial=True,
        )
        if serializer.is_valid():
            updated_amenity = serializer.save()
            return Response(AmenitySerializer(updated_amenity).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        amenity = self.get_object(pk).delete()
        return Response(status=HTTP_204_NO_CONTENT)


class Rooms(APIView):
    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(all_rooms, many=True)
        return Response(serializer.data)

    def post(self, request):
        print(dir(request))

        if request.user.is_authenticated:
            # request :: 누가 이 URL로 요청하였는지에 관한 정보를 갖고 있다.
            # 이 request를 보내는 유저가 로그인 중인지 아닌지를 확인해야 한다.
            # => 요청 보내는 user를 검증
            serializer = RoomDetailSerializer(data=request.data)
            # serializer는 'data=request.data'이 부분에서 방의 주인에 관한 정보까지 포함하고 있다고 예상한다.
            # => 우리가 방을 생성할 때 오너의 정보도 함께 넘겨주길 원함
            # owner = TinyUserSerializers(),의 형태가 되어야 함.
            """ fields = (
                "name",
                "avatar",
                "username",
            )"""
            # RoomDetailSerializer는 owner, amenities,category를 독립적으로 가지고 있다.(자신만의 형태가 있음)
            # 문제 :: 유저한테 누가 이방의 주인인지 적을 수 있게 허용해서는 안됀다.
            # 권한 허용 안됌. serializer는 방에는 owner가 필요하고 그 owner의 형태를 가져야 한다는 것만 알아.
            # => 우리방에는 여전히 owner가 필요하다, 그러나 우린 방을 생성할때 owner를 보내는 다른 방법으로 정보를 전송해야 할 필요가 있다 .
            # => owner는 request.data로 오지 않을 것 owner field를 read_only라고 설정

            if serializer.is_valid():
                # user-data로만 serializer를 생성해서,
                # save method를 호출 하면 자동으로 create-method를 호출하게 된다.
                room = serializer.save(owner=request.user)
                serializer = RoomDetailSerializer(room)
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            raise NotAuthenticated


class RoomDetail(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomDetailSerializer(room)
        return Response(serializer.data)
