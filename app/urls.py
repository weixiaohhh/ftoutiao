# coding:utf-8
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.IndexvView.as_view(), name='index'),
	url(r'^list/$', views.article_list, name='list'),
    # 作者订阅号信息
    url(r'^info/(?P<pk>\d+)/(?P<choice>\w+)/$', views.subjectinfo, name='subjectinfo'),
	# 作者信息
    url(r'^u/(?P<pk>\d+)/(?P<choice>\w+)/$', views.userinfo, name='userinfo'),
	# 分享
    url(r'^share/$', views.share, name='share'),
	#修改订阅号
    url(r'^subject/edit/$', views.subject_edit, name='subject_edit'),

	url(r'^like/$', views.article_like, name='like'),
	url(r'^collection/$', views.article_collection, name='collection'),
	url(r'^follow/$', views.follow, name='follow'),
	url(r'^subscript/$', views.subscript, name='subscript'),

]
