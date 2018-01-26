# _*_ coding: utf-8 _*_

import urllib
import json
import requests
import subprocess
import locale
import time
import datetime
import threading


from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.db.models import Q
from multiprocessing import Pool

from models import Container, Image, Host
from other import data_serilazer
from other import Dashbord

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

        # for each in all_info:
        #     container_url = 'http://%s/containers/json?all=1' % (each.host, )
        #     container_info = urllib.urlopen(container_url).read()
        #     container_info_list = json.loads(container_info)
        #
        #     if isinstance(container_info_list, list):
        #         container_result = 'success'
        #         for each_container in container_info_list:
        #             # print each_container
        #             container_id = each_container['Id']
        #             container_state = each_container['State']
        #
        #             Container.objects.filter(container_id=container_id).update(state=container_state)
        #
        #     elif isinstance(container_info_list, dict):
        #         container_result = container_info_list['message']

        # all_info = Container.objects.all()

        # 添加container中的host列表
        add_info = Host.objects.all()

        return render(request, 'container.html', {'all_info': all_info, 'add_info': add_info})


# container 和 image中的“宿主机”
class SpecifyHostView(View):
    def get(self, request, ip):
        all_info = Host.objects.filter(ip=ip)

        return render(request, 'host.html', {'all_info': all_info})


# container中的“镜像”
class ContainerImageView(View):
    def get(self, request, host, id):
        all_info = Image.objects.filter(Q(image_id=id) & Q(host=host))
        all_host = Host.objects.all().distinct()

        return render(request, 'image.html', {'all_info': all_info, 'all_host': all_host})


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
        all_host = Host.objects.all().distinct()

        return render(request, 'image.html', {'all_info': all_info, 'all_host': all_host})


# host中的“容器数量”
class HostContainerView(View):
    def get(self, request, host):
        all_info = Container.objects.filter(host=host)
        add_info = Host.objects.all()

        return render(request, 'container.html', {'all_info': all_info, 'add_info': add_info})


# 菜单“镜像列表”
class ImageView(View):
    def get(self, request):
        all_info = Image.objects.all()
        all_host = Host.objects.all().distinct()

        return render(request, 'image.html', {'all_info': all_info, 'all_host': all_host})


