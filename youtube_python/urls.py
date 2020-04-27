from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from youtube.views import HomeView, NewVideo, CommentView, LoginView, RegisterView, VideoView, VideoFileView, LogoutView, ComplainView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view()),
    path('login/', LoginView.as_view()),
    path('register/', RegisterView.as_view()),
    path('new_video/', NewVideo.as_view()),
    path('video/<int:id>', VideoView.as_view()),
    path('comment/', CommentView.as_view()),
    path('get_video/<file_name>', VideoFileView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('complain/', ComplainView.as_view()),
    #path('profile/', ProfileView.as_view())
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns