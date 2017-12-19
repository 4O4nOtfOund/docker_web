# _*_ coding: utf-8 _*_

import urllib
import json
import requests

from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse

from models import Container, Image, Host
from other import date_serilazer

# Create your views here.

# 登录
class LoginView(View):
    def get(self, requset):
        return render(requset, 'login.html', {})

    def post(self, request):
        user_name = request.POST.get('username', '')
        pass_word = request.POST.get('password', '')
        user = authenticate(username=user_name, password=pass_word)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'index.html')
            else:
                return render(request, 'login.html', {'error': u'用户未激活'})
        else:
            return render(request, 'login.html', {'error': u'用户名或密码错误'})

# 注销
class LogoutView(View):
    def get(self, request):
        logout(request)
        from django.core.urlresolvers import reverse
        return HttpResponseRedirect(reverse('index'))

# 首页
class IndexView(View):
    def get(self, request):
        container_number = Container.objects.all().count()
        image_number = Image.objects.all().count()
        host_number = Host.objects.all().count()

        return render(request, 'index.html', {'container_number': container_number,
                                              'image_number': image_number, 'host_number': host_number})


# 菜单“容器列表”
class ContainerView(View):
    def get(self, request):

        all_info = Container.objects.all()

        for each in all_info:
            container_url = 'http://%s/containers/json?all=1' % (each.host, )
            container_info = urllib.urlopen(container_url).read()
            container_info_list = json.loads(container_info)

            if isinstance(container_info_list, list):
                container_result = 'success'
                for each_container in container_info_list:
                    # print each_container
                    container_id = each_container['Id']
                    container_state = each_container['State']

                    Container.objects.filter(container_id=container_id).update(state=container_state)

            elif isinstance(container_info_list, dict):
                container_result = container_info_list['message']

        all_info = Container.objects.all()

        return render(request, 'container.html', {'all_info': all_info})


# container 和 image中的“宿主机”
class SpecifyHostView(View):
    def get(self, request, ip):
        all_info = Host.objects.filter(ip=ip)

        return render(request, 'host.html', {'all_info': all_info})


# container中的“镜像”
class ContainerImageView(View):
    def get(self, request, id):
        all_info = Image.objects.filter(image_id=id)

        return render(request, 'image.html', {'all_info': all_info})


# 宿主机列表
class HostView(View):
    def get(self, request):
        all_info = Host.objects.all()

        return render(request, 'host.html', {'all_info': all_info})

    def post(self, request):
        all_info = Host.objects.all()

        return render(request, 'host.html', {'all_info': all_info})


# host中的“镜像数量”
class HostImageView(View):
    def get(self, request, host):
        all_info = Image.objects.filter(host=host)

        return render(request, 'image.html', {'all_info': all_info})


# host中的“容器数量”
class HostContainerView(View):
    def get(self, request, host):
        all_info = Container.objects.filter(host=host)

        return render(request, 'container.html', {'all_info': all_info})


# 菜单“镜像列表”
class ImageView(View):
    def get(self, request):
        all_info = Image.objects.all()

        return render(request, 'image.html', {'all_info': all_info})


# image中的“容器数量”
class ImageContainerView(View):
    def get(self, request, imageid):
        all_info = Container.objects.filter(imageid=imageid)

        return render(request, 'container.html', {'all_info': all_info})


# 检测宿主机
class ChkHostView(View):
    def get(self, request):
        from django.core.urlresolvers import reverse
        return HttpResponseRedirect(reverse('index'))

    def post(self, request):
        ip = request.POST.get('ip', '')
        port = request.POST.get('port', '')
        url = 'http://%s:%s/version' % (ip, port)

        try:
            info = urllib.urlopen(url)
            version = json.loads(info.read())
            version = 'Version: %s' % (version['Version'])
        except Exception as e:
            version = 'error'

        return HttpResponse(version)


