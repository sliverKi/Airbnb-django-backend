from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CategorySerializer
from .models import Category
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_204_NO_CONTENT


@api_view(["GET", "POST"])
def categories(request):  # request객체는 URL안에서 호출된 모든 함수에게 주어진다.==api_view
    if request.method == "GET":
        all_categories = Category.objects.all()
        serializer = CategorySerializer(all_categories, many=True)  # translate Category data
        # many=True :: 우리는 CategorySerializer에게 카테고리의 모든 data를 lst형태로 넘김(=all_categories)
        # 근데 CategorySerializer는 번역하는 필드가 name과 kind밖에 없어서 오류가 발생되어짐. 따라서 오류를 해결하기 위해 many=True를 작성함
        return Response(
            serializer.data,
        )
    elif request.method == "POST":
        print(request.data)  # request.data :: user가 보낸 data를 가져다가 쓸 수 있음
        serializer = CategorySerializer(
            data=request.data,
        )  # user가 보낸 data를 serializer에게 넘김
        # CategorySerializer는 user에게서 온 데이터로만 이 serializer를 만든다는 것을 앎
        if serializer.is_valid() == True:
            new_category = serializer.save()
            # serializer.save() :: serializer는 create method를 찾음

            return Response(
                CategorySerializer(new_category).data,
            )  # 보낸data가 유효한지 검사

        else:
            return Response(serializer.errors)


# serializer : Django Python 객체를 JSON으로 번역하는 것
# serializer : user에게 온 data를 받아서 우리의 DB에 넣을 수 있는 Django 객체로 바꿔준다


@api_view(["GET", "PUT", "DELETE"])
def category(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        raise NotFound
    if request.method == "GET":
        serializer = CategorySerializer(category)  # many=True ::설정하지 않아도 되는 이유:: 어차피 하나만 보내고 있기 때문
        return Response(
            serializer.data,  # DB에서 넘어오는 django객체를 번역
        )
    elif request.method == "PUT":
        serializer = CategorySerializer(
            category,
            data=request.data,
            partial=True,  # input data가 완벽한 형태가 아닐수도 있다고 알려줌
            # partial=True => category를 부분적으로 update할 수 있게 함
        )
        if serializer.is_valid():  # data유효성 check
            updated_category = serializer.save()
            return Response(CategorySerializer(updated_category).data)
        else:
            return Response(serializer.errors)
    elif request.method == "DELETE":
        category.delete()
        return Response(status=HTTP_204_NO_CONTENT)
