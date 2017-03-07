from django.conf.urls import url
from .views import TokenStorage
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^tokenstorage/$', view=TokenStorage.as_view()),
    url(r'^tokenstorage/(?P<instance_id>\w{1,50})/$', view=TokenStorage.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
