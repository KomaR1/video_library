import random
import string
from wsgiref.util import FileWrapper

from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from django.db import transaction, DatabaseError
from django.db.models import F
from django.views.generic.base import View, HttpResponseRedirect, HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from search.documents import VideoDocument


from youtube_python.settings import MEDIA_ROOT
from .forms import LoginForm, RegisterForm, NewVideoForm, CommentForm, ComplainForm
from .models import Video, Comment, Complain, CustomUser, Genre

LANGUAGES = (
    ('en', _('English')),
    ('ru', _('Russian')),
)

class MyVideoView(View):
    template_name = 'my_video.html'

    def get(self, request):
        if request.user.is_authenticated:
            user_videos = Video.objects.filter(user__id=request.user.id).order_by('-datetime')
            paginator = Paginator(user_videos, 7)
            page = request.GET.get('page')
            page_obj = paginator.get_page(page)
        else:
            return HttpResponseRedirect('/login')

        return render(request, self.template_name, {'page_obj': page_obj})


# def search(request):
#
#     q = request.GET.get('q')
#
#     if q:
#         posts = VideoDocument.search().query("match", title=q)
#     else:
#         posts = ''
#
#     return render(request, 'index.html', {'posts': posts})

class VideoFileView(View):

    def get(self, request, file_name):
        file = FileWrapper(open(MEDIA_ROOT + '/' + file_name, 'rb'))
        response = HttpResponse(file, content_type='video/mp4')
        response['Content-Disposition'] = 'attachment; filename={}'.format(file_name)
        return response


class HomeView(View):
    template_name = 'index.html'

    def get(self, request):
        most_recent_videos = Video.objects.order_by('-datetime')
        paginator = Paginator(most_recent_videos, 7)
        page = request.GET.get('page')
        page_obj = paginator.get_page(page)
        return render(request, self.template_name, {'page_obj': page_obj})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')


class VideoView(View):
    template_name = 'video.html'

    def get(self, request, id):
        # fetch video from DB by ID
        video_by_id = Video.objects.get(id=id)
        video_by_id.path = 'http://localhost:8000/get_video/' + video_by_id.path
        context = {'video': video_by_id}
        Video.objects.filter(pk=video_by_id.pk).update(views=F('views') + 1)
        video_by_id.views += 1  # to show valid counter in the template

        if request.user.is_authenticated:
            if video_by_id.user_id == request.user.id:
                context['user_is_owner'] = True
            else:
                context['user_is_owner'] = False
            print('user signed in')
            comment_form = CommentForm()
            context['form'] = comment_form
        comments = Comment.objects.filter(video__id=id).order_by('-datetime')[:5]
        print(comments)
        context['comments'] = comments
        return render(request, self.template_name, context)




class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        # pass filled out HTML-Form from View to LoginForm()
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # create a new entry in table 'logs'
                login(request, user)
                print('success login')
                return HttpResponseRedirect('/')
            else:
                return HttpResponseRedirect('/login_error')
        return HttpResponse('This is Login view. POST Request.')


class CommentView(View):
    template_name = 'comment.html'

    def post(self, request):
        # pass filled out HTML-Form from View to CommentForm()
        form = CommentForm(request.POST)
        if form.is_valid():
            # create a Comment DB Entry
            text = form.cleaned_data['text']
            video_id = request.POST['video']
            video = Video.objects.get(id=video_id)

            new_comment = Comment(text=text, user=request.user, video=video)
            new_comment.save()
            return HttpResponseRedirect('/video/{}'.format(str(video_id)))
        return HttpResponse('This is Register view. POST Request.')


class RegisterView(View):
    template_name = 'register.html'

    def get(self, request):
        if request.user.is_authenticated:
            print('already logged in. Redirecting.')
            print(request.user)
            return HttpResponseRedirect('/')
        form = RegisterForm()
        return render(request, self.template_name, {'form': form})

    @csrf_exempt
    def post(self, request):
        # pass filled out HTML-Form from View to RegisterForm()
        form = RegisterForm(request.POST)
        if form.is_valid():
            # create a User account
            print(form.cleaned_data['username'])
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            birth = form.cleaned_data['birth']
            try:
                with transaction.atomic():
                    # All the database operations within this block are part of the transaction
                    user = CustomUser.objects.create_user(email=email, username=username, password=password,
                                                          first_name=first_name, last_name=last_name, birth=birth)
            except DatabaseError:
                # The transaction has failed. Handle appropriately
                pass
            return HttpResponseRedirect('/login')
        return HttpResponse('Введены некорректные данные')


class NewVideo(View):
    template_name = 'new_video.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/login')

        form = NewVideoForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        # pass filled out HTML-Form from View to NewVideoForm()
        form = NewVideoForm(request.POST, request.FILES)

        if form.is_valid():
            # create a new Video Entry
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            file = form.cleaned_data['file']
            genre = form.cleaned_data['genre']
            random_char = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            path = random_char + file.name

            fs = FileSystemStorage(location=MEDIA_ROOT)
            filename = fs.save(path, file)
            file_url = fs.url(filename)

            print(fs)
            print(filename)
            print(file_url)
            try:
                with transaction.atomic():
                    genre_new = Genre.objects.get_or_create(genre=genre)
            except DatabaseError:
                # The transaction has failed. Handle appropriately
                pass
            new_genre = Genre.objects.get(genre=genre)
            new_video = Video(title=title,
                              description=description,
                              user=request.user,
                              path=path,
                              genre_id=new_genre.id)
            new_video.save()

            # redirect to detail view template of a Video
            return HttpResponseRedirect('/video/{}'.format(new_video.id))
        else:
            return HttpResponse('Your form is not valid. Go back and try again.')


class ComplainView(View):
    template_name = 'complain.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/')
        form = ComplainForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        # pass filled out HTML-Form from View to ComplainForm()
        form = ComplainForm(request.POST)
        print(request.user)
        if form.is_valid():
            text = form.cleaned_data['text']
            new_complain = Complain(text=text, user_id=request.user)
            new_complain.save()
            return HttpResponseRedirect('/')
        return HttpResponse('This is Complain view. POST Request.')


class LoginErrorView(View):
    template_name = 'login_error.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        # pass filled out HTML-Form from View to ComplainForm()
        print(request.user)
        return HttpResponseRedirect('/login')


def btn_click(request, id):
    if request.user.is_authenticated:
        # if request.user.id == list(Video.objects.filter(pk=id))[0].user_id:
        video = get_object_or_404(Video, pk=id)
        video.delete()
        return HttpResponseRedirect('/my_videos')
        #else:
            #return HttpResponse('ПАШОЛ НАХУЙ id не сходятся')
    else:
        return HttpResponse('ПАШОЛ НАХУЙ ПРОСТО')
