from django.db import models
# from django.conf import settings


class BaseModel(models.Model):
    creation_date = models.DateTimeField(
        auto_now_add=True,
    )
    update_date = models.DateTimeField(
        auto_now=True,
    )
    
    estate = models.CharField(
        max_length=1,
        default='A',
    )

    class Meta:
        abstract = True
