from django.contrib.auth import login
from django.shortcuts import render, redirect

from pr1.forms import UserRegistrationForm
from django.contrib.auth import authenticate
from django.contrib import messages


def register_user(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()



            login(request, user)
            return redirect("account:index")
    else:
        form = UserRegistrationForm()
    return render(request, "accounts/register.html", {"form": form})

def index(request):
    # Temporary: redirect root to the editor home while templates are being finalized
    from django.shortcuts import redirect
    return redirect('editor:home')


def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('account:index')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login_user')
    return render(request, 'accounts/login.html')

def thirds(request):
    context = {
    }
    return render(request, 'accounts/thirds.html', context)