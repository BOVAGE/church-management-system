from celery import shared_task
from celery.schedules import crontab
from config.celery import app
from .models import BibleVerse
import redis
from django.conf import settings

# connect to redis
r = redis.Redis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB
)


@shared_task
def today_bible_verse(id):
    today_bible_verse = BibleVerse.objects.get(id=id)
    today_bible_verse = today_bible_verse.get_bible_verse()
    # store in redis
    r.set("today_bible_verse", today_bible_verse)
    return today_bible_verse


app.conf.beat_schedule = {
    # Executes at the midnight of every day
    "get-daily-bible-verse": {
        "task": "blog.tasks.today_bible_verse",
        "schedule": crontab(hour=0, minute=5),
        "args": 1,  # (BibleVerse.today.first().id,),
    },
}
