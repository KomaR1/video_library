import random
import string
from wsgiref.util import FileWrapper

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.views.generic.base import View, HttpResponseRedirect, HttpResponse

from youtube_python.settings import MEDIA_ROOT
from .forms import LoginForm, RegisterForm, NewVideoForm, CommentForm, ComplainForm
from .models import Video, Comment, Complain


# class ProfileView(View):
#     template_name = 'profile.html'
#     def get(self, request):
#         if not request.user.is_authenticated:
#             return HttpResponseRedirect('/')
#         form = UserForm
#         return render(request, self.template_name, {'form': form})
#
#     def post(self, request):
#         print(User.object.get)
#         print(User.username)
#         print(User.password)
#         # pass filled out HTML-Form from View to LoginForm()
#         form = ProfileView(request.POST)
#         if form.is_valid():
#             # email = form.cleaned_data['email']
#             full_name = form.cleaned_data['full_name']
#             birth = form.cleaned_data['birth']
#             new_profile = UserProfile(full_name=full_name, birth=birth)
#             new_profile.user = User
#             new_profile.save()
        #     if user is not None:
        #         # create a new entry in table 'logs'
        #         login(request, user)
        #         print('success login')
        #         return HttpResponseRedirect('/')
        #     else:
        #         return HttpResponseRedirect('login')
        # return HttpResponse('This is Login view. POST Request.')


class VideoFileView(View):
    
    def get(self, request, file_name):
        file = FileWrapper(open(MEDIA_ROOT+'/'+file_name, 'rb'))
        response = HttpResponse(file, content_type='video/mp4')
        response['Content-Disposition'] = 'attachment; filename={}'.format(file_name)
        return response


class HomeView(View):
    template_name = 'index.html'

    def get(self, request):
        most_recent_videos = Video.objects.order_by('-datetime')[:8]
        return render(request, self.template_name, {'most_recent_videos': most_recent_videos})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')


class VideoView(View):
    template_name = 'video.html'

    def get(self, request, id):
        # fetch video from DB by ID
        video_by_id = Video.objects.get(id=id)
        video_by_id.path = 'http://localhost:8000/get_video/'+video_by_id.path
        context = {'video':video_by_id}
        
        if request.user.is_authenticated:
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
                return HttpResponseRedirect('login')
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

    def post(self, request):
        # pass filled out HTML-Form from View to RegisterForm()
        form = RegisterForm(request.POST)
        if form.is_valid():
            # create a User account
            print(form.cleaned_data['username'])
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            full_name = form.cleaned_data['full_name']
            new_user = User(username=username, email=email, full_name=full_name)
            new_user.set_password(password)
            new_user.save()
            return HttpResponseRedirect('/login')
        return HttpResponse('This is Register view. POST Request.')


class NewVideo(View):
    template_name = 'new_video.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/login')
        
        form = NewVideoForm()
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        # pass filled out HTML-Form from View to NewVideoForm()
        form = NewVideoForm(request.POST, request.FILES)       

        if form.is_valid():
            # create a new Video Entry
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            file = form.cleaned_data['file']

            random_char = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            path = random_char+file.name

            fs = FileSystemStorage(location=MEDIA_ROOT)
            filename = fs.save(path, file)
            file_url = fs.url(filename)

            print(fs)
            print(filename)
            print(file_url)

            new_video = Video(title=title, 
                            description=description,
                            user=request.user,
                            path=path)
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