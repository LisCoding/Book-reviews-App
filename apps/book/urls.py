from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^authentification$', views.authentification),
    url(r'^create$', views.create),
    url(r'^books$', views.display_books),
    url(r'^books/add$', views.new),
    url(r'^book_review/(?P<user_id>\d+)$', views.book_review),
    url(r'^books/(?P<id>\d+)$', views.show),
    url(r'^user/(?P<id>\d+)$', views.display_user),

    # url(r'^/(?P<id>\d+)/edit$', views.edit),
    # url(r'^/update/(?P<id>\d+)$', views.update),
    # url(r'^/create$', views.create),
    # url(r'^/(?P<id>\d+)/delete$', views.delete)
]
