from django.db import models
from mongoengine import *


# Create your models here.


class MyUser(Document):
    username = StringField(max_length=128, required=True, unique=True)
    password = StringField(max_length=256, required=True)
    content_num = IntField(default=0)

    # def __str__(self):
    #     return '{username:{},content_num:{}}'.format(str(self.username), str(self.content_num))


class Content(Document):
    text = StringField(max_length=500, required=True)
    time = DateTimeField(required=True)
    user = ReferenceField(MyUser)

    # def __str__(self):
    #     return '{text:{},user:{}}'.format(str(self.text), str(self.user))
