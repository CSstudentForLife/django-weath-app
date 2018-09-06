from django.shortcuts import render
from .models import Location
import requests
from .forms import LocationForm
from django.utils import timezone

# Create your views here.

def weather_list(request):
    url = "https://api.openweathermap.org/data/2.5/weather?q={},{}&units=imperial&APPID=d09e9f50bf267db14c26931849969919"
    weathers = Location.objects.filter(time__lte=timezone.now()).order_by("-time")

    notice = "Your weather locations are listed below."

    if request.method == "POST":
        form = LocationForm(request.POST)
        if form.is_valid():
            instance = form.save(commit = False)
            r = requests.get(url.format(instance.city, instance.country)).json()
            if r['cod'] == '404':
                notice = "Sorry, that city could not be found."
                form = LocationForm()
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