# image中的“容器数量”
class ImageContainerView(View):
    def get(self, request, host, imageid):
        all_info = Container.objects.filter(Q(imageid=imageid) & Q(host=host))
        add_info = Host.objects.all()

        return render(request, 'container.html', {'all_info': all_info, 'add_info': add_info})


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
            info = 'unreachable'

        if not Host.objects.filter(ip=host):
            Host.objects.create(ip=host,
                                container_number=container_number,
                                image_number=image_number,
                                info=json.dumps(host_info_list, sort_keys=True, indent=4))
        else:
            Host.objects.filter(ip=host).update(container_number=container_number,
                                                image_number=image_number,
                                                info=json.dumps(host_info_list, sort_keys=True, indent=4))

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
                container_create_time = data_serilazer.convert(each_container['Created'])
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
                image_repository = each_image['RepoTags'][0].split("/")[-1].split(":")[0]
                image_host = Host.objects.get(ip=host)
                image_create_time = data_serilazer.convert(each_image['Created'])
                image_size = each_image['Size']
                image_container_number = Container.objects.filter(Q(imageid=image_id) & Q(host=host)).count()
                print '++container num', image_container_number

                if not Image.objects.filter(Q(image_id=image_id) & Q(host=host)):
                    Image.objects.create(image_id=image_id, repository=image_repository,
                                         host=image_host, create_time=image_create_time,
                                         container_number=image_container_number, size=image_size)
                else:
                    Image.objects.filter(Q(image_id=image_id) & Q(host=host)).update(host=image_host,
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
                if each_container['Id'] == id:
                    restart_status = each_container['State']
                    print restart_status
                    if restart_status == 'running':
                        Container.objects.filter(container_id=id).update(state=restart_status)
                    break
        else:
            restart_status = 'failed'

        return HttpResponse(restart_status)


# 删除容器
class DeleteContainerView(View):
    def get(self, request):
        all_info = Host.objects.all()

        return render(request, 'host.html', {'all_info': all_info})

    def post(self, request, host, id):
        image_id = request.POST.get('image_id', '')
        print host, id, image_id
        delete_url = 'http://%s/containers/%s' % (host, id)
        container_url = 'http://%s/containers/json?all=1' % (host,)

        print delete_url, container_url

        info = requests.delete(delete_url)
        print info

        # try:
        #     info = requests.delete(delete_url)
        #     print info
        #     if info != '':
        #         delete_status = 'failed'
        # except Exception as delete_status:
        #     print delete_status
        #     return HttpResponse(delete_status)

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
            # 删除成功后host和image中的容器数量减少1
            number_host = Host.objects.get(ip=host)
            number_image = Image.objects.get(Q(image_id=image_id) & Q(host=host))
            print number_host, number_image
            number_host.container_number -= 1
            number_image.container_number -= 1
            if number_host.container_number < 0:
                number_host.container_number = 0
            if number_image.container_number < 0:
                number_image.container_number = 0
            number_host.save()
            number_image.save()

        return HttpResponse(delete_status)


# 创建容器
class AddContainerView(View):
    def get(self, request):
        all_info = Host.objects.all()

        return render(request, 'host.html', {'all_info': all_info})

    def post(self, request):
        name = request.POST.get('name', '')
        image = request.POST.get('image', '')
        host = request.POST.get('host', '')
        hostname = request.POST.get('hostname', '')
        address = request.POST.get('address', '')
        gateway = request.POST.get('gateway', '')
        netmask = request.POST.get('netmask', '')
        dns = request.POST.get('dns', '')
        other = request.POST.get('other', '')
        after = request.POST.get('after', '')
        print name, image, host, hostname, address, gateway, netmask, other, after

        data = {
            'Hostname': hostname,
            'Image': image,
            "AttachStdin": True,
            "AttachStdout": True,
            "AttachStderr": True,
            "Tty": True,    # 打开终端，相当于docker run 的 -t选项，如果不加则无法start 容器。
            "OpenStdin": True,   # 开启标准输入，相当于docker run 的 -i选项，如果不开启则进入容器后无法输入命令。
            "HostConfig": {
                "Dns": list(dns),
                "NetworkMode": "none"
            },
        }

        cmd = 'docker exec %s %s' % (name, after)
        print cmd

        url = "http://%s/containers/create?name=%s" % (host, name)
        start_url = "http://%s/containers/%s/start" % (host, name)

        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
        }

        response = requests.request("POST", url, data=json.dumps(data), headers=headers)
        response = json.loads(response.text)

        if 'message' in response.keys():
            add_result = ['error', response['message']]
            return JsonResponse(add_result, safe=False)
        elif 'Id' in response.keys():
            container_id = response['Id']

            # 创建完成后启动容器
            requests.post(start_url)

            # 启动容器后执行命令
            # run = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            # (output, err) = run.communicate()
            #
            # # 判断是否需要对命令结果进行解码
            # if locale.getdefaultlocale()[-1]=='cp936':
            #     output = output.decode('gb2312')
            #     err = err.decode('gb2312')
            #
            # # 判断命令执行结果
            # if err != '':
            #     add_result = ['error', err]
            #     return JsonResponse(add_result, safe=False)
            # else:
            add_result = ['success', container_id]
            local_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            create_time = datetime.datetime.strptime(local_time, '%Y-%m-%d %H:%M:%S')
            imageid = Image.objects.filter(Q(repository=image) & Q(host=host)).values('image_id')

            for each_imageid in imageid:
                imageid = each_imageid['image_id']
            host = Host.objects.get(ip=str(host))

            # try:
            Container.objects.create(container_id=container_id, name=name, imagename=image, imageid=imageid, host=host,
                                     create_time=create_time, state='running')
            number_host = Host.objects.get(ip=str(host))
            number_image = Image.objects.get(Q(image_id=imageid) & Q(host=host))
            print number_host, number_image
            number_host.container_number += 1
            number_image.container_number += 1
            number_host.save()
            number_image.save()
        # except Exception as e:
            #     print e

            return JsonResponse(add_result, safe=False)



        # code, run = commands.getstatusoutput(cmd)
        # print type(code), chardet.detect(run)
        # print output.decode('gb2312'), err.decode('gb2312')

        # print(response.text)
        # return HttpResponse(response.text)


