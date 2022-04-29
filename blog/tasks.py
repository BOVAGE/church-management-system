from celery import shared_task
from .models import BibleVerse
import redis
from django.conf import settings

#connect to redis
r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)

@shared_task
def today_bible_verse(id):
    today_bible_verse = BibleVerse.objects.get(id=id)
    today_bible_verse = today_bible_verse.get_bible_verse()
    #store in redis 
    r.set('today_bible_verse', today_bible_verse)
    return today_bible_verse