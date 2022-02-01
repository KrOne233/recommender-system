from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class CreateUserForm(UserCreationForm):
    class Meta :
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']
        
        # ['username','email','password1','password2']
        
        # '__all__' 

class Rating(forms.Form):
    rating = forms.DecimalField(max_value=5, min_value=1, decimal_places=1)

