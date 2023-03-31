from django.conf import settings
from django.db import transaction
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, NotAuthenticated, ParseError, PermissionDenied
from rest_framework.status import HTTP_204_NO_CONTENT,  HTTP_400_BAD_REQUEST
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Amenity, Room
from .serializers import AmenitySerializer, RoomListSerializer, RoomDetailSerializer
from categories.models import Category
from reviews.serializers import ReviewSerializer 
from medias.serializers import PhotoSerializer
from users.serializers import TinyUserSerializers
from bookings.models import Booking 
from bookings.serializers import PublicBookingSerializer, CreateRoomBookingSerializer
#transaction:: code조각중 하나라도 실패 한 경우, 그 시점에 db에서 변경된 사항들이 모두 되돌려 지게 할 수 있다. 

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
        
        if serializer.is_valid():
            updated_amenity = serializer.save()
            return Response(AmenitySerializer(updated_amenity).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        amenity = self.get_object(pk).delete()
        return Response(status=HTTP_204_NO_CONTENT)


class Rooms(APIView):
    permission_classes =[IsAuthenticatedOrReadOnly]

    #IsAuthenticatedOrReadOnly :: 
    #1. user가 인증을 받았는지 확인 
    #2. SAFE_METHODS라고 불리는 것 안에 요청 메서드가 존재하는지 확인 
    #SAFE_METHODS ~> GET, HEAD,OPTION을 가지는데 이것 들은 모두 읽기 전용 메서드 임.
    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(
            all_rooms, 
            many=True,
            context={"request":request}, #모든 방을 get할때, context를 보내어 
        )  #RoomListSerializer에서 context에 접근 할 수 있게 만듬.
        return Response(serializer.data)

    def post(self, request):
        
        #if request.user.is_authenticated:
            # request :: 누가 이 URL로 요청하였는지에 관한 정보를 갖고 있다.
            # 이 request를 보내는 유저가 로그인 중인지 아닌지를 확인해야 한다.
        # => 요청 보내는 user를 검증
        serializer = RoomDetailSerializer(data=request.data)
        # serializer는 'data=request.data'이 부분에서 방의 주인에 관한 정보까지 포함하고 있다고 예상한다.
        # => 우리가 방을 생성할 때 오너의 정보도 함께 넘겨주길 원함
        # owner = TinyUserSerializers(),의 형태가 되어야 함.
        # RoomDetailSerializer는 owner, amenities,category를 독립적으로 가지고 있다.(자신만의 형태가 있음)
        # 문제 :: 유저한테 누가 이방의 주인인지 적을 수 있게 허용해서는 안됀다.
        # 권한 허용 안됌. serializer는 방에는 owner가 필요하고 그 owner의 형태를 가져야 한다는 것만 알아.
        # => 우리방에는 여전히 owner가 필요하다, 그러나 우린 방을 생성할때 owner를 보내는 다른 방법으로 정보를 전송해야 할 필요가 있다 .
        # => owner는 request.data로 오지 않을 것 owner field를 read_only라고 설정

        if serializer.is_valid():
            # user-data로만 serializer를 생성해서,
            # save method를 호출 하면 자동으로 create-method를 호출하게 된다.
            category_pk=request.data.get("category")#user-data로 부터 category를 받아옴
            if not category_pk:#category 없이 방을 만들수 없게 함 
                return ParseError("Category is required")#400 Bad request ~> 유저가 잘못된 data(ex.공란)를 전송함 
            #ParseError :: User가 잘못된 data를 갖고 있는 경우 발생
            try:
                category = Category.objects.get(pk=category_pk) #만약 카테고리 변수가 있다면 category변수를 덮어씌움   
                if category.kind==Category.CategoryKindChoices.EXPERIENCES:#카테고리 선택지에서 찾아
                    raise ParseError("The category kind should be rooms")
            except Category.DoesNotExist:#유저가 선택지에 존재하지 않는 카테고리를 넘겨준 경우 
                raise ParseError("Category does not found in Category-Kind-Choices")
            try:
                with transaction.atomic():#transaction > room-amenity의 try-except를 할 필요가 없어짐.
                        #try: Amenity.objects.get(pk=amenity_pk)    
                        #except Amenity.DoesNotExist: #만약 찾지 못했다면 에러 발생 
                        #pass ::: #~> if). 다른 필드는 맞게 기입했는데 , amenity-field만 잘못 기입했다면 >> 그냥 pass(신경쓰지 않고 계속 진행 )
                        #room.delete() #~> if).2. 그 방을 삭제하고 에러메시지 띄움<<좋은 방법 아님 :: 생성했다 지웠다를 많이 반복해야 됌  > id 낭비 심함 == Transaction : 
                        #id 낭비라는 말은 곧 우리가 맣은 쿼리들을 생성하고 모두 성공하거나, 모두 실패하게 할 수 있다.
                        #방을 생성하는 건 잘 작동하고 있는데 amenity를 추가할때, amenity가 존재하지 않는다면, 딱 그 쿼리만 실패하게 되어 있다. 즉 우리는 수동으로 방을 삭제 해야만 한다.
                        #위 line(109)모두 성공해야만 하는 코드의 세트를 만드는 것!, 그리고 만약 성공하지 못했다면 전체 코드와 변화들이 되돌려 지는 것(== Transaction)
                        #모든 코드가 성공하거나 아무것도 성공하지 않기를 원할때 트랜잭션을 사용한다.
                        #장고엣는 기본적으로 모든 쿼리는 즉시 DB에 저장됨 ==개별의 쿼리가 DB를 수정한다..
                        #하지만 트랜잭션을 사용하게 되면 많은 쿼리와 create-Method를 정의한 다음 이중 하나라도 실패한 다면 모든 쿼리가 실패 즉, 모든 쿼리가 되돌려 지게 됨.(모든 변경사항이 원래 상태대로 되돌아감 )
                        #방을 생성하고 삭제 하기 보다 필드를 하나라도 잘 못 기입한 경우, 애초에 방을 생성하지 않음
                    room = serializer.save(#serializer.save는 생성된 방을 결과물로 돌려줌
                        owner=request.user, 
                        category = category,
                    )
                    amenities=request.data.get("amenities")
                    for amenity_pk in amenities: #amenity-field의 PK를 보면서 각 amenity가 존재하는지 알아봄 
                        amenity = Amenity.objects.get(pk=amenity_pk)#개별 amenity를 찾아
                        room.amenities.add(amenity)#만약 각 방이 존재하다면 방에 amenity를 추가하여 준다.
                    #user-data로 생성된 serializer가 save메서드를 호출하면 자동으로 create()를 호출함
                    #나의 create-Method에 validated_data에 추가됨. 
                    serializer = RoomDetailSerializer(room)
                    #user가 보낸 모든 amenity를 확인한 다음에, 그게 존재하든 않든 유저에게 데이터를 반환  
                    return Response(serializer.data)
                #transaction.atomic()이 없을땐 코드가 실행될때 마다 쿼리가 DB에 즉시 반영,
                #코드를 transaction.atomic()안에 넣는다면..? 장고는 DB에 transaction.atomic()안에 있는 코드를 즉시 반영 하지 않음
                #대신 장고는 나의 코드가 어떻게 작동 되어 지는 지를 보고 살펴본 다음, 
                #변경사항들을 리스트로 만들어서 계속해서 코드를 살펴본 다음에 내가 수정하고 싶은 부분들을 기억함.
                #만약 여기서 에러가 발생하지 않는다면 장고는 이때 DB에 push 
                #에러가 하나라도 발생된다면 장고는 DB에 반영하지 않음 >> try-except를 삭제한 이유 
                # try-except를 삭제한 이유::transaction은 에러가 난 사실을 알지 못함
                #따라서 try-except로 transaction.atomic()을 감쌈
            except Exception:
                raise ParseError("Amenity not Found")
        else:
            return Response(serializer.errors)
        #else:
        #    raise NotAuthenticated

class RoomDetail(APIView):
    
    permission_classes=[IsAuthenticatedOrReadOnly]
    
    def is_negative(self,num,temp):
        if num: #있는지 확인
            if num<0: #음수 인지  
                raise ParseError(f"{temp} must be Positive") #음수면 에러       

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomDetailSerializer(#request객체를 serializer에 전달
            room,
            context={"request": request},#RoomDetailSerializer는 
            #새로운 SerializerMethodField의 값을 계산 할수 있게 됨 
        )
        #context :: 내가 serializer에 외부세계에 대한 정보를 보낼때 유용함, 
        # 내가 원하는 메소드 어떤 것이든 serializer의  context에 접근 할 수 있다.
        return Response(serializer.data)

    def put(self, request,pk):
        
        room=self.get_object(pk)
        
        if room.owner!=request.user:
            raise PermissionDenied        
        
        serializer=RoomDetailSerializer(
            room,  # user-data
            data=request.data,
            partial=True,
        )
        
        #check, Is data-value positive?
        if serializer.is_valid():  # 모든 data유효성 check
            with transaction.atomic():
                price=request.data.get("price")
                self.is_negative(price, "price")
                rooms=request.data.get("rooms")
                self.is_negative(rooms,"rooms")
                toilets=request.data.get("toilets")
                self.is_negative(toilets, "toilets")
                
        #check, Category errors
                category_pk=request.data.get("category")
                if category_pk:
                    try:
                        category=Category.objects.get(pk=category_pk)
                        if category.kind==Category.CategoryKindChoices.EXPERIENCES:
                            raise ParseError("The category kind should be rooms")
                        room.category=category
                    except Category.DoesNotExist:
                        raise ParseError("Category does not found in Category-Kind-Choices")    
        #check, Amenity errors
                amenities=request.data.get("amenities")
                if amenities:
                    if not isinstance(amenities, list):
                        raise ParseError("Invalid amenities")
                    rooms.amenities.clear()
                    for amenity_pk in amenities: #amenity-field의 PK를 보면서 각 amenity가 존재하는지 알아봄 
                        try:
                            amenity = Amenity.objects.get(pk=amenity_pk)#개별 amenity를 찾아
                            room.amenities.add(amenity)
                        except Amenity.DoesNotExist:
                            raise ParseError("Amenity not Found")
                updated_room = serializer.save()
            return Response(RoomDetailSerializer(updated_room).data)
        else:
            #return Response(serializer.errors)
            return Response(status=HTTP_BAD_REQUEST)

    def delete(self, request, pk):#self: class의 Method라서 / request: views의 함수라 장고에 의해 자동으로 request를 받음/ url에서 pk라는 값을 전달받고 있기 때문   
       
        room=self.get_object(pk)
       
        if room.owner!=request.user:
            raise PermissionDenied
        room.delete()
        return Response(status=HTTP_204_NO_CONTENT)    


class RoomReviews(APIView):
    
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_object(self, pk):
        try: 
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request,pk):
        try:
            page=request.query_params.get("page", 1)#URL에서 PAGE를 가져오는데, 만약 PAGE가 URL에 있지 않다면 기본적으로 PAGE는 1로 지정 
        #+)모든 딕셔너리의 get메서드는 기본값을 지정할 수 있게 해줌     
            page=int(page)#url의 page=값을 받아옴, 그러나 page의 type이 str형태이고 int로 강제 형변환,  
        
        except ValueError:#if ) page=jsdjhsdk이런 형태라면 valueerror가 발생
            page=1 
            # 따라서 URL에 페이지가 없거나 유저가 잘못된 페이지를 보내는 상황이라고 하더라도 여전히 페이지는 1이 됨  
        page_size=settings.PAGE_SIZE
        start=(page-1)*page_size
        end=start+page_size

        room=self.get_object(pk)
        serializer=ReviewSerializer(
            room.reviews.all()[start:end], 
            many=True,
        )
        return Response(serializer.data)
    def post(self, request, pk):
        serializer=ReviewSerializer(data=request.data)
        
        if serializer.is_valid():#serializer가 유효하다면, 
            
            review=serializer.save(#review는 유저도 필요하고, 방도 필요하다
                user=request.user,
                room=self.get_object(pk)    
            )#리턴 값을 review에 대입 하여 저장 
            
            serializer=ReviewSerializer(review)
            return Response(serializer.data)

