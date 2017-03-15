from django.conf.urls import url
from .views import TokenStorage, TokenStorageViewSet, clear_database
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^tokenstorage/$', view=TokenStorage.as_view()),
    url(r'^tokenstorage/reset/$', view=clear_database),
    url(r'^tokenstorage/all/$', view=TokenStorageViewSet.as_view({'get': 'list'})),
    url(r'^tokenstorage/(?P<instance_id>\w{1,50})/$', view=TokenStorage.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
