from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, UserChangeForm
from django.contrib.auth.models import User


''' Форма регистрации нового пользователя '''
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254,
                             help_text='Обязательное поле. Введите действующий адрес электронной почты.')
    first_name = forms.CharField(max_length=30, required=True, help_text='Обязательное поле. Введите ваше имя.',
                                 label="Имя (Имя Отчество)")

    class Meta:
        model = User
        fields = ['first_name', 'email', 'password1', 'password2']


''' Форма входа пользователя '''
class LoginForm(AuthenticationForm):
    class Meta:
        fields = ['username', 'password']



class ProfileForm(UserChangeForm):
    username = forms.CharField(label="Nik")
    email = forms.EmailField(label="Email / Login", widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']

