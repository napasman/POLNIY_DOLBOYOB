from django.urls import path
from . import views

app_name = 'charts'
urlpatterns = [
    # URL patterns for the app
    # ...
    path("dashboard/charts/", views.charts, name="charts"),
]
