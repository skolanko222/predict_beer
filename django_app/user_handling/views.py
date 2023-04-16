from django.shortcuts import render, redirect
from .models import CustomUser
from django.contrib.auth import login,logout,authenticate
from beer_db.models import Beer
import pandas as pd
from ML.models import Parallel_ML

machine_learning=Parallel_ML()

def login_fun(request):
    """
    Handles the login request of registrated user. Throws an error if incorrect login or password submited.
	Uses the CustomUser model.

    **Context**

    ``CustomUser``
        An instance of :model:`user_handling.snippetform`. 

    **Template:**

    :template:`registration/login.html`
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if  user is not None:
            login(request, user,  backend='django.contrib.auth.backends.ModelBackend')
            return redirect('/predict/')
        else:
            return render(request, 'registration/login.html', {'error_message': 'Incorrect password'})
    else:
        if not machine_learning.built:
            machine_learning.start_creating_model()
        return render(request, 'registration/login.html')
    
def register(request):
    """
    Handles the registration request of non-registrated user. Creates the CustomUser oobject and stores it
	in the database. If submited login is already taken, throws an error and asks for diffrent one.

    **Context:**

    ``CustomUser``
        An instance of :model:`user_handling.customuser`. 

    **Template:**

    :template:`registration/register.html`
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        users = CustomUser.objects.filter(username=username)
        if len(users) > 0:
            return render(request, 'registration/register.html', {'error_message': 'Username already exists'})
        else:
            user = CustomUser.objects.create(username=username)
            user.set_password(password)
            user.save()
            return redirect('users:login')
    else:
        return render(request, 'registration/register.html')

def logout_fun(request):
    """
    Handles the logout request of non-registrated user. Redirects to the login page.

    **Context:**

    ``CustomUser``
        An instance of :model:`user_handling.customuser`

    **Template:**

	Redirect user to:

    :template:`registration/login.html`
    
	"""
    logout(request)
    return redirect('/')
    
def history(request):
    """
    Renders a list of beers that has been fitted for a logged user (via predict_beer app).
	If no user logged in, throws error message that says 'No user logged in'.

    **Context:**

    ``Beer``
        An instance of :model:`beer_db.beer`

    **Template:**

	Redirect user to:

    :template:`beerhistory.html`
    
    """
    if request.user.is_authenticated:
        if request.method == 'GET':
            txt=request.user.history
            hist_list=txt.split(',')
            hist_list=hist_list[1:]
            beer_list=[Beer.objects.get(id=i) for i in pd.unique(hist_list)]
        return render(request, 'BeerHistory.html', {'username':request.user.username, 'history': beer_list})
    else:
        return render(request, 'BeerHistory.html', {'error_message':'No user logged in'})