from django import forms


# class UserForm(forms.Form):
#     email = forms.CharField(max_length=60)
#     full_name = forms.CharField(max_length=60)
#     birth = forms.DateTimeField(label='What is your birth date?', widget=forms.SelectDateWidget)


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=20)
    password = forms.CharField(label='Password', max_length=20)


class RegisterForm(forms.Form):
    username = forms.CharField(label='Username', max_length=20)
    password = forms.CharField(label='Password', max_length=20)
    email = forms.CharField(label='Email', max_length=30)
    full_name = forms.CharField(label='Full name', max_length=60)


class CommentForm(forms.Form):
    text = forms.CharField(label='text', max_length=300)


class NewVideoForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100)
    description = forms.CharField(label='Description', max_length=300)
    file = forms.FileField()


class ComplainForm(forms.Form):
    text = forms.CharField(label='text', max_length=300)
