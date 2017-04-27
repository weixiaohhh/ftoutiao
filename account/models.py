# coding:utf-8
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	github_username = models.CharField(u'Github用户名', max_length=16, blank=True)
	site = models.URLField(u'个人主页', blank=True)
	introduction = models.CharField('一句话介绍', max_length=64, blank=True)
	date_of_birth = models.DateField(blank=True, null=True)
	photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True,default='users/default/Path.png')


	def get_hot_article(self):
		articles = self.author_article.all().order_by('-likes')
		return articles
	
	def get_new_article(self):
		articles = self.author_article.all().order_by('-create_time')
		return articles
	
	# 获得关注者
	def get_follower(self):
		
		user_list = []
		for follower_user in self.follower.all():
			user_list.append(follower_user.follower)
		return user_list


	# 获得关注
	def get_following(self):
		
		user_list = []
		for following_user in self.following.all():
			user_list.append(following_user.following)
		return user_list


	def follow(self, user):
		if not self.is_following(user):
			Friendship.objects.create(following=user, follower=self)

    # 判断是否该用户是否已经关注
	def is_following(self, user):
		return self.follower.filter(following=user).first() is not None

	def unfollow(self, user):
		f = self.follower.filter(following=user).first()
		if f:
			f.delete()

	def is_followed_by(self, user):
		return self.following.filter(follower=user).first() is not None

#获取用户独家号
	def get_user_subject(self):
		subjects = []
		for subject in self.subject.all():
			subjects.append(subject)
		return subjects

# 获取所有订阅的独家号
	def get_subscript_subject(self):
		subjects = []
		for subscription in	 self.subscription.all():
			subjects.append(subscription.subject)
		return subjects
# 获取所有订阅的用户
	def get_subscript_user(self):
		users = []
		for subscription in	 self.subscription.all():
			users.append(subscription.user)
		return users
	
	def subscripte(self, subject):
		if not self.is_subscripting(subject):
			Subscription.objects.create(user=self,subject=subject)
		
	def is_subscripting(self, subject):
		return self.subscription.filter(subject=subject).first() is not None

   	def unsubscripte(self, subject):
		s = self.subscription.filter(subject=subject).first()
		if s:
			s.delete()

	def save(self, *args, **kwargs):
		super(Profile, self).save(*args, **kwargs)  # Call the "real" save() method.
        # 自己关注自己
		self.follow(self)
        # 自动创建主题
		Subject.objects.get_or_create(title=self.user.username + u'的独家号', user=self)
		# 自动订阅自己的主题
		self.subscripte(self.subject.all()[0])

	def __unicode__(self):
		return self.user.username

# 接收User 的变化
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


# 订阅号
class Subject(models.Model):
    title = models.CharField(u'独家号', max_length=32 )
    user = models.ForeignKey(Profile, related_name='subject')

# 获取所有订阅的用户
    def get_subscripted_user():
        users = []
        for subscription in	 self.subscripted.all():
             users.append(subscription.user)
        return users
		

    def __unicode__(self):
        return self.title

# 关注
class Friendship(models.Model):
	following = models.ForeignKey(Profile, related_name='following')
	follower = models.ForeignKey(Profile, related_name='follower')
	create_time = models.DateTimeField(u'创建时间', auto_now_add=True)

	def __init__(self, *args, **kwargs):
		super(Friendship, self).__init__(*args, **kwargs)

	def __unicode__(self):
		return "被关注者：{0},关注者：{1}".format(
            self.following.user.username, self.follower.user.username
        )

# 订阅
class Subscription(models.Model):
	user = models.ForeignKey(Profile, related_name='subscription')
	subject =  models.ForeignKey(Subject, related_name='subscripted')

	def __unicode__(self):
		
		return "{0}订阅了{1}".format(self.user.user.username, self.subject.title)


		
