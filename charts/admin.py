from django.contrib import admin
from .models import WordChart


@admin.register(WordChart)
class WordChartAdmin(admin.ModelAdmin):
    pass