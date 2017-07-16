from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import home_view,login_view,category_view,detail_view,logout_view,PostCreate,PostUpdate,PostDelete

app_name = "blog"

urlpatterns = [
    url(r'^$', home_view, name="index"),
    url(r'^login$', login_view, name="login"),
    url(r'^logout$', logout_view, name="logout"),
    url(r'^add$', login_required(PostCreate.as_view()), name="add"),
    url(r'^category/(?P<slug>[\w-]+)/$', category_view, name="category"),
    url(r'^detail/(?P<slug>[\w-]+)/$', detail_view, name="detail"),
    url(r'^edit/(?P<slug>[\w-]+)/$', login_required(PostUpdate.as_view()), name="edit"),
    url(r'^delete/(?P<pk>[0-9]+)/$', login_required(PostDelete.as_view()), name="delete"),
]