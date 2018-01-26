# _*_ coding: utf-8 _*_

"""docker_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin


from app01.views import LoginView, LogoutView, IndexView, ContainerView, HostView, ImageView
from app01.views import ContainerImageView, SpecifyHostView, ImageContainerView, HostImageView, HostContainerView
from app01.views import ChkHostView, HostAddView, StartContainerView, StopContainerView, RestartContainerView, DeleteContainerView
from app01.views import AddContainerView, AddInfo, DashbordView, PullImageView, DeleteImageView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),

    # 菜单“容器列表”
    url(r'^container/$', ContainerView.as_view(), name='container'),

    # image中的“容器数量”
    url(r'^container/(?P<host>[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}:[0-9]{0,5})/(?P<imageid>[0-9a-z]+)/$', ImageContainerView.as_view(), name='image_to_container'),

    # host中的“容器数量”
    url(r'^container/(?P<host>[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}:[0-9]{0,5})/$', HostContainerView.as_view(), name='host_to_container'),

    # 菜单“镜像列表”
    url(r'^image/$', ImageView.as_view(), name='image'),

    # container中的“镜像”
    url(r'^image/(?P<host>[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}:[0-9]{0,5})/(?P<id>[a-z0-9A_Z-_]+)/$', ContainerImageView.as_view(), name='container_to_image'),

    # host中的“镜像数量”
    # url(r'image/(?P<host1>[0-9]{1,3})\.(?P<host2>[0-9]{1,3})\.(?P<host3>[0-9]{1,3})\.(?P<host4>[0-9]{1,3})/$', HostImageView.as_view(), name='host_to_image'),
    url(r'^image/(?P<host>[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}:[0-9]{0,5})/$', HostImageView.as_view(), name='host_to_image'),

    # 菜单“宿主机列表”
    url(r'^host/$', HostView.as_view(), name='host'),

    # container 和 image 中的“宿主机”
    url(r'^host/(?P<ip>[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}:[0-9]{0,5})/$', SpecifyHostView.as_view(), name='specify_host'),

    # 检测添加主机
    url(r'chkhost/$', ChkHostView.as_view(), name='chkhost'),

    # 添加主机
    url(r'hostadd/$', HostAddView.as_view(), name='hostadd'),

    # 启动容器
    url(r'container/start/(?P<host>[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}:[0-9]{0,5})/(?P<id>[0-9a-zA-Z]+)/$', StartContainerView.as_view(), name='startcontainer'),

    # 停止容器
    url(r'container/stop/(?P<host>[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}:[0-9]{0,5})/(?P<id>[0-9a-zA-Z]+)/$', StopContainerView.as_view(), name='stopcontainer'),

    # 重启容器
    url(r'container/restart/(?P<host>[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}:[0-9]{0,5})/(?P<id>[0-9a-zA-Z]+)/$', RestartContainerView.as_view(), name='restartcontainer'),

    # 删除容器
    url(r'container/delete/(?P<host>[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}:[0-9]{0,5})/(?P<id>[0-9a-zA-Z]+)/$', DeleteContainerView.as_view(), name='deletecontainer'),

    # 添加容器
    url(r'containeradd/$', AddContainerView.as_view(), name="addcontainer"),

    # 添加容器时获取选择的宿主机包含的镜像
    url(r'addcontainer/$', AddInfo.as_view(), name='containerimage'),

    url(r'dashbord/$', DashbordView.as_view(), name='dashbord'),

    url(r'pullimage/(?P<ip>[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}:[0-9]{0,5})/$', PullImageView.as_view(), name='pullimage'),

    url(r'image/delete/(?P<ip>[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}:[0-9]{0,5})/$', DeleteImageView.as_view(), name='deleteimage'),
]
