from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render

from trading_portfolio.forms import SignUpForm


# Create your views here.
def home(request):
    return render(request, 'home.html', {})

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})

    return render(request, 'register.html', {'form': form})