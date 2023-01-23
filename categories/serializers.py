from rest_framework import serializers
from .models import Category

# Category를 어떻게 Serialize 할지(번역) 결정
#  Category가 어떻게 API바깥으로 나갈때 표시되는 방법을 정할 수 있다.
# 1, 어떻게 번역할것인지
# 2, 무엇을 번역할것인지 :: 무엇을 보여주고 무엇을 안보여줄지


class CategorySerializer(serializers.Serializer):
    # DB에 있는 객체들은 모두 PK를 가지고 있다.
    # pk를 이용하여 커스터 마이징을 할 수도 있다.

    pk = serializers.IntegerField(read_only=True)
    # serialize에게 카테고리 필드 설명
    name = serializers.CharField(
        required=True,
        max_length=50,
    )
    kind = serializers.ChoiceField(
        choices=Category.CategoryKindChoices.choices,
    )
    # serialize에게 name과 kind가 JSON으로 어떻게 표현하는지 설명함.
    created_at = serializers.DateTimeField(read_only=True)
    # 각 모델이 갖고 있는 필드를 이용하여 customizing을 할 수 있음.
    # 단점:: 만약 해당 모델이 많은 필드를 갖고 있는 경우 다 하나하나 복사하여 serializer에게 알려줘야함.
    # serializer와 - pk, name, kind, created_at를 공유
    # => user에게서 넘어오는 data를 검증하는 걸 도와줄 수 있다.
    # ex :max_length=50,  :: 50미만이 경우 유효한 데이터가 아니라고 에러 메세지 발생시킴(검증)
    # read_only=True :: serializer에게어떤건 보내고 어떤건 보내지 않는지 설정할떄 사용
    def create(self, validate_data):
        return Category.objects.create(**validate_data)
        # ** 역할 :: dict를 가져와, {'name':'Category from DRF', 'kind':'rooms'}의 dictionary를
        # name='Category from DRF',
        # kind='rooms'로 바꿔줌 Line 35-36은 create가 필요한것
        # name=validate_data['name'],
        # kind=validate_data['kind'],

        # return super().create(validate_data)#create는 객체를 반환해야 한다.

    # if requested.data로만 생성한 serializer에서 save메서드를 호출하면
    # 그때가 바로 serializer가 create method를 호출하는 순간이다.

    def update(self, instance, validate_data):  # instance :: 너가 update하려는 model / validate_data :: user-data
        instance.name = validate_data.get("name", instance.name)  # update-Method는 validate_date에서 사용자 데이터를 가져오고,
        instance.kind = validate_data.get("kind", instance.kind)  # 만약에 거기에 데이터가 없으면 DB에 있는 기본값(instance)을 사용함.
        instance.save()
        return instance
        # update method :: 다른 곳에서 save method를 실행한 경우에 호출 되어짐
        # instance::db에서 가져온 data
