from django.shortcuts import render
from django.http import HttpResponse
from .models import Room


def see_all_rooms(request):
    rooms = Room.objects.all()
    # DB에서 모든 정보를 가져옴
    return render(  # rooms의 모든 data를 all_rooms.html로 보냄
        request,
        "all_rooms.html",
        {
            "rooms": rooms,  # 보내는 data들
            "title": "Hello! this title comes from django!",
        },
    )

    # return HttpResponse("see all rooms")


def see_one_room(request, room_pk):
    try:
        room = Room.objects.get(pk=room_pk)
        return render(
            request,
            "room_detail.html",
            {
                "room": room,
            },
        )
    except Room.DoesNotExist:
        return render(
            request,
            "room_detail.html",
            {
                "not_found": True,
            },
        )
