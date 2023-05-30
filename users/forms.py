import datetime
import uuid
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms
from users.models import User, EmailVerification
from django.utils import timezone

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Введите имя пользователя"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Введите пароль"}))

    class Meta:
        model = User
        fields = ("username", "password")

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        for field_name, filed in self.fields.items():
            filed.widget.attrs['class'] = 'form-control py-4'

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Введите имя"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Введите фамилию"}))
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Введите имя пользователя"}))
    email = forms.CharField(widget=forms.EmailInput(attrs={"placeholder": "Введите email"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Введите пароль"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Подтвердите пароль"}))

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        for field_name, filed in self.fields.items():
            filed.widget.attrs['class'] = 'form-control py-4'

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=True)
        expiration = timezone.now() + datetime.timedelta(hours=48)
        record = EmailVerification.objects.create(user=user, expiration=expiration, code=uuid.uuid4())
        record.send_verification_email()
        return user


class UserProfileForm(UserChangeForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={"required": False}))
    username = forms.CharField(widget=forms.TextInput(attrs={"readonly": True}))
    email = forms.CharField(widget=forms.EmailInput(attrs={"readonly": True}))

    class Meta:
        model = User
        fields = ("image", "username", "email", "first_name", "last_name")

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field_name, filed in self.fields.items():
            filed.widget.attrs['class'] = 'form-control py-4'
        self.fields['image'].widget.attrs['class'] = 'custom-file-label'

