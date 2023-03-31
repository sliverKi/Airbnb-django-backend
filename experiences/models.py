from django.db import models
from common.models import CommonModel
from categories.models import Category

# Create your models here.
class Experience(CommonModel):
    """Experience Model Definition"""

    country = models.CharField(
        max_length=50,
        default="South Korea",
    )
    city = models.CharField(
        max_length=80,
        default="Seoul",
    )
    name = models.CharField(
        max_length=250,
    )
    host = models.ForeignKey(  # experiences_model pointing to User model
        "users.User",  # User model은 experience_Model로 부터 자동으로 experience_set을 받게 됨
        on_delete=models.CASCADE,
        related_name="experiences",#related_name을 사용하게 되면, 모든 리뷰에 접근하는 방법을 명시할 수 있다.
    )
    price = models.PositiveIntegerField()
    address = models.CharField(
        max_length=250,
    )
    start = models.TimeField()
    end = models.TimeField()
    description = models.TextField()
    perks = models.ManyToManyField(
        "experiences.Perk",
    )
    category = models.ForeignKey(
        "categories.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="experiences",
    )
    # if) on_delete=models.CASCADE이면 카테고리가 삭제되면
    # ExperienceModel도 같이 삭제 됨
    # if)on_delete=models.SET_NULL 이면 experience-host가 계정을 삭제하면
    # experiences가 삭제됨

    def __str__(self):
        return self.name


class Perk(CommonModel):

    """Perk Model Definition"""

    name = models.CharField(
        max_length=100,
    )
    detail = models.CharField(
        max_length=250,
        blank=True,
        default="",
        # null=True,
    )
    explanation = models.TextField(
        blank=True,
        default="",
    )
    # blank=True :: form에서 해당 항목이 필수가 아니게 됨~> form 에서 field를 비워둘 수 있어
    # null=True :: DataField에서 필드가 NULL값을 가질 수 있게 해 줌
    def __str__(self):
        return self.name
