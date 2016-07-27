from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, TextField


class User(AbstractUser):
    address = TextField(null=False, blank=True, default='')
    cellphone = CharField(null=False, blank=True, default='', max_length=16)

    class Meta:
        unique_together = (('email', ), ('username', ))
