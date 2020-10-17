from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm


def register(request):
    # either GET or POST
    if request.method == 'POST':
        # create new form using provided POST data
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # save the user. Hash password & everything.
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    # if the user's already entered data (and their form was rejected),
    # this return statement will return that same form + error messages
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'users/profile.html')