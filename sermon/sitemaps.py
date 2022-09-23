from django.contrib.sitemaps import Sitemap
from .models import Sermon


class SermonSitemap(Sitemap):
    changefreq = "daily"
    priority = 1.0

    def items(self):
        return Sermon.objects.all()
