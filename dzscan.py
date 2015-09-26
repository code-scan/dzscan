#!/usr/bin/env python
# -*- coding:utf-8 -*-

from gevent import monkey; monkey.patch_all()
from string import strip
from Queue import Queue, Empty

from utils import examine, banner
from utils import USAGE, parseCmd

import datetime
import re, sys, time
import gevent, requests


class DzscanBase():

    def __init__(self, argsDic):
        self.plugin_pages = 3
        self.addonTol = set()
        self.url = argsDic['url'] or 'http://www.discuz.net'
        self.addon_path = '%s/%s?id=' % (self.url, '/plugin.php')
        self.queue = Queue()
        self.gevents = int(argsDic['gevent']) if argsDic['gevent'] else 10
        self.pool = []
        self.ctn = True
        self.verbose = argsDic['verbose']
        self.reqs = 0
        self.outs = 0
        self.log = argsDic['log']

    def update(self):
        print '[i] Updateing Database ...'
        fetch_url = 'http://addon.discuz.com/index.php?view=plugins&f_order=create&page=%s'
        pattern = re.compile(r'<img src="resource/plugin/(.*)"')

        for page in xrange(1, self.plugin_pages + 1):
            req = requests.get(fetch_url % page)
            self.reqs += 1
            addons = pattern.findall(req.content)

            for addon in addons:
                self.addonTol.add((addon.split('.png?')[0],
                    addon.split('alt="')[1].decode('gbk').encode('utf8')))
            print 'page %s' % page

        with open('adds.txt', 'w') as fp:
            for add in self.addonTol:
                fp.write('%s, %s\n' % add)

    def fetch_version(self):
        robots_path = '%s/%s' % (self.url, '/robots.txt')
        req = requests.get(robots_path)
        self.reqs += 1
        if req.status_code == 200:
            print '[!] The Discuz! \'%s\' file exists .\n' % robots_path
            try:
                ver = req.content.split('#')[2].split(' for ')[1]
                print '[+] Discuz! version \'%s\' .\n\n' % strip(ver)
            except IndexError:
                print '[!] But seems no version revealed'

        robots_path = '%s/%s' % (self.url, '/source/plugin/tools/tools.php')
        req = requests.get(robots_path)
        self.reqs += 1
        if req.status_code == 200:
            print '[!] The Discuz! \'%s\' file exists.\n' % robots_path       

        #/utility/convert/index.php?a=config&source=d7.2_x2.0 
        robots_path = '%s/%s' % (self.url, '/utility/convert/index.php?a=config&source=d7.2_x2.0')
        req = requests.get(robots_path)
        self.reqs += 1
        if req.status_code == 200:
            print '[!] The Discuz! \'%s\' file exists.\n' % robots_path   

        #develop.php
        robots_path = '%s/%s' % (self.url, '/develop.php')
        req = requests.get(robots_path)
        self.reqs += 1
        if req.status_code == 200:
            print '[!] The Discuz! \'%s\' file exists.\n' % robots_path  

    def stdout(self, name):
        scanow = '[*] scan addon \'%s\' for exisitance... ' % name
        sys.stdout.write(str(scanow)+" "*20+"\b\b\r")
        sys.stdout.flush()
    
    def fetch_addons(self):
        while self.ctn:
            try:
                addon_name = self.queue.get_nowait()               
                self.stdout(addon_name)
                self.exist_examine(addon_name)
            except Empty:
                self.ctn = False

    def init_addon(self):
        self.addonTol = set()
        with open('adds.txt') as fp:
            for line in fp.readlines():
                self.addonTol.add((line.split(',')[0], line.split(',')[1]))
                self.queue.put(line.split(',')[0])

    def execute(self):
        for event in xrange(self.gevents):
            self.pool.append(gevent.spawn(self.fetch_addons))
        gevent.joinall(self.pool)

    def exist_examine(self, addon_name):
        examine_url = '{}{}'.format(self.addon_path, addon_name)
        if self.verbose:
            print '[*] scan addon \'%s\' for exisitance... ' % addon_name
        try:    
            req = requests.get(examine_url)
            self.reqs += 1
            if 'charset=gbk' in req.content:
                exist = examine(req.content.decode('gbk').encode('utf8'))
            else:
                exist = examine(req.content)

            if exist:
                sucMsg = '\n[!] Find addon \'{}\' : \'{}\' !'.format(addon_name, examine_url)
                print sucMsg
                self.outs += 1
        except Exception as ex:
            print ex


if __name__ == "__main__":
    start_time = datetime.datetime.now()
    banner()
    cmdArgs = parseCmd()

    base = DzscanBase(cmdArgs)
    # {'url': None, 'force': False, 'gevents': 10, 'update': True, 'verbose': False, 'log': False}

    if cmdArgs['update']:
        base.update()

    elif cmdArgs['url'] == None:
        print "usage: ./dzscan.py --help"

    else:
        base.fetch_version()
        print '[+] Enumerating plugins from passive detection ...'
        base.init_addon()
        base.execute()

    if not base.log:
        pointer = sys.stdout
    else:
        from urlparse import urlsplit
        log_name = urlsplit(base.url)[1].replace('.', '_')
        pointer = open('%s.log' % log_name, 'a')

    pointer.write('[+] %s plugins found.                            \n' % (base.outs or 'No'))
    pointer.write('[+] Finished: %s.\n' % time.ctime())
    pointer.write('[+] Requests Done: %s.\n' % base.reqs)
    sec = (datetime.datetime.now() - start_time).seconds
    pointer.write('[+] Elapsed time: {}:{}:{}.\n'.format(sec / 3600, sec % 3600 / 60, sec % 60))

    pointer.close()
