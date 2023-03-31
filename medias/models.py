from django.db import models
from common.models import CommonModel


class Photo(CommonModel):

    file = models.URLField()
    description = models.CharField(
        max_length=150,
    )

    room = models.ForeignKey(#Photo Model은 방을 가리키는 외래키를 사용하고 있다.
        "rooms.Room", #즉 방은 역접근자 또는 related_name을 이용하여 자기를 가리키는 모든 사진을 가져올 수 있다. 
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="medias",
    )
    experience = models.ForeignKey(
        "experiences.Experience",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="medias",
    )

    def __str__(self):
        return "Photo File"


class Video(CommonModel):
    file = models.URLField()
    experience = models.OneToOneField(
        "experiences.Experience",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    # OneToOneField::ForeignKey와 동일 하나 고유한 값을 가지게 됨
    # 하나의 활동은 하나의 동영상만을 가질수 있으며 그 활동은 다른 동영상을 가질 수 없음
    # 1:1 종속관계가 됨 ex) 1 user as one credit info
    def __str__(self):
        return "Video File"
