from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^faq$', views.faq, name='faq'),
    url(r'^about$', views.about, name='about'),
    url(r'^submission/new/$', views.submission_new, name='submission_new'),
    url(r'^submission/(?P<pk>\d+)/$', views.submission_detail, name='submission_detail'),
    url(r'^submission/(?P<pk>\d+)/edit/$', views.submission_edit, name='submission_edit'),
    url(r'^mapQuery', views.map_query),
]  