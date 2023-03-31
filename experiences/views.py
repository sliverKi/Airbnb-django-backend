from django.shortcuts import render
from django.conf import settings
from django.utils import timezone
from django.db import transaction

from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT,HTTP_400_BAD_REQUEST
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated


from .models import Experience, Perk
from .serializers import ExperienceSerializer, ExperienceDetailSerializer, PerkSerializer

from bookings.models import Booking
from bookings.serializers import PublicBookingSerializer, CreateExperienceBookingSerializer

class Experiences(APIView):
    
    permission_classes=[IsAuthenticatedOrReadOnly] #인가된 사용자
    
    def get(self, request):#조회
        all_experiences = Experience.objects.all()
        serializer = ExperienceSerializer(
            all_experiences,
            many=True,
        )
        return Response(serializer.data)


    def post(self, request):#생성
        serializer = ExperienceDetailSerializer(data=request.data)
        
        if serializer.is_valid():
            with transaction.atomic():
#price                
                price = request.data.get("price")
                if price:
                    if price<0:
                        raise ParseError("Price must be PositiveInteger")
#category            
                category_pk=request.data.get("category")
                if not category_pk:
                    raise ParseError("Category must be required")
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind==Category.CategoryKindChoices.ROOMS:
                        raise ParseError("The category kind should be Experiences")
                except Category.DoesNotExist:
                    raise ParseError("Category does not found in Category-Kind-Choices")
                
                experience = serializer.save(
                    host=request.user,
                    category=category,
                )
#perk                
                perks_pk=request.data.get("perks")
                if not perk_pk:
                    raise ParseError("Perk must be required")     
                try:
                    for perk_pk in perks:
                        perk = Perk.objects.get(pk=perk_pk)
                        experience.perks.add(perk)
                except Perk.DoesNotExist:
                    raise ParseError("Perk does not found")

                serializer=ExperienceSerializer(experience)
                return Response(serializer.data) 
        else:
            return Response(serializer.errors)   

class ExperienceDetail(APIView):

    permission_classes=[IsAuthenticatedOrReadOnly]
    
    
    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise Notfound

    def get(self, request, pk):
        experience=self.get_object(pk)
        serializer = ExperienceSerializer(experience)
        return Response(serializer.data)
    
    def put(self, request, pk):
        experience=self.get_object(pk)
        
        if experience.host!=request.user:
            raise PermissionDenied 
        serializer=ExperienceDetailSerializer(
            experience,  
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            with transaction.atomic():
                
            #category error check
                if category_pk:
                    try:
                        category=Category.objects.get(pk=category_pk)
                        if category.kind==Category.CategoryKindChoices.ROOMS:
                            raise ParseError("The category kind should be EXPERIENCES")
                        room.category=category
                    except Category.DoesNotExist:
                        raise ParseError("Category does not found in Category-Kind-Choices")
            
            #perk error check
                perks_pk=request.data.get("perks")
                if perks_pk:
                    if not isinstance(perks_pk, list):
                        raise ParseError("Invalid perks_pk")
                    experience.perks.clear()
                    for pk in perks_pk:
                        try:
                            perk = Perk.objects.get(pk=pk)
                            experience.perks.add(perk)
                        except Perk.DoesNotExist:
                            raise ParseError("Invalid Perk pk")
                updated_experience=serializer.save()
            return Response(ExperienceSerializer(updated_experience).data)
        else:
            return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        experience = self.get_object(pk)

        if experience.host!=request.user:
            raise PermissionDenied
        experience.delete()
        return Response(status=HTTP_204_NO_CONTENT)            


class ExperiencePerk(APIView):
    
    permission_classes=[IsAuthenticatedOrReadOnly]#비인가자에게 get만 허용, 나머진 불허

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotFound:
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

        experience=self.get_object(pk)
        serializer=PerkSerializer(
            experience.perks.all()[start:end],
            many=True,
        )
        return Response(serializer.data) 
           

class ExperienceBook(APIView):
    permission_classes=[IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except:
            raise NotFound

    def get(self, request, pk):
        experience=self.get_object(pk)
        now=timezone.localtime(timezone.now()).date()
        
        bookings=Booking.objects.filter(
            experience=experience,
            kind=Booking.BookingKindChoices.EXPERIENCE,
            experience_time__gte=now,
        )
        serializer=PublicBookingSerializer(
            bookings, 
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        experience = self.get_object(pk)
        serializer= CreateExperienceBookingSerializer(data=request.data)

        if serializer.is_valid():
            booking=serializer.save(
                experience=experience,
                user=request.user,
                kind=Booking.BookingKindChoices.EXPERIENCE,
            )
            serializer=PublicBookingSerializer(booking)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class ExperienceBookDetail(APIView):
    permission_classes=[IsAuthenticatedOrReadOnly]

    def get_experience(self,pk):
        try: Experience.objects.get(pk=pk)
        except Experience.DoesNotFound: 
            raise NotFound
    
    def get_book(self,pk):
        try: Booking.objects.get(pk=pk)
        except Booking.DoesNotFound: 
            raise NotFound

    def get(self, request, pk, book_pk):
        book=self.get_object(book_pk)
        if book.experience ==self.get_experience(pk):
            return Response(PublicBookingSerializer(book).data)
        else:
            raise ParseError("No data") 
               
    def put(self, request, pk, book_pk):

        book=self.get_book(book_pk)
        
        serializer =CreateExperienceBookingSerializer(
            book,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            book=serializer.save()
            serializer=PublicBookingSerializer(book)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)    

    def delete(self, request, pk, book_pk):

        book=self.get_book(book_pk)
        if book.user.pk!=request.user.pk:
            raise PermissionDenied
        book.delete()
        return Response(status=HTTP_204_NO_CONTENT)    

class Perks(APIView):
    def get(self, request):
        all_perks = Perk.objects.all()
        serializer = PerkSerializer(all_perks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PerkSerializer(data=request.data)
        if serializer.is_valid():
            perk = serializer.save()
            return Response(PerkSerializer(perk).data)
        else:
            return Response(serializer.errors)


class PerkDetail(APIView):
    def get_object(self, pk):
        try:
            return Perk.objects.get(pk=pk)
        except Perk.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        perk = self.get_object(pk)
        serializer = PerkSerializer(perk)
        return Response(serializer.data)

    def put(self, request, pk):
        perk = self.get_object(pk)
        serializer = PerkSerializer(
            perk,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_perk = serializer.save()
            return Response(
                PerkSerializer(updated_perk).data,
            )
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        perk = self.objects.get(pk).delete()
        return Response(status=HTTP_204_NO_CONTENT)
