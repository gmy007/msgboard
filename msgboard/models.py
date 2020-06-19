# -*- coding:utf-8
from django.db import models
from mongoengine import *
import sys


reload(sys)
sys.setdefaultencoding("utf-8")


# Create your models here.


class MyUser(Document):
    username = StringField(max_length=128, required=True, unique=True)
    password = StringField(max_length=256, required=True)
    content_num = IntField(default=0)

    def to_json(self):
        return {'username': str(self.username), 'content_num': str(self.content_num)}


class Content(Document):
    text = StringField(max_length=500, required=True)
    time = DateTimeField(required=True)
    user = ReferenceField(MyUser)

    def to_json(self):
        return {'text': str(self.text), 'user': self.user.to_json(),
                'time': self.time.strftime('%Y年%m月%d日 %H:%M')}
