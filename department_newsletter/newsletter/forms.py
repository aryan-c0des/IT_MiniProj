from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Article

class SignUpForm(UserCreationForm):
    department = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'department')

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'content', 'category')
