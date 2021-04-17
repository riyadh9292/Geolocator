from .views import calculate_distance_view
from django.urls import path,include

urlpatterns = [
    path('',calculate_distance_view,name='home')
]