# 添加容器时获取选择的宿主机包含的镜像
class AddInfo(View):
    def get(self, request):

        from django.core.urlresolvers import reverse

        return HttpResponseRedirect(reverse('host'))

    def post(self, request):
        image = []

        host = request.POST.get('selected', '')

        images = Image.objects.filter(host=host)

        for each in images:
            image.append(each.repository)

        return JsonResponse(image, safe=False)


class DashbordView(View):
    def post(self, request):
        res = []
        all_host = Host.objects.all()
        # print u'顺序执行开始', time.strftime('%H:%M:%S', time.localtime())
        # before = time.time()
        # for each in all_host:
        #     # res.append(do(each))
        #     do(each)
        #
        # for line in res:
        #     print line
        # print u'顺序执行结束', time.strftime('%H:%M:%S', time.localtime())
        # after = time.time()
        # use = after-before
        # print u'耗时 ', use

        print u'并发执行开始', time.strftime('%H:%M:%S', time.localtime())
        before = time.time()
        pool = Pool()
        for each in all_host:
            res.append(pool.apply_async(Dashbord.do, args=(each, )))
        pool.close()
        pool.join()
        for a in res:
            print a.get()
        print u'并发执行结束', time.strftime('%H:%M:%S', time.localtime())
        after = time.time()
        use = after-before
        print u'耗时 ', use
        return JsonResponse('aaa', safe=False)


class PullImageView(View):
    def get(self, request):
        all_info = Image.objects.all()
        all_host = Host.objects.all().distinct()

        return render(request, 'image.html', {'all_info': all_info, 'all_host': all_host})

    def post(self, request, ip):
        imagename = request.POST.get('imagename', '')
        url = 'http://%s/images/create?fromImage=%s&tag=%s' % (ip, imagename, 'latest')
        image_url = 'http://%s/images/json?all=1' % (ip,)

        try:
            response = requests.post(url)

            print type(response), response.status_code

            if response.status_code == 200:
                if not 'error' in response.text:
                    result = 'success'
                    image_info = urllib.urlopen(image_url).read()
                    image_info_list = json.loads(image_info)

                    for each_image in image_info_list:
                        image_repository = each_image['RepoTags'][0].split("/")[-1].split(":")[0]
                        if image_repository == imagename:
                            image_id = each_image['Id'].split(":")[-1]
                            image_host = Host.objects.get(ip=ip)
                            image_create_time = data_serilazer.convert(each_image['Created'])
                            image_size = each_image['Size']
                            image_container_number = Container.objects.filter(Q(imageid=image_id) & Q(host=ip)).count()

                            if not Image.objects.filter(Q(repository=imagename) & Q(host=ip)):
                                Image.objects.create(image_id=image_id, repository=image_repository,
                                                     host=image_host, create_time=image_create_time,
                                                     container_number=image_container_number, size=image_size)

                                number_image = Host.objects.get(ip=ip)
                                number_image.image_number += 1
                                number_image.save()
                                break
                            else:
                                result = 'error'
                else:
                    result = 'error'
            else:
                result = 'error'

            return JsonResponse(result, safe=False)

        except Exception as e:
            result = e

            return JsonResponse(result, safe=False)


class DeleteImageView(View):
    def get(self, request):
        all_info = Image.objects.all()
        all_host = Host.objects.all().distinct()

        return render(request, 'image.html', {'all_info': all_info, 'all_host': all_host})

    def post(self, request, ip):
        imageid = request.POST.get('image_id', '')
        url = 'http://%s/images/%s' % (ip, imageid)

        try:
            response = requests.delete(url)

            if response.status_code == 200:
                if not 'error' in response.text:
                    delete_status = 'success'

                    Image.objects.filter(Q(host=ip) & Q(image_id=imageid)).delete()
                    number_image = Host.objects.get(ip=ip)
                    number_image.image_number -= 1
                    number_image.save()

            else:
                delete_status = 'error'

            return JsonResponse(delete_status, safe=False)

        except Exception as e:
            delete_status = e
            return JsonResponse(delete_status, safe=False)
