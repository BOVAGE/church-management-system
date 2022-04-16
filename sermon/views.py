from django.shortcuts import render
from django.db.models import Count
from .models import Sermon
# Create your views here.
def index(request):
    today_sermon = Sermon.today.first()
    today_sermon_tags_ids = today_sermon.tags.values_list('id', flat=True)
    # gets similar sermon based on the number of tags in common 
    similar_sermons = Sermon.objects.filter(tags__in=today_sermon_tags_ids).exclude(id=today_sermon.id)
    similar_sermons = similar_sermons.annotate(same_tags=Count('tags')).order_by('-same_tags', '-datetime_created')[:2]
    context = {'today_sermon': today_sermon, 'similar_sermons': similar_sermons}
    return render(request, 'sermon/index.html', context)