# 添加宿主机
class HostAddView(View):
    def get(self, request):

        from django.core.urlresolvers import reverse
        return HttpResponseRedirect(reverse('host'))

    def post(self, request):
        result = ''
        ip = request.POST.get('ip', '')
        port = request.POST.get('port', '')
        host = '%s:%s' % (ip, port)
        host_url = 'http://%s:%s/info' % (ip, port)
        container_url = 'http://%s:%s/containers/json?all=1' % (ip, port)
        image_url = 'http://%s:%s/images/json?all=1' % (ip, port)

        # 添加host时收集host信息
        host_info = urllib.urlopen(host_url).read()
        host_info_list = json.loads(host_info)

        if isinstance(host_info_list, dict):
            host_result = 'success'
            container_number = host_info_list['Containers']
            image_number = host_info_list['Images']
        else:
            host_result = 'error'

        if not Host.objects.filter(ip=host):
            Host.objects.create(ip=host,
                                container_number=container_number,
                                image_number=image_number)
        else:
            Host.objects.filter(ip=host).update(container_number=container_number,
                                              image_number=image_number)

        # 添加host时收集container信息
        container_info = urllib.urlopen(container_url).read()
        container_info_list = json.loads(container_info)

        if isinstance(container_info_list, list):
            container_result = 'success'
            for each_container in container_info_list:
                # print each_container
                container_id = each_container['Id']
                container_name = each_container['Names'][0].replace('/', '')
                container_imagename = each_container['Image']
                container_imageid = each_container['ImageID'].split(":")[-1]
                container_host = Host.objects.get(ip=host)
                print container_host
                container_create_time = date_serilazer.convert(request, each_container['Created'])
                container_state = each_container['State']

                print container_id, container_name, container_imagename, container_imageid, container_host, container_create_time, container_state
                if not Container.objects.filter(container_id=container_id):
                    Container.objects.create(container_id=container_id, name=container_name,
                                             imagename=container_imagename, imageid=container_imageid,
                                             host=container_host, create_time=container_create_time,
                                             state=container_state)
                else:
                    Container.objects.filter(container_id=container_id).update(name=container_name,
                                                                               imagename=container_imagename,
                                                                               imageid=container_imageid,
                                                                               host=container_host,
                                                                               create_time=container_create_time,
                                                                               state=container_state)

        elif isinstance(container_info_list, dict):
            container_result = container_info_list['message']

        # 添加host时，收集image信息
        image_info = urllib.urlopen(image_url).read()
        image_info_list = json.loads(image_info)

        if isinstance(image_info_list, list):
            image_result = 'success'
            for each_image in image_info_list:
                # print each_image
                image_id = each_image['Id'].split(":")[-1]
                print image_id
                image_repository = each_image['RepoTags'][0].split("/")[-1].split(":")[0]
                image_host = Host.objects.get(ip=host)
                image_create_time = date_serilazer.convert(request, each_image['Created'])
                image_size = each_image['Size']
                image_container_number = Container.objects.filter(imageid=image_id).count()

                if not Image.objects.filter(image_id=image_id):
                    Image.objects.create(image_id=image_id, repository=image_repository,
                                         host=image_host, create_time=image_create_time,
                                         container_number=image_container_number, size=image_size)
                else:
                    Image.objects.filter(image_id=image_id).update( host=image_host,
                                                                    create_time=image_create_time,
                                                                    container_number=image_container_number,
                                                                    size=image_size)

        elif isinstance(image_info_list, dict):
            image_result = image_info_list['message']


        if host_result == 'success' and container_result == 'success' and image_result == 'success':
            result = 'success'
        else:
            result = 'error'

        return render(request, 'host.html', {'result': result})


# 启动容器
class StartContainerView(View):
    def get(self, request):
        all_info = Host.objects.all()

        return render(request, 'host.html', {'all_info': all_info})

    def post(self, request, host, id):
        print host, id
        start_url = 'http://%s/containers/%s/start' % (host, id)
        container_url = 'http://%s/containers/json?all=1' % (host, )

        print start_url, container_url

        try:
            info = requests.post(start_url)
            print info
            if info != '':
                start_status = 'failed'
        except Exception as start_status:
            print start_status
            return HttpResponse(start_status)
        # start_info = requests.post(start_url)

        # if start_info.text == '':
        #     start_status = 'success'

        container_info = urllib.urlopen(container_url).read()
        container_info_list = json.loads(container_info)

        if isinstance(container_info_list, list):
            for each_container in container_info_list:
                # print each_container
                if each_container['Id'] == id:
                    start_status = each_container['State']
                    if start_status == 'running':
                        Container.objects.filter(container_id=id).update(state=start_status)
                    break
        else:
            start_status = 'failed'

        return HttpResponse(start_status)


