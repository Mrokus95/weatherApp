from django.contrib import admin
from .models import WeatherHistory
# Register your models here.

@admin.register(WeatherHistory)
class WeatherHistory(admin.ModelAdmin):
    list_display = ('id','city_name', 'weather', 'temp', 'temp_feel', 'pressure', 'question_time') # Model fields list which should be displayed in admin panel. 
    list_filter = ('city_name','weather') # Filtrs list to filter a data list in admin panel.
    search_fields = ('city_name', 'weather') # List of model fields to be used for searching in the admin panel.
