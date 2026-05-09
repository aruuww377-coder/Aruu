from django.urls import path
from . import views  # <--- Make sure this has an 's'

urlpatterns = [
    path('', views.index, name='wheel_timer_home'),
]