from django.db import models
from mongoengine import *


# Create your models here.

class MyUser(Document):
    username = StringField(max_length=120, required=True, unique=True)
    password = StringField(max_length=200, required=True)
