# coding:utf-8
from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime
from account.models import Profile, Subject
import urllib

class Article(models.Model):
    title = models.CharField(u'标题', max_length=70)
    link = models.URLField(u'链接')
    author = models.ForeignKey(Profile, related_name='author_article', default='')
    create_time = models.DateTimeField(u'创建时间', default=timezone.now)
    views = models.PositiveIntegerField(u'浏览量', default=0)
    
    subject = models.ForeignKey(Subject, related_name='article', null=True, blank=True)
    # 收藏
    collection_user = models.ManyToManyField(Profile, related_name='collection_articles',  blank=True)
    likes = models.ManyToManyField(Profile,
                                   related_name='article_liked',
                                   blank=True)

    def save(self, *args, **kwargs):

        # 文章的独立号默认
        if self.subject == None:
            self.subject = self.author.subject.all()[0]
        super(Article, self).save(*args, **kwargs)  # Call the "real" save() method.


    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=30) <= self.create_time <= now
	
    def getdomain(self):
        proto, rest = urllib.splittype(self.link)
        host, rest = urllib.splithost(rest)
        return host

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-create_time']











