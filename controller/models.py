from django.db import models

# request count and threshold models
# for this program to work there should be at least one record in the database and 
# the views use the first record (id 1) to keep track of the current count/threshold 

class requestCount(models.Model):
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.count 

class threshold(models.Model):
    threshold = models.IntegerField(default=20)

    def __str__(self):
        return self.threshold

class requestReset(models.Model):
    requestReset = models.IntegerField(default=160)

    def __str__(self):
        return self.requestReset

