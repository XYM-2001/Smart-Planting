from attr import field
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from matplotlib import widgets

#from authentication.views.user import register
from main.models import Comment


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'


"""class AddPost(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].disabled = True
    class Meta:
        model=Post
    fields = ('title', 'author', 'content')
    widgets = {
        'title': forms.TextInput(attrs={'class': 'form-control'}),
        'author': forms.Select(attrs={'class': 'form-control' ,'readonly': 'readonly'}),
        'content': forms.TextInput(attrs={'class': 'form-control'}),
    }"""

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'content')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }
