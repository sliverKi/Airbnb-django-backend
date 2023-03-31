from django.db import models
from common.models import CommonModel

# Create your models here.


class Review(CommonModel):
    """Review from a User to a Room or Experience"""

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    # 둘 다 보낸는건 불가능
    # room or experience
    
    
    room = models.ForeignKey(
        "rooms.Room", #room.reviews.all() :: 방을 가리키고 있는 모든 리뷰를 알 수 있다.
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="reviews",
        #related_name을 사용하게 되면, 이 방을 가리키고 있는 모든 리뷰에 접근하는 방법을 명시할 수 있다. 
        #따라서 우리는 방이 rooms.reviews라는 것을 가지고 있다는 말을 할 수 있다.   
    )
    experience = models.ForeignKey(
        "experiences.Experience",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    payload = models.TextField()
    rating = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user} / {self.rating}"
    
