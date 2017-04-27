import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'toutiao.settings')

import django
django.setup()

from app.models import Article, User


def populate():
    u = add_user('axe')
    add_page(
        title="Official Python Tutorial",
        link="http://docs.python.org/2/tutorial/",
        author=u
    )

    u = add_user('eric')
    add_page(
        title="How to Think like a Computer Scientist",
        link="http://www.greenteapress.com/thinkpython/",
        author=u
    )

    u = add_user('wex')
    add_page(
        title="Learn Python in 10 Minutes",
        link="http://www.korokithakis.net/tutorials/python/",
        author=u
    )

    for c in Article.objects.all():
            print "- {0} ".format(str(c))


def add_page(title, link, author):
    p = Article.objects.get_or_create(title=title, link=link, author=author)[0]
    return p


def add_user(username):
    u = User.objects.get_or_create(username=username)[0]
    return u


# Start execution here!
if __name__ == '__main__':
    print "Starting Rango population script..."
    populate()