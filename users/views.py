from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


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
    return render(request=request, template_name='users/register.html', context={'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        # request.FILES will include the user's uploaded image
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            # because of 'post get redirect pattern', we want to redirect here.
            # otherwise reloading the page causes a...
            # "are you sure you want to? [...] stuff will be resubmitted" message
            # (makes reloading submit a GET request, and not a POST request)
            return redirect('profile')

    else:
        # these params mean that the fields in these forms are auto filled
        # with current user's data.
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)