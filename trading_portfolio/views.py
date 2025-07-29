from datetime import timezone

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from .forms import SignUpForm, ProfileForm
from .models import UserSession


# Create your views here.
def home(request):
    return render(request, 'home.html', {})


# get the client_ip
def get_client_ip(request):
    ip = request.META.get('REMOTE_ADDR')
    if request.META.get('HTTP_X_FORWARDED_FOR'):
        ip = request.META.get('HTTP_X_FORWARDED_FOR').split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def register(request):
    if request.user.is_authenticated:
        return redirect('accounts/dashboard')

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
            return redirect('profile')
    else:
        form = SignUpForm()
        return render(request, 'accounts/register.html', {'form': form})

    return render(request, 'accounts/register.html', {'form': form})


# profile view
@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, "You Have Successfully Updated!")
            return redirect('dashboard')
    else:
        form = ProfileForm(instance=request.user.profile)

    return render(request, 'accounts/profile.html', {
        'form': form,
        'user': request.user
    })


# login view
@csrf_protect
@never_cache
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            try:

                user_session = UserSession.objects.create(
                    user=user,
                    session_key=request.session.session_key,
                    ip_address=get_client_ip(request),
                    user_agent=request.META.get('HTTP_USER_AGENT', ''),
                )
            except Exception as e:

                # If session_key already exists, update the existing one
                try:
                    user_session = UserSession.objects.get(session_key=request.session.session_key)
                    user_session.user = user
                    user_session.ip_address = get_client_ip(request)
                    user_session.user_agent = request.META.get('HTTP_USER_AGENT', '')
                    user_session.is_active = True
                    user_session.last_activity = timezone.now()
                    user_session.save()
                except UserSession.DoesNotExist:
                    # Log the error for debugging
                    print(f"Session creation error: {e}")
                    pass

            if hasattr(user, 'profile'):
                user.profile.last_login_ip = get_client_ip(request)
                user.profile.save(update_fields=['last_login_ip'])

            messages.success(request, "You Have Been Logged In!")
            return redirect('dashboard')

        else:
            messages.success(request, "There Was An Error Logging In, Please Try Again...")
            return redirect('login')

    else:
        return render(request, 'accounts/login.html')


@login_required
def logout_view(request):
    # deactivate user session
    try:
        user_session = UserSession.objects.get(
            user=request.user,
            session_key=request.session.session_key,
            is_active=True
        )
        user_session.is_active = False
        user_session.save()
    except UserSession.DoesNotExist:
        pass
    logout(request)
    messages.success(request, "You Have Been Logged Out!")
    return redirect('login')


def dashboard(request):
    return render(request, 'accounts/dashboard.html', context={'user': request.user})
