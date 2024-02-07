# D:\Python\myProject\bookshelves\app\users\views.py
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .forms import RegistrationForm, LoginForm, ProfileForm

from django.shortcuts import render, redirect
from django.contrib.auth import login


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Присваиваем значение "email" полю "username"
            form.cleaned_data['username'] = form.cleaned_data['email']

            # Сохраняем данные формы
            user = form.save(commit=False)  # используем commit=False, чтобы не сохранять пользователя сразу
            user.username = form.cleaned_data['email']  # устанавливаем значение username
            user.save()  # теперь сохраняем пользователя

            # Логиним пользователя после успешной регистрации
            login(request, user)

            return redirect('home')  # Измените 'home' на имя вашего URL-шаблона главной страницы
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Измените 'home' на имя вашего URL-шаблона главной страницы
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})


@login_required
def profile(request):
    user = request.user

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user)
        password_change_form = CustomPasswordChangeForm(user, request.POST)

        if form.is_valid() and password_change_form.is_valid():
            old_password = password_change_form.cleaned_data['old_password']
            new_password1 = password_change_form.cleaned_data['new_password1']
            new_password2 = password_change_form.cleaned_data['new_password2']

            if not user.check_password(old_password):
                messages.error(request, 'Invalid old password.')
            elif new_password1 and new_password1 != new_password2:
                messages.error(request, 'New passwords do not match.')
            else:
                user.set_password(new_password1)
                user.save()
                update_session_auth_hash(request, user)  # Important for maintaining the user's session
                messages.success(request, 'Password changed successfully.')
        else:
            messages.error(request, 'Password change form is not valid.')

        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')  # Redirect to profile page after saving changes

    else:
        form = ProfileForm(instance=user)
        password_change_form = PasswordChangeForm(user)

    return render(request, 'users/profile.html', {'form': form, 'password_change_form': password_change_form})

