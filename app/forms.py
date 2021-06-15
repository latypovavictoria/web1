from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from app.models import Question
from app.models import Author
from app.models import Answer
class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput())

class QuestionForm(forms.ModelForm):
    tags = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'tag1, tag2'}))
    class Meta:
        model = Question
        fields = ['title', 'text']


# class RegisterForm(forms.ModelForm):
    # avatar=forms.ImageField()
    # password = forms.CharField(widget=forms.PasswordInput())
    # password2 = forms.CharField(widget=forms.PasswordInput())
    # class Meta:
        # model = User
        # model1=Authoreq
        # fields = ('username', 'first_name', 'email')
        # fields1=['avatar']
    # def clean_password2(self):
        # cd = self.cleaned_data
        # if cd['password'] != cd['password2']:
            # raise forms.ValidationError('Passwords don\'t match.')
        # return cd['password2']
    # def save(self, *args, **kwargs):
        # user=super().save(*args, **kwargs)
        # user.authoreq.avatar=self.cleaned_data['avatar']
        # user.authoreq.save()
        # return user
class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    avatar = forms.ImageField()
class SettingsForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    avatar = forms.ImageField()

# class AnswerForm(forms.ModelForm):
    # class Meta:
        # model=Answer
        # fields=['text']