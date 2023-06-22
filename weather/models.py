from django.db import models
from django.utils import timezone

# Create your models here.

class WeatherHistory(models.Model):

    city_name = models.CharField(max_length=20, null=False, blank=False)
    country = models.CharField(max_length=3, null=False, blank=False)
    weather = models.CharField(max_length=30, null=False, blank=False)
    temp = models.IntegerField()
    temp_feel = models.IntegerField()
    pressure = models.IntegerField()
    sunrise = models.TimeField()
    sunset = models.TimeField()
    unit = models.CharField(max_length=20)
    question_time= models.DateTimeField(auto_now_add=True)

    class Meta():
        ordering = ('-question_time',) # definiuje kolejność sortowania postów na podstawie pola published w porządku malejącym.
    
    def __str__(self):
        return f'{self.city_name} - {self.question_time}'