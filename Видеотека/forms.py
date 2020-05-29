from django import forms


YEARS = [x for x in range(1940, 2021)]


class LoginForm(forms.Form):
    username = forms.CharField(label='Имя пользователя', max_length=20)
    password = forms.CharField(label='Пароль', max_length=20)


class RegisterForm(forms.Form):
    username = forms.CharField(label='Имя пользователя', max_length=20)
    password = forms.CharField(label='Пароль', max_length=20)
    email = forms.CharField(label='Email', max_length=30)
    full_name = forms.CharField(label='ФИО', max_length=60)
    birth = forms.DateField(label='Дата рождения', widget=forms.SelectDateWidget(years=YEARS))


class CommentForm(forms.Form):
    text = forms.CharField(label='Текст', max_length=300)


class NewVideoForm(forms.Form):
    title = forms.CharField(label='Название', max_length=100)
    description = forms.CharField(label='Описание', max_length=300)
    file = forms.FileField(label='Файл')
    genre = forms.CharField(label='Жанр', max_length=30)


class ComplainForm(forms.Form):
    text = forms.CharField(label='Текст ', max_length=300)
