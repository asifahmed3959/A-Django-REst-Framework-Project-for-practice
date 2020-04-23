from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from django.contrib.postgres.fields import JSONField

import uuid
import string
import nanoid
import datetime


class User(AbstractUser):
    first_name = models.CharField(_('first name'), max_length=30, blank=False)
    last_name = models.CharField(_('last name'), max_length=150, blank=False)
    email = models.EmailField(_('email address'), blank=False, unique=True)


class UserAuthInfo(models.Model):
    access_token = models.CharField(max_length=48, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_token')


# class APISecret(models.Model):
#     public_key = models.CharField(max_length=18, unique=True)
#     secret_key = models.CharField(max_length=18, unique=True)
#     generated_at = models.DateTimeField()
#     user = models.OneToOneField('base.User', on_delete=models.CASCADE, related_name='apisecret')
#     scopes = JSONField(null=True, blank=True)
#
#     def gen_key(self):
#         api_char_choices = string.ascii_letters + string.digits + "-_"
#
#         self.public_key = "pk_" + nanoid.generate(api_char_choices, size=15)
#         self.public_key = "sk_" +nanoid.generate(api_char_choices, size=15)
#         self.generated_at = datetime.datetime.utcnow()


class Quote(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    author = models.ForeignKey(User, related_name='quotes', on_delete=models.CASCADE)
    quote = models.CharField(max_length=128, blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    signed = models.ManyToManyField(User, related_name='approved_by', through='ApprovedMembers',through_fields=('quote','user') ,blank=True)
    created_by = models.ForeignKey(User, related_name='created_by', on_delete=models.DO_NOTHING, null=True, blank=True)
    updated_by = models.ForeignKey(User, related_name='updated_by', on_delete=models.DO_NOTHING, null=True,blank=True)


class Publication(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=128, blank=False)
    quote = models.ForeignKey(Quote, related_name='publications', on_delete=models.CASCADE)
    date = models.DateField(blank=False, null=False)


class ApprovedMembers(models.Model):
    quote = models.ForeignKey(Quote, related_name='approved_quote', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='approved_members', on_delete=models.CASCADE)
    underground_name = models.CharField(max_length=128)
    rank = models.IntegerField()