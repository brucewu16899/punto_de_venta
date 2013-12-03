#encoding:utf-8
from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model
###########     

from models import Usuario
User = get_user_model()


class CrearusuarioForm(forms.ModelForm):
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Verifica contraseña", widget=forms.PasswordInput)
    
    class Meta:
        model = Usuario
        fields = ('usuario', 'perfil', 'sucursal','codigo','supervisa','user_permissions', 'is_superuser')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password2

    def save(self, commit=True):
        user = super(CrearusuarioForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class CambiarusuarioForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text="<a href='password/'>Cambiar contraseña</a>")
    class Meta:
        model = Usuario
        fields = ('usuario', 'perfil', 'sucursal','codigo','supervisa', 'activo', 'administrador', 'user_permissions', 'is_superuser')

    def clean_password(self):
        return self.initial['password']

class InicioForm(forms.Form):
    usuario = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Usuario', 'type':'text', 'autofocus':'True'}), required=True)
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder':'Password','type':'password',}), required=True)



