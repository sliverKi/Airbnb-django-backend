from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):  # AbstractUser를 상속받음
    class GenderChoices(models.TextChoices):
        MALE = ("male", "MALE")  # (VALUE(=DB inside), LABEL(= see in admin page))
        FEMALE = ("female", "FEMALE")

    class LanguageChoices(models.TextChoices):
        KR = ("kr", "Korean")
        EN = ("en", "English")

    class CurrencyChoices(models.TextChoices):
        WON = "won", "Korean Won"
        USD = "usd", "Dollar"

    first_name = models.CharField(
        max_length=150,
        editable=False,
    )
    last_name = models.CharField(
        max_length=150,
        editable=False,
    )
    name = models.CharField(
        max_length=150,
        default="",
    )
    is_host = models.BooleanField(
        default=False,
    )
    avatar = models.URLField(
        null=True,
        blank=True,
    )
    # blank=True :: form에서 해당 항목이 필수가 아니게 됨~> form 에서 field를 비워둘 수 있어
    # null=True :: DataField에서 필드가 NULL값을 가질 수 있게 해 줌
    gender = models.CharField(
        max_length=10,
        choices=GenderChoices.choices,
    )
    language = models.CharField(
        max_length=2,
        choices=LanguageChoices.choices,
    )
    currency = models.CharField(
        max_length=5,
        choices=CurrencyChoices.choices,
    )
    # null=True :: 장고는 is_host칼럼에 아무런 값을 넣지 않으면서 추가가 가능
    # default=False : 이전에 생성된 모든 사용자는 is_host의 값을 False로 가짐

    # name, is_host field는 null값을 가질 수 없음.
    # name, is_host field is non-nullable field
    # BooleanField, and Charfield also cannot be null
            