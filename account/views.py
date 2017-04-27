# coding:utf8


from django.shortcuts import render

from .models import Profile



# def user_login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(username=cd['username'],
#                                 password=cd['password'])
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return HttpResponse(u'验证成功')
#                 else:
#                     return HttpResponse(u'密码错误')
#             else:
#                 return HttpResponse(u'用户未注册')
#     else:
#         form = LoginForm()
#     return render(request, 'account/login.html', {'form': form})


from django.contrib.auth.decorators import login_required
@login_required
def dashboard(request):
    return render(request,
                 'account/dashboard.html',
                 {'section': 'dashboard'})


# 注册
def register(request):


    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            profile = Profile.objects.create(user=new_user)
            return render(request,
                         'account/register_done.html',
                         {'new_user': new_user,
                          'profile':profile})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                 'account/register.html',
                 {'user_form': user_form})

from .forms import LoginForm, UserRegistrationForm, \
UserEditForm, ProfileEditForm
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
@login_required
def profile(request):

    try:
        profile = request.user.profile
    except ObjectDoesNotExist:
        profile = Profile(user=request.user)
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                data=request.POST)
        profile_form = ProfileEditForm(instance=profile,
                                        data=request.POST,
                                        files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect(reverse('index', args=[]))


    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                 'account/profile.html',
                 {'user_form': user_form,
                 'profile_form': profile_form})

