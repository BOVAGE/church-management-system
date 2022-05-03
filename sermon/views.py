from django.shortcuts import render, HttpResponse, get_object_or_404
from django.db.models import Count
from django.template.loader import render_to_string
from .models import Sermon
from django.conf import settings
import os
#added to fix os.add_dll_directory(r"C:\Program Files\GTK3-Runtime Win64\bin")
os.add_dll_directory(r"C:\Program Files\GTK3-Runtime Win64\bin")

import redis, json, weasyprint

#connect to redis
r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)

# Create your views here.
def index(request):
    today_sermon = Sermon.today.first()
    if today_sermon:
        # increment today sermon views by 1 
        total_views = r.get(f'sermon:{today_sermon.id}:views')
        if total_views == None:
            total_views = '0'
        total_views = json.loads(total_views)
        today_sermon_tags_ids = today_sermon.tags.values_list('id', flat=True)
        # gets similar sermon based on the number of tags in common 
        similar_sermons = Sermon.objects.filter(tags__in=today_sermon_tags_ids).exclude(id=today_sermon.id)
        similar_sermons = similar_sermons.annotate(same_tags=Count('tags')).order_by('-same_tags', '-datetime_created')[:2]
        #gets popular sermon based on the number of views
        sermon_ranking = r.zrange('sermon_ranking', 0, -1, desc=True)[:5]
        sermon_ranking_ids = [int(id) for id in sermon_ranking]
        popular_sermons = list(Sermon.objects.filter(id__in=sermon_ranking_ids))
        #sort the popular_sermons objects to be in sync with the sermon_ranking_ids
        popular_sermons.sort(key=lambda sermon: sermon_ranking_ids.index(sermon.id))
        context = {'today_sermon': today_sermon, 'similar_sermons': similar_sermons, 
                'total_views': total_views, 'popular_sermons': popular_sermons}
        return render(request, 'sermon/index.html', context)
    else:
        return HttpResponse('No sermon has been added today! Thank You.')

def detail(request, year, month, day, slug):
    sermon = get_object_or_404(Sermon, date_created__year=year,
                                date_created__month=month,
                                date_created__day=day,
                                slug=slug)
    # increment today sermon views by 1 
    total_views = r.incr(f'sermon:{sermon.id}:views')
    # increment sermon ranking by 1
    r.zincrby('sermon_ranking', 1, sermon.id)
    context = {'sermon': sermon, 'total_views': total_views}
    return render(request, 'sermon/detail.html', context)

def sermon_pdf(request, id):
    # generate the pdf of each sermon 
    sermon = get_object_or_404(Sermon, id=id)
    html = render_to_string('sermon/sermon_pdf.html', {'sermon': sermon})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=sermon_{sermon.slug}.pdf'
    weasyprint.HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response, 
        stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'sermon/css/sermon.css'),
        weasyprint.CSS(settings.STATIC_ROOT + 'blog/css/base.css')])
    return response