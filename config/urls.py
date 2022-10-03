from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404, handler403
from django.contrib.sitemaps.views import sitemap
from apps.sermon.sitemaps import SermonSitemap
from apps.blog.sitemaps import PostSitemap


sitemaps = {
    "posts": PostSitemap,
    "sermons": SermonSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.blog.urls")),
    path("user/", include("apps.user.urls")),
    path("sermon/", include("apps.sermon.urls")),
    path("search/", include("apps.search.urls")),
    path("payment/", include("apps.payment.urls")),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]
handler404 = "apps.blog.views.error_404"
handler403 = "apps.blog.views.error_403"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# admin site overrides
admin.site.index_title = "Believe Administration"
admin.site.site_header = "Believe Administration"
admin.site.site_title = "Believe Admin"
