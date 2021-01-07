from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            u1 = User.objects.get(username=username)
            u1.profile.voter_id = form.cleaned_data.get('voter_id')
            u1.save()
            messages.success(request, f'Account Created, Please Login')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form':form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Changes have been successfully saved')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    content = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', content)

@login_required
def ChangePassword(request):
    if request.method == 'POST':
        p1 = request.POST['password1']
        p2 = request.POST['password2']
        if len(p1) < 6 or len(p2) < 6:
            messages.success(request, f'Weak or Passwords did not match')
            redirect('chngpass')
        elif p1 == p2 and len(p1) > 6:
            u = request.user
            u.set_password(p1)
            u.save()
            messages.success(request, f'Password Changed Successfully, Please Login')
            return redirect('login')

    return render(request, 'users/chngpass.html')
