from django.db import models

# Create your models here.

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from rest_framework.authtoken.models import Token


class Todo(models.Model):
    title = models.CharField(max_length=300)
    completed = models.BooleanField(null=True, default=None)
    url = models.URLField(null=True, default=None)
    order = models.IntegerField(null=True, default=None)

    def __str__(self):
        return self.title


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_token(sender, instance=None, created=False, **kwags):
    if created:
        Token.objects.create(user=instance)