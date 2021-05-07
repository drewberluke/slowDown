from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

# registration view function, the login and logout functions are part of 
# django's built in auth library 
# sends the user creation form from the auth library to the view. 
# this view should not be called, the url has been disabled to prevent students from 
# registering and viewing the admin page

def register(response):
    if response.method == "POST":
        form = UserCreationForm(response.POST)
        if form.is_valid():
            form.save()
    else:
        form = UserCreationForm()
    return render(response, 'register/register.html', {'form':form})