from django.contrib import admin
from .models import WeatherHistory
# Register your models here.

@admin.register(WeatherHistory)
class WeatherHistory(admin.ModelAdmin):
    list_display = ('id','city_name', 'weather', 'temp', 'temp_feel', 'pressure', 'question_time') # Lista pól modelu, które mają być wyświetlane w widoku listy w panelu administracyjnym.
    list_filter = ('city_name','weather') # filtry do filtrowania listy w panelu administracyjnym
    search_fields = ('city_name', 'weather') # Lista pól modelu, które mają być używane do wyszukiwania w panelu administracyjnym
