from django import forms

from news.models import ContactForm, Comment


class FormContact(forms.ModelForm):

    class Meta:
        model=ContactForm
        fields = "__all__"

class CommentForm(forms.ModelForm):

    class Meta:
        model=Comment
        fields=['body']