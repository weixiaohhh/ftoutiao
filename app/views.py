# coding:utf8
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views import generic
from .models import Article

from .forms import ShareForm, SubjectForm
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from account.models import Profile, Subject, Subscription, Friendship
from app.models import Article
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.

class IndexvView(generic.ListView):
    template_name = "app/index.html"
    context_object_name = "articles"

    def get_queryset(self):
        articles = Article.objects.all()
        return articles


def subjectinfo(request, pk, choice):



	profile = Profile.objects.get(pk=pk)

	# 新文章
	new_articles = profile.get_new_article()
	# 热门文章
	hot_articles = profile.get_hot_article()
    # 订阅者视图
		
	subscribers = profile.get_subscript_user()
	subscribers_count = len(subscribers)


	
	

	context = {
        'profile': profile,
        'hot_articles': hot_articles,
        'new_articles': new_articles,
        'choice': choice,
		'subscribers': subscribers,
		'subscribers_count': subscribers_count,

    }
	choice_list = ['index', 'new','subscribers']
	if choice not in choice_list:
		raise Http404(u'<b>404,找不到你要访问的页面</b>')
	return render(request, "app/subject_info.html ", context=context)


# 分享编辑
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
@login_required
def share(request):
   
	if request.method == 'POST':
		article_form = ShareForm(data=request.POST, user=request.user.profile)

		if article_form.is_valid():
			profile = request.user.profile
			
			new_article = article_form.save(commit=False)
			new_article.author = profile
			new_article.save()
			new_article.collection_user.add(profile)
			
				
			return redirect(reverse('index', args=[]))
	
	else:
		form = ShareForm(user=request.user.profile)

                    
	return render(request, 'app/share.html',
					{'form': form} )

@login_required
def userinfo(request, pk, choice):
	profile = Profile.objects.get(pk=pk)


	# 新文章
	new_articles = profile.get_new_article()
	# 热门文章
	hot_articles = profile.get_hot_article()
	# 独家号
	user_subjects = profile.get_user_subject() # 用户的独家号
	dy_subjects = profile.get_subscript_subject() # 订阅的独家号
	subjects = set(user_subjects + dy_subjects) # 避免重复
	subject_count = len(subjects)
	# 收藏文章
	favorite_articles = profile.collection_articles.all()

	# 关注
	followings = profile.get_following()

	# 关注者
	followers = profile.get_follower()



	
	context = {
						'profile': profile,
						'subject_count': subject_count,
						'hot_articles': hot_articles,
						'new_articles': new_articles,
						'subjects': subjects,
						'favorite_articles': favorite_articles,
						'followings': followings,
						'followers': followers,
						'choice': choice,
	}

	choice_list = ['index', 'new', 'subjects', 'favorite_articles', 'followings', 'followers']
	if choice not in choice_list:
		raise Http404(u'<b>404,找不到你要访问的页面</b>')

	return render(request, 'app/user_info.html', context=context)



@login_required
def subject_edit(request):
	
	user = request.user.profile
	instance = Subject.objects.all().filter(user=user).first()
	if request.method == 'POST':
		form = SubjectForm(data=request.POST, instance=instance) 
		if form.is_valid():
			f = form.save(commit=False)
			f.user = user
			f.save()
			return redirect(reverse('index', args=[]))
	else:
		user = request.user.profile
		subject = Subject.objects.all().filter(user=user).first()
		editform = SubjectForm(instance=subject)

	return render(request, 'app/subject_edit.html', {'editform': editform})





from django.http import HttpResponse, JsonResponse
from common.decorators import ajax_required
from django.views.decorators.http import require_POST
@login_required
@ajax_required
@require_POST
def article_like(request):
    article_id = request.POST.get('id')
    action = request.POST.get('action')
    if article_id and action:
        
        article = Article.objects.get(id=article_id)
        if action == 'like':
            article.likes.add(request.user.profile)
        else:
            article.likes.remove(request.user.profile)
        return JsonResponse({'status':'ok'})
        
            
    return JsonResponse({'status':'ko',
			'a':article_id,
			'b':action})


@login_required
@ajax_required
@require_POST
def article_collection(request):
    article_id = request.POST.get('id')
    action = request.POST.get('action')
    if article_id and action:
        
        article = Article.objects.get(id=article_id)
		
        if action == 'collection':
            article.collection_user.add(request.user.profile)
        else:
            article.collection_user.remove(request.user.profile)
        return JsonResponse({'status':'ok'})
        
            
    return JsonResponse({'status':'ko'})


@login_required
@ajax_required
@require_POST
def follow(request):
    article_id = request.POST.get('id')
    action = request.POST.get('action')
    if article_id and action:
        
        article = Article.objects.get(id=article_id)
        user = article.author
        if action == 'following':
            request.user.profile.follow(user)
        else:
            request.user.profile.unfollow(user)
        return JsonResponse({'status':'ok'})
        
            
    return JsonResponse({'status':'ko'})

@login_required
@ajax_required
@require_POST
def subscript(request):
    article_id = request.POST.get('id')
    action = request.POST.get('action')
    if article_id and action:
        
        article = Article.objects.get(id=article_id)
        user = article.author
        subject = user.subject.all()[0]
        if action == 'subscripting':
            request.user.profile.subscripte(subject)
        else:
			request.user.profile.unsubscripte(subject)
        return JsonResponse({'status':'ok'})
        
            
    return JsonResponse({'status':'ko'})


from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required
def article_list(request):
    articles = Article.objects.all()
    paginator = Paginator(articles, 5)
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        articless = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            # If the request is AJAX and the page is out of range return an empty page
            return HttpResponse('')
        # If page is out of range deliver last page of results
        articles = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request,
                      'app/index_ajax.html',
                      {'section': 'articles', 'articles': articles})
    return render(request,
                  'app/index.html',
                   {'section': 'articles', 'articles': articles})
