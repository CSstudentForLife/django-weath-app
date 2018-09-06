from django import forms
from .models import Location

class LocationForm(forms.ModelForm):
    city = forms.CharField(label = "City Name", max_length = 30,
                            widget=forms.TextInput(attrs={'placeholder': ' i.e. (New York, London, Boston)', 'class': 'myfieldclass'}))
    country = forms.CharField(label = "Country Code:", max_length = 10,
                            widget=forms.TextInput(attrs={'placeholder': ' i.e. (US, UK, RU)', 'class': 'myfieldclass'}))

    class Meta:
        model = Location
        fields = ('city', 'country')
