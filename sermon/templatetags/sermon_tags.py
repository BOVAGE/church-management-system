from atexit import register
from django import template
from ..models import Sermon

register = template.Library()


@register.inclusion_tag("sermon/latest_sermons.html")
def show_latest_sermons(count=4):
    latest_sermons = Sermon.objects.all()[:count]
    return {"latest_sermons": latest_sermons}
