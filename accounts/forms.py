from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from typing import ClassVar


class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        label="Nombre de usuario", widget=forms.TextInput(attrs={"class": "input", "placeholder": "usuario_ejemplo"})
    )
    first_name = forms.CharField(
        label="Nombre", widget=forms.TextInput(attrs={"class": "input", "placeholder": "Nombre"})
    )

    last_name = forms.CharField(
        label="Apellido", widget=forms.TextInput(attrs={"class": "input", "placeholder": "Apellido"})
    )

    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.TextInput(attrs={"class": "input", "placeholder": "ejemplo@correo.com"}),
        required=True,
    )

    password1 = forms.CharField(
        label="Contraseña",
        help_text="La contraseña no puede ser solamente numérica, debe tener al menos 8 carácteres y no puede parecerse\
            mucho al nombre de usuario.",
        widget=forms.PasswordInput(
            attrs={
                "class": "input",
            }
        ),
    )

    password2 = forms.CharField(
        label="Confirmar contraseña",
        help_text="Repita la contraseña anterior.",
        widget=forms.PasswordInput(
            attrs={
                "class": "input",
            }
        ),
    )

    class Meta:
        model = User
        fields: ClassVar[list[str]] = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]

        def save(self, commit=True):
            # stop from default saving, intervenes the save process
            # and adds information
            user = super(RegistrationForm, self).save(commit=False)
            user.first_name = self.cleanded_data["first_name"]
            user.last_name = self.cleanded_data["last_name"]
            user.email = self.cleanded_data["email"]

            if commit:
                user.save()

            return user


class ProfileForm(forms.ModelForm):
    rut = forms.CharField(
        required=True, label="RUT", widget=forms.TextInput(attrs={"class": "input", "placeholder": "10.897.570-1"})
    )
    phone = forms.CharField(
        required=True,
        label="Número telefónico",
        help_text="Este servirá para contactarte en caso de que ocurra un inconveniente.",
        widget=forms.TextInput(attrs={"class": "input", "placeholder": "+56975186972"}),
    )

    profile_type = forms.ChoiceField(
        choices=Profile.USER_TYPE,
        required=False,
        label="Tipo de usuario",
        widget=forms.Select(attrs={"class": "select"}),
    )

    class Meta:
        model = Profile
        fields: ClassVar[list[str]] = [
            "rut",
            "phone",
            "profile_type",
        ]
        labels: ClassVar[dict[str, str]] = {
            "rut": "RUT",
            "phone": "Número de teléfono",
            "profile_type": "Tipo de usuario",
        }
