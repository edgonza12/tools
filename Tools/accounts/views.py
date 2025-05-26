from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import UserModulePermission


@login_required
def home(request):
    return render(request, 'accounts/home.html')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

# @login_required
# def dashboard_view(request):
#     return render(request, 'accounts/dashboard.html')

# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render
# from .models import UserModulePermission

@login_required
def dashboard_view(request):
    user_permissions = UserModulePermission.objects.filter(
        user=request.user,
        can_access=True,
        module__is_active=True
    ).select_related('module')

    modules = [perm.module for perm in user_permissions]

    return render(request, 'accounts/dashboard.html', {'modules': modules})