from django.db import models
# from django.conf import settings


class BaseModel(models.Model):
    creation_date = models.DateTimeField(
        auto_now_add=True,
    )
    update_date = models.DateTimeField(
        auto_now=True,
    )
    # creation_user = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     on_delete=models.CASCADE,
    #     null=True,
    #     blank=True,
    #     related_name='%(class)s_creation',
    # )
    # update_user = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     on_delete=models.CASCADE,
    #     null=True,
    #     blank=True,
    #     related_name='%(class)s_update',
    # )
    estate = models.CharField(
        max_length=1,
        default='A',
    )

    class Meta:
        abstract = True