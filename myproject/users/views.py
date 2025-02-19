from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from .models import UserProfile

def home(request):
    return render(request, 'base.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
        else:
            print(form.errors)  
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})

@login_required
def dashboard(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)
    template = 'users/doctor_dashboard.html' if user.user_type == 'doctor' else 'users/patient_dashboard.html'
    return render(request, template, {'user': user, 'profile': profile})

def custom_logout(request):
    logout(request)
    return redirect('home')