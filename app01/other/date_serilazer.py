# _*_ coding: utf-8 _*_

import datetime
import time

def convert(request, local_time):
    print local_time
    old_time = time.localtime(local_time)
    new_time = time.strftime('%Y-%m-%d %H:%M:%S', old_time)
    # update_time = datetime.datetime.strptime(new_time, '%Y-%m-%d %H:%M:%S')

    print new_time

    return new_time

if __name__ == '__main__':
    print 'Only Run By Import'