from django.contrib.auth import login
from django.shortcuts import render, redirect

from pr1.forms import UserRegistrationForm


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

    context = {

    }
    return render(request, 'accounts/index.html', context)

def thirds()