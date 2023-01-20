from django.db import models


class CommonModel(models.Model):
    """CommonModel Definition"""

    created_at = models.DateTimeField(
        auto_now_add=True,
    )  # 처음 생성시
    updated_at = models.DateTimeField(
        auto_now=True,
    )  # 업데이트 랗때 마다

    class Meta:  # db에 넣지마
        abstract = True
