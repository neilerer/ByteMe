from django.conf.urls import include,url
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns


urlpatterns = [
    url(r'^i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    url(r'', include('home.urls')),
    url(r'^admin/', admin.site.urls),
                             )