class RoomAmenities(APIView):
    def get_object(self, pk):
        try: 
            return Room.objects.get(pk=pk)
        except Room.DoesNotFound:
            raise NotFound 

    def get(self, request, pk):
        try:
            page=request.query_params.get("page",1)      
            page=int(page)
        except ValueError:
            page=1 

        page_size=settings.PAGE_SIZE
        start=(page-1)*page_size 
        end=start+page_size   

        room=self.get_object(pk)#각 방의 id를 받음 
        serializer=AmenitySerializer(
            room.amenities.all()[start:end], #방에 대한 aenitites
            many=True,
        )
        return Response(serializer.data)

class RoomPhotos(APIView):

    permission_classes=[IsAuthenticatedOrReadOnly]
    # :: 아래주석과 동일 기능, code-ReFactor
    #if not request.user.is_authenticated:
            #raise NotAuthenticated 
        
    
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotFound:
            raise NotFound 

    def post(self, request, pk):
        room=self.get_object(pk)
        if request.user != room.owner:
            raise PermissionDenied   

        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            photo=serializer.save(room=room)
            #사진이 속한 방도 보내야 함 
            serializer = PhotoSerializer(photo)#photo:: 번역 대상 
            return Response(serializer.data)
        else:
            return Response(serializer.errors)    

