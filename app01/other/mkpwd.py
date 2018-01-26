#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import crypt

from app01.models import Host


def write(pwd, ip):
    salt = crypt.prpcrypt('ta$8i2^)f4g$vp879j*a0&bl*8w1o3lv8!1klt+j')
    pwd_write = salt.encrypt(pwd)
    Host.objects.filter(ip=ip).update(pwd=pwd_write)


def read(pwd_write):
    salt = crypt.prpcrypt('ta$8i2^)f4g$vp879j*a0&bl*8w1o3lv8!1klt+j')
    pwd_read = salt.decrypt(pwd_write)

    return pwd_read

if __name__ == '__main__':
    print 'Only Run By Import'
