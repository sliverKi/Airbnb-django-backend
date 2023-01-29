from django.db import models
from common.models import CommonModel


class Category(CommonModel):
    """Room Experience Category"""

    class CategoryKindChoices(models.TextChoices):
        ROOMS = "rooms", "ROOMS"
        EXPERIENCES = "experiences", "Experiences"

    name = models.CharField(max_length=50)
    kind = models.CharField(
        max_length=15,
        choices=CategoryKindChoices.choices,
        # kind에 choices가 있어 선택지가 있다고 알림.
    )

    def __str__(self):
        return f"{self.kind.title()}:{self.name}"

    # self.kind :: experience(lowercase)
    # self.kind.title() :: Experience(uppercase)
    class Meta:
        verbose_name_plural = "Categories"
