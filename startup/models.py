from django.db import models

class Starter(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.IntegerField()
    def __str__(self):
        return self.name

class second(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.IntegerField()

    def __str__(self):
        return self.name

class third(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()