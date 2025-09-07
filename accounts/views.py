from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home') # Redirect if already logged in

    if request.method == 'POST':
        # Use Django's built-in form for secure authentication
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            redirect_url = request.GET.get('next', 'home')
            return redirect(redirect_url)
        else:
            # The form will contain the error messages
            messages.error(request, "Please correct the errors below.")
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('home')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        # UserCreationForm automatically handles password matching and existing user checks
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account created for {username}! You can now log in.")
            return redirect('accounts:login')
        else:
            # The form will contain specific errors (e.g., "Username already exists")
            messages.error(request, "Registration failed. Please see the errors below.")
    else:
        form = UserCreationForm()
        
    return render(request, 'accounts/register.html', {'form': form})