from django.core.paginator import Paginator
from django.shortcuts import render
from search.documents import VideoDocument
from Видеотека.models import Video


def search(request):

    q = request.GET.get('q')

    if q:
        posts = VideoDocument.search().query("multi_match", query=q, fields=["title", "description"])
        id_list = []
        for i in posts:
            id_list.append(i.id)
        video = Video.objects.filter(id__in=id_list)
        return render(request, 'search.html', {'posts': video})
    else:
        posts = ''
        return render(request, 'search.html')


# def search(request):
#
#     q = request.GET.get('q')
#
#     if q:
#         posts = VideoDocument.search().query("match", title=q)
#     else:
#         posts = ''
#         return render(request, 'search.html')
#     return render(request, 'search.html', {'posts': posts})

# def search_genre(request):
#
#     q = request.GET.get('q')
#
#     if q:
#         posts = GenreDocument.search().query("match", genre=q)
#         id_list = []
#         for i in posts:
#             id_list.append(i.id)
#         genre = Genre.objects.filter(id__in=id_list)
#         return render(request, 'search_genre.html', {'posts': genre})
#     else:
#         posts = ''
#         return render(request, 'search_genre.html')
