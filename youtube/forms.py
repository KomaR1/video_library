from django import forms


YEARS = [x for x in range(1940, 2021)]


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=20)
    password = forms.CharField(label='Password', max_length=20)


class RegisterForm(forms.Form):
    username = forms.CharField(label='Username', max_length=20)
    password = forms.CharField(label='Password', max_length=20)
    email = forms.CharField(label='Email', max_length=30)
    full_name = forms.CharField(max_length=60)
    birth = forms.DateField(widget=forms.SelectDateWidget(years=YEARS))


class CommentForm(forms.Form):
    text = forms.CharField(label='text', max_length=300)


class NewVideoForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100)
    description = forms.CharField(label='Description', max_length=300)
    file = forms.FileField()
    genre = forms.CharField(label='Genre', max_length=30)


class ComplainForm(forms.Form):
    text = forms.CharField(label='text', max_length=300)
