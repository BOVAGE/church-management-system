from django.shortcuts import render
from blog.models import Post
from sermon.models import Sermon
from django.contrib.postgres.search import SearchVector
from itertools import chain
from django.contrib.auth import get_user_model

# Create your views here.
def search(request):
    query = request.GET.get('q')
    post_search = Post.objects.filter(body__search=query)
    sermon_search = Sermon.objects.filter(content__search=query)
    r = chain(post_search, sermon_search)
    result = list(r)
    context = {'search_result': result, 'query': query}
    return render(request, 'search/search_result.html', context)