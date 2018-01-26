# _*_ coding: utf-8 _*_

import urllib
import json
import django
django.setup()

from django.db.models import Q

from app01.models import Host, Image, Container
import data_serilazer


def do(host):
    host_url = 'http://%s/info' % (host, )
    container_url = 'http://%s/containers/json?all=1' % (host,)
    image_url = 'http://%s/images/json?all=1' % (host,)

    # 添加host时收集host信息
    try:
        host_info = urllib.urlopen(host_url).read()
        host_info_list = json.loads(host_info)

        if isinstance(host_info_list, dict):
            host_result = 'success'
            container_number = host_info_list['Containers']
            image_number = host_info_list['Images']

            Host.objects.filter(ip=str(host)).update(container_number=container_number,
                                                     image_number=image_number,
                                                     info=json.dumps(host_info_list, sort_keys=True, indent=4))
        else:
            host_result = 'unreachable'
            Host.objects.filter(ip=str(host)).update(info=host_result)

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
                container_host = Host.objects.get(ip=str(host))
                container_create_time = data_serilazer.convert(each_container['Created'])
                container_state = each_container['State']

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
                image_id = each_image['Id'].split(":")[-1]
                image_repository = each_image['RepoTags'][0].split("/")[-1].split(":")[0]
                image_host = Host.objects.get(ip=str(host))
                image_create_time = data_serilazer.convert(each_image['Created'])
                image_size = each_image['Size']
                image_container_number = Container.objects.filter(Q(imageid=image_id) & Q(host=str(host))).count()

                if not Image.objects.filter(image_id=image_id):
                    Image.objects.create(image_id=image_id, repository=image_repository,
                                         host=image_host, create_time=image_create_time,
                                         container_number=image_container_number, size=image_size)
                else:
                    Image.objects.filter(Q(image_id=image_id) & Q(host=image_host)).update(create_time=image_create_time,
                                                                                           container_number=image_container_number,
                                                                                           size=image_size)

        elif isinstance(image_info_list, dict):
            image_result = image_info_list['message']

        # if host_result == 'success' and container_result == 'success' and image_result == 'success':
        #     result = 'success'
        # else:
        #     result = 'error'
        return host, 'ok+++'
    except Exception as e:
        Host.objects.filter(ip=str(host)).update(info='unreachable')
        return e
