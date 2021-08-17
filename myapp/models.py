import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    money = models.IntegerField(default=10000)


class Note(models.Model):
    title = models.CharField(max_length=100, default='name')
    text = models.CharField(max_length=100)
    instock = models.IntegerField(default=5)
    price = models.IntegerField(default=100)
    created_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')

    class Meta:
        ordering = ['-created_at', ]


class Buy(models.Model):
    buy = models.ForeignKey(Note, on_delete=models.DO_NOTHING, related_name='cus', default=False)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='tovar', default=False)
    quantity = models.IntegerField(default=1)
    timeOfBuy = models.DateTimeField(auto_now=True)
    canReturn=models.BooleanField(default=True)


class ReturnBuy(models.Model):
    returnBuy=models.ForeignKey(Buy,on_delete=models.DO_NOTHING,related_name='returnTovar',default=False)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='USERRRR', default=False)
    timeOfReturn=models.DateTimeField(auto_now=True)

