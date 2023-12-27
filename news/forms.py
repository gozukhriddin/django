from django import forms

from news.models import ContactForm


class FormContact(forms.ModelForm):

    class Meta:
        model=ContactForm
        fields = "__all__"