class RoomBookings(APIView):
    permission_classes=[IsAuthenticatedOrReadOnly]
    #인가된 사용자만 예약 가능하게 하고,  룸 예약 여부를 보여줌  


    """ 모든 사용자에가 get(조회) method를 이용할 수 있지만, 인가된 사용자만 put(수정), post(생성, 등록), delete method를 이용할 수 있다."""
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except:
            raise NotFound 

    def get(self, request, pk):
        room=self.get_object(pk)
        now=timezone.localtime(timezone.now()).date() #now 한국 기준의 로컬 타임이고 date()를 해주면 datetime중에 date만 반환
        
        bookings=Booking.objects.filter(
            room=room, 
            kind=Booking.BookingKindChoices.ROOM,
            check_in__gt=now,#다가올 예약만 보여줌
        )
        serializers=PublicBookingSerializer(bookings, many=True)

        return Response(serializers.data)

    def post(self, request, pk): #post(생성, 등록)
        room=self.get_object(pk)
        serializer=CreateRoomBookingSerializer(data=request.data) #1. PublicBookingSerializer가 data를 검증함. -> 2.CreateRoomBookingSerializer으로 교체 :: post는 data 생성 method
        #~> 1.근데 fields를 보면 guests만 필수 사항이고 그외는 선택,
        # 1.유저는 guests-field만 있는 data를 보내도 serializer는 data is valid라고 생각하게됨 => room booking만을 위한 CreateRoomBookingSerializer 생성 
        
        
        if serializer.is_valid(): #여기서는 형식이 옳은지, 값이 들어오는지만 확인함    
            #미래의 date로 만 check_in해야하는 것을 serializer는 모르기 때문에 추가 작업을 해줘야 함
            #if user가 보낸 data가 미래 날짜가 아닌 경우에는 false를 반환 ~> validation을 custom화 
            booking=serializer.save(
                room=room,
                user=request.user,
                kind=Booking.BookingKindChoices.ROOM,
            )
            serializer=PublicBookingSerializer(booking)
            return Response(serializer.data)      
        else:
            return Response(serializer.errors)    