# 停止容器
class StopContainerView(View):
    def get(self, request):
        all_info = Host.objects.all()

        return render(request, 'host.html', {'all_info': all_info})

    def post(self, request, host, id):
        print host, id
        stop_url = 'http://%s/containers/%s/stop' % (host, id)
        container_url = 'http://%s/containers/json?all=1' % (host, )

        print stop_url, container_url

        try:
            info = requests.post(stop_url)
            print info
        except Exception as stop_status:
            print stop_status
            return HttpResponse(stop_status)
        # stop_info = requests.post(stop_url)

        # if stop_info.text == '':
        #     stop_status = 'success'

        container_info = urllib.urlopen(container_url).read()
        container_info_list = json.loads(container_info)

        if isinstance(container_info_list, list):
            for each_container in container_info_list:
                # print each_container
                if each_container['Id'] == id:
                    stop_status = each_container['State']
                    if stop_status != 'running':
                        Container.objects.filter(container_id=id).update(state=stop_status)
                    break
        else:
            stop_status = 'failed'

        return HttpResponse(stop_status)


# 重启容器
class RestartContainerView(View):
    def get(self, request):
        all_info = Host.objects.all()

        return render(request, 'host.html', {'all_info': all_info})

    def post(self, request, host, id):
        print host, id
        restart_url = 'http://%s/containers/%s/restart' % (host, id)
        container_url = 'http://%s/containers/json?all=1' % (host, )

        print restart_url, container_url

        container_info = urllib.urlopen(container_url).read()
        container_info_list = json.loads(container_info)

        if isinstance(container_info_list, list):
            for each_container in container_info_list:
                # print each_container
                if each_container['Id'] == id:
                    restart_status_befroe = each_container['State']
                    print restart_status_befroe
                    break
        else:
            restart_status = 'failed'

        try:
            info = requests.post(restart_url)
            print info
        except Exception as restart_status:
            print restart_status
            return HttpResponse(restart_status)

        container_info = urllib.urlopen(container_url).read()
        container_info_list = json.loads(container_info)

        if isinstance(container_info_list, list):
            for each_container in container_info_list:
                # print each_container
                if each_container['Id'] == id:
                    restart_status = each_container['State']
                    print restart_status
                    if restart_status == 'running' and restart_status == restart_status_befroe:
                        Container.objects.filter(container_id=id).update(state=restart_status)
                    break
        else:
            restart_status = 'failed'

        return HttpResponse(restart_status)


class DeleteContainerView(View):
    def get(self, request):
        all_info = Host.objects.all()

        return render(request, 'host.html', {'all_info': all_info})

    def post(self, request, host, id):
        print host, id
        delete_url = 'http://%s/containers/%s' % (host, id)
        container_url = 'http://%s/containers/json?all=1' % (host,)

        print delete_url, container_url

        try:
            info = requests.delete(delete_url)
            print info
            if info != '':
                delete_status = 'failed'
        except Exception as delete_status:
            print delete_status
            return HttpResponse(delete_status)

        container_info = urllib.urlopen(container_url).read()
        container_info_list = json.loads(container_info)

        if isinstance(container_info_list, list):
            for each_container in container_info_list:
                # print each_container
                if each_container['Id'] == id:
                    delete_status = 'failed'
                    # delete_status = each_container['State']
                    # print delete_status
                    # if delete_status == 'running' and delete_status == delete_status_befroe:
                    #     Container.objects.filter(container_id=id).update(state=delete_status)
                    break
                else:
                    delete_status = 'success'
        else:
            delete_status = 'failed'

        if delete_status == 'success':
            Container.objects.filter(container_id=id).delete()

        return HttpResponse(delete_status)


# 创建容器
class AddContainerView(View):
    def get(self, request):
        all_info = Host.objects.all()

        return render(request, 'host.html', {'all_info': all_info})

    def post(self, request):
        hostname = request.POST.get('hostname', '')
        image = request.POST.get('image', '')
        networkmode = request.POST.get('networkmode', '')

        data = {
            "Hostname": hostname,
            "Image": image,
            "NetworkMode": networkmode,
        }

        url = "http://192.168.2.145:5555/containers/create"

        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
        }

        response = requests.request("POST", url, data=data, headers=headers)

        print(response.text)
