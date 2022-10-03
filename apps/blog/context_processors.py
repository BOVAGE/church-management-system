from apps.blog.models import Announcement


def announcement(request):
    # only show one announcement at a time
    try:
        context = {"announcement": Announcement.objects.filter(featured=True)[0]}
    except IndexError:
        context = {"announcement": ""}
    return context
