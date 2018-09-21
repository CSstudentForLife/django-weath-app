from django.shortcuts import render, redirect
from .models import Location
import requests
from .forms import LocationForm, RegistrationForm
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse

# Create your views here.

def user_register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_login')
        else:
            return redirect('user_register')
    else:
        form = RegistrationForm()
        return render(request, 'weatherApp/user_register.html', {'form': form})

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user:
            login(request, user)
            return redirect('weathers')
        else:
            message = "Incorrect username and password combination."
            return render(request, 'weatherApp/login.html', {'message': message})
    else:
        message = "Please enter your username and password."
        return render(request, 'weatherApp/login.html', {'message': message})

def user_logout(request):
    if request.method == "POST":
        logout(request)
        return redirect('user_login')

def weathers(request):
    url = "https://api.openweathermap.org/data/2.5/weather?q={},{}&units=imperial&APPID=d09e9f50bf267db14c26931849969919"

    notice = "Your weather locations are listed below."

    if request.method == "POST":
        form = LocationForm(request.POST)
        if form.is_valid():
            instance = form.save(commit = False)
            r = requests.get(url.format(instance.city, instance.country)).json()
            if r['cod'] == '404':
                notice = "Sorry, that city could not be found."
                form = LocationForm()
                weathers = Location.objects.filter(time__lte=timezone.now()).order_by("-time")
                return render(request, 'weatherApp/weather_list.html', {'form': form, 'notice': notice, 'weathers': weathers})
            else:
                instance.city = instance.city.title()
                instance.country = instance.country.upper()
                instance.temp = r['main']['temp']
                instance.desc = r['weather'][0]['main']
                instance.time = timezone.now()
                instance.icon = r['weather'][0]['icon']
                instance.save()

    weathers = Location.objects.filter(time__lte=timezone.now()).order_by("-time")
    form = LocationForm()
    return render(request, 'weatherApp/weather_list.html', {'form': form, 'notice': notice, 'weathers': weathers})
