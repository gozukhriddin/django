from django import forms
from django.contrib.auth.models import User
from .models import ProfileUser

class loginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)


class RegistrForm(forms.ModelForm):
    password=forms.CharField(label='Parolni kiriting',
                              widget=forms.PasswordInput)
    password2=forms.CharField(label='Parolni takrorlang',
                              widget=forms.PasswordInput)

    class Meta:
        model = User
        fields=['username', 'first_name',  'email']

    def clean_password2(self):
        data=self.cleaned_data
        if data['password']!=data['password2']:
            raise forms.ValidationError('Sizning parolingiz mos eams')
        return data['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','email']

class ProfilEditForm(forms.ModelForm):
    class Meta:
        model=ProfileUser
        fields=['photo','date_brith']

