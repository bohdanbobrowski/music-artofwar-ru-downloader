#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
from os.path import expanduser
import re
import sys
import urllib
import urllib2

response = urllib2.urlopen('http://music.artofwar.ru/')
html = response.read()

mp3s = re.findall('href="([^"]*).mp3"',html)
for mp3 in mp3s:
    directory = './'
    url = 'http://music.artofwar.ru/'+mp3+'.mp3'
    if mp3.find('/') > -1:
        mp3 = mp3.split('/',1)
        directory = './'+mp3[0]+'/'
        if not os.path.exists(directory):
            os.makedirs(directory)
        mp3 = mp3[1]
        mp3 = mp3.replace('/','_')
    file_name = directory+mp3+'.mp3'
    if(os.path.isfile(file_name)):
        print 'Omitting: '+url
    else:
        try:
            u = urllib2.urlopen(url)
            f = open(file_name, 'wb')
            meta = u.info()
            file_size = int(meta.getheaders("Content-Length")[0])
            print("Downloading: {0} Size: {1}".format(url, file_size))            
            file_size_dl = 0
            block_sz = 8192
            while True:
                buffer = u.read(block_sz)
                if not buffer:
                    break
                file_size_dl += len(buffer)
                f.write(buffer)
                p = float(file_size_dl) / file_size
                status = r"{0}  [{1:.2%}]".format(file_size_dl, p)
                status = status + chr(8)*(len(status)+1)                
                sys.stdout.write(status)
            f.close()
        except urllib2.HTTPError as e:
            print(e.code)
            print(e.read())    
