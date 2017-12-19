# _*_ coding: utf-8 _*_

from __future__ import unicode_literals
from datetime import datetime

from django.db import models


# Create your models here.


class Container(models.Model):
    container_id = models.CharField(max_length=100, null=False, blank=False, verbose_name=u'ID')
    name = models.CharField(max_length=50, null=False, blank=False, verbose_name=u'容器名')
    # imagename = models.ForeignKey('Image', to_field='repository', null=True, blank=True, verbose_name=u'所属镜像', db_column='image_name', related_name='image_name')
    # imageid = models.F.ForeignKey('Image', to_field='repository', null=True, blank=True, verbose_name=u'所属镜像', db_column='image_name', related_name='image_name')
    imagename = models.CharField(max_length=20, null=False, blank=False, verbose_name=u'所属镜像', db_column='image_name')
    imageid = models.CharField(max_length=100, null=False, blank=False, verbose_name=u'所属镜像ID', db_column='image_id')
    host = models.ForeignKey('Host', to_field='ip', verbose_name=u'所属宿主机')
    create_time = models.DateTimeField(default=datetime.now, verbose_name=u'创建时间')
    state = models.CharField(max_length=10, null=False, blank=False, verbose_name=u'状态')

    class Meta:
        verbose_name = u'容器列表'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class Image(models.Model):
    image_id = models.CharField(max_length=100, unique=True, null=False, blank=False, verbose_name=u'ID')
    repository = models.CharField(max_length=50,  unique=True, null=False, blank=False, verbose_name=u'仓库镜像')
    host = models.ForeignKey('Host', to_field='ip', on_delete=models.CASCADE, verbose_name=u'所属宿主机')
    create_time = models.DateTimeField(default=datetime.now, verbose_name=u'创建时间')
    container_number = models.IntegerField(verbose_name=u'容器数量')
    size = models.CharField(max_length=100, null=False, blank=False, verbose_name=u'镜像大小')

    class Meta:
        verbose_name = u'镜像列表'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.repository


class Host(models.Model):
    ip = models.GenericIPAddressField(protocol='ipv4', unique=True, null=False, blank=False, verbose_name=u'IP地址')
    container_number = models.IntegerField(verbose_name=u'容器数量')
    image_number = models.IntegerField(verbose_name=u'镜像数量')
    info = models.TextField(null=False, blank=False, verbose_name=u'宿主机状态')

    class Meta:
        verbose_name = u'宿主机列表'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.ip
