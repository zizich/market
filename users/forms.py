from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from users.models import User


class UserLoginForm(AuthenticationForm):

    # username = forms.CharField()
    # password = forms.CharField()

    # username = forms.CharField(
    #     label='Имя',
    #     widget=forms.TextInput(attrs={"autofocus": True,
    #                                   "class": "form-control",
    #                                   "placeholder": "Введите ваше имя пользователя"}))
    # password = forms.CharField(
    #     label="Пароль",
    #     widget=forms.PasswordInput(attrs={"autocomplete": "current-password",
    #                                       "class": "form-control",
    #                                       "id": "password",
    #                                       "placeholder": "Введите ваш пароль"}))

    class Meta:
        model = User
        fields = ['username', 'password']


# класс для регистрации нового пользователя
class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2',
        ]

    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()
    email = forms.CharField()
    password1 = forms.CharField()
    password2 = forms.CharField()

    # first_name = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             "class": "form-control",
    #             "placeholder": "Введите ваше имя",
    #         }
    #     )
    # )
    #
    # last_name = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             "class": "form-control",
    #             "placeholder": "Введите вашу фамилию",
    #         }
    #     )
    # )
    #
    # username = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             "class": "form-control",
    #             "placeholder": "Введите ваше имя пользователя",
    #         }
    #     )
    # )
    #
    # email = forms.CharField(
    #     widget=forms.EmailInput(
    #         attrs={
    #             "class": "form-control",
    #             "placeholder": "Введите ваш e-mail: *youremail@example.com",
    #         }
    #     )
    # )
    #
    # password1 = forms.CharField(
    #     widget=forms.PasswordInput(
    #         attrs={
    #             "class": "form-control",
    #             "placeholder": "Введите ваш пароль",
    #         }
    #     )
    # )
    #
    # password2 = forms.CharField(
    #     widget=forms.PasswordInput(
    #         attrs={
    #             "class": "form-control",
    #             "placeholder": "Подтвердите пароль",
    #         }
    #     )
    # )
