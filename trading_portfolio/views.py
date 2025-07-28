from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages

from trading_portfolio.forms import SignUpForm


# Create your views here.
def home(request):
    return render(request, 'home.html', {})


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # add Authenticate and login functionality in register
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You Have Successfully Registered! Welcome!")
            return redirect('dashboard')
    else:
        form = SignUpForm()
        return render(request, 'accounts/register.html', {'form': form})

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
            return redirect('dashboard')
        else:
            messages.success(request, "There Was An Error Logging In, Please Try Again...")
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out!")
    return redirect('home')


def dashboard(request):
    return render(request, 'accounts/dashboard.html', context={'user': request.user})
