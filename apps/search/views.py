from django.shortcuts import render
from apps.blog.models import Post
from apps.sermon.models import Sermon
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from itertools import chain
from django.contrib.auth import get_user_model

# Create your views here.
def search(request):
    query = request.GET.get("q")
    search_query = SearchQuery(query)
    post_search_vector = SearchVector("title", "body")
    sermon_search_vector = SearchVector("title", "content")
    post_search = (
        Post.objects.annotate(
            search=post_search_vector, rank=SearchRank(post_search_vector, search_query)
        )
        .filter(search=search_query)
        .order_by("-rank")
    )
    sermon_search = (
        Sermon.objects.annotate(
            search=sermon_search_vector,
            rank=SearchRank(sermon_search_vector, search_query),
        )
        .filter(search=search_query)
        .order_by("-rank")
    )
    r = chain(post_search, sermon_search)
    result = list(r)
    context = {"search_result": result, "query": query}
    return render(request, "search/search_result.html", context)
