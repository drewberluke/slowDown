from django.db import models

# Create your models here.

class requestCount(models.Model):
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.count 

class threshold(models.Model):
    threshold = models.IntegerField(default=20)

    def __str__(self):
        return self.threshold