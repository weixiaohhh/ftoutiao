
---
# 仿开发者头条
-------------



####示例:  
[网站地址](http://ftoutiao.herokuapp.com/)

### 实现 --
- 开发者头条大部分功能实现
-- 第三方社交登录（github）
-- 实现无刷新 点赞，收藏，订阅，关注，首页文章Ajax 分页
-- 实现全文搜索

###原理说明
- 后端用**django+sqlite**，前端使用**bootstrap**
- 第三方社交登录 用的是**social-auth-app-django**库，实现可参考这篇[文章](https://simpleisbetterthancomplex.com/tutorial/2016/10/24/how-to-add-social-login-to-django.html?hmsr=toutiao.io&utm_medium=toutiao.io&utm_source=toutiao.io)
- jQuery Ajax 实现无刷新等功能
- 全文搜索 用的 django-haystack + Whoosh + jieba 这个三个库，具体实现 参考这篇[文章](http://www.jianshu.com/p/5073e25de698?hmsr=toutiao.io&utm_medium=toutiao.io&utm_source=toutiao.io)
- 网站的实现也有借鉴《Django By Example》，中文翻译[地址](http://www.jianshu.com/p/05810d38f93a)

### 下载安装
ftoutiao:  
``` xml
git clone 'xxx'
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
# 查看后台
python manage.py createsuperuser
# 实现社交登录
set S_A_G_K='XXXX'(Github 的OAuth2 ID)
set S_A_G_S='XXXX'(Github 的OAuth2 秘钥)

```

### 注意事项
- 注意 github 创建OAuth2(本地运行)
-- 配置:
> **Authorization callback URL**:http://127.0.0.1:8000/oauth/complete/github/
> **Homepage URL**:http://127.0.0.1:8000/


