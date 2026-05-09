from django.shortcuts import render

def index(request):
    return render(request, 'wheel_timer/wheel_timer.html')