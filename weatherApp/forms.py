from django import forms
from .models import Location
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class LocationForm(forms.ModelForm):
    city = forms.CharField(label = "City Name", max_length = 30,
                            widget=forms.TextInput(attrs={'placeholder': ' i.e. (New York, London, Boston)', 'class': 'myfieldclass'}))
    country = forms.CharField(label = "Country Code:", max_length = 10,
                            widget=forms.TextInput(attrs={'placeholder': ' i.e. (US, UK, RU)', 'class': 'myfieldclass'}))

    class Meta:
        model = Location
        fields = ('city', 'country')

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(required = True,
                                help_text = "Please enter your first name.",
                                widget = forms.TextInput(attrs={'class': 'myfieldclass'}))
    last_name = forms.CharField(required = True,
                                help_text = "Please enter your last name.",
                                widget = forms.TextInput(attrs={'class': 'myfieldclass'}))
    email = forms.EmailField(required = True,
                            help_text = "Please enter your email address.",
                            widget = forms.TextInput(attrs={'class': 'myfieldclass'}))
    username = forms.CharField(required = True, max_length = 20,
                                help_text = "Max length is 20 characters, letters, digits and @/./+/-/_ only.",
                                widget = forms.TextInput(attrs={'class': 'myfieldclass'}))
    password1 = forms.CharField(label = 'Password', required = True, max_length = 20,
                                help_text = "Max length is 20 characters, at least 8 characters, can't be all numbers.",
                                widget = forms.PasswordInput(attrs={'class': 'myfieldclass'}))
    password2 = forms.CharField(label = 'Verify Password', required = True, max_length = 20,
                                help_text = "Please enter the same password as before for verification.",
                                widget = forms.PasswordInput(attrs={'class': 'myfieldclass'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email','username', 'password1', 'password2')

    def save(self, commit = True):
        user = super(RegistrationForm, self).save(commit = False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user
