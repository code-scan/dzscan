#!/usr/bin/env python
# -*- coding:utf-8 -*-

from gevent import monkey; monkey.patch_all()
from string import strip
from urlparse import urljoin
from Queue import Queue, Empty

import datetime
import json, gevent
import re, sys, time
import argparse, requests

USAGE = './dzscan.py [options]'


def parseCmd():
    """
    @cmdline parser
    """

    parser = argparse.ArgumentParser(usage=USAGE, formatter_class=argparse.RawTextHelpFormatter, add_help=False)

    parser.add_argument('-u', '--url', dest='url',
                        help='The Discuz! URL/domain to scan.')

    parser.add_argument('--gevent', dest='gevent', metavar='<number of gevent>',
                        help='The number of gevents to use when multi-requests')

    parser.add_argument('-f', '--force', dest='force', action='store_true', default=False,
                        help='Forces DzScan to not check if the remote site is running Discuz!')

    parser.add_argument('-h', '--help', action='help', 
                        help='Show help message and exit.')

    parser.add_argument('-v', '--verbose', action='store_true',
                        default=False, help='Show verbose message during scaning')

    parser.add_argument('--update', dest='update', action='store_true', default=False,
                        help='Update database to the latests version.')

    parser.add_argument('--log', dest='log', action='store_true', default=False,
                        help='Record scan output in .log file')

    args = parser.parse_args()
    return args.__dict__


def banner():
    """
    @dzscan banner
    """
    str = """_______________________________________________________________

    ██████╗ ███████╗███████╗ ██████╗ █████╗ ███╗   ██╗
    ██╔══██╗╚══███╔╝██╔════╝██╔════╝██╔══██╗████╗  ██║
    ██║  ██║  ███╔╝ ███████╗██║     ███████║██╔██╗ ██║
    ██║  ██║ ███╔╝  ╚════██║██║     ██╔══██║██║╚██╗██║
    ██████╔╝███████╗███████║╚██████╗██║  ██║██║ ╚████║
    ╚═════╝ ╚══════╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝
    Dizscan! Security Scanner by the DzScan Team
    Version 0.2
    http://dzscan.org wyc@Dzscan
_______________________________________________________________
    """
    print str


class DzscanBase():

    def __init__(self, argsDic):
        self.plugin_pages = 3
        self.addonTol = set()
        self.url = argsDic['url'] or 'http://www.discuz.net'
        self.addon_path = '%s?id=' % urljoin(self.url, '/plugin.php')
        self.queue = Queue()
        self.gevents = argsDic['gevent'] or 10
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
        robots_path = urljoin(self.url, '/robots.txt')
        req = requests.get(robots_path)
        self.reqs += 1
        if req.status_code == 200:
            print '[!] The Discuz! \'%s\' file exists .\n' % robots_path
            ver = req.content.split('#')[2].split(' for ')[1]
            print '[+] Discuz! version \'%s\' .\n\n' % strip(ver)

        robots_path = urljoin(self.url, '/source/plugin/tools/tools.php')
        req = requests.get(robots_path)
        self.reqs += 1
        if req.status_code == 200:
            print '[!] The Discuz! \'%s\' file exists.\n' % robots_path       

        #/utility/convert/index.php?a=config&source=d7.2_x2.0 
        robots_path = urljoin(self.url, '/utility/convert/index.php?a=config&source=d7.2_x2.0')
        req = requests.get(robots_path)
        self.reqs += 1
        if req.status_code == 200:
            print '[!] The Discuz! \'%s\' file exists.\n' % robots_path   

        #develop.php
        robots_path = urljoin(self.url, '/develop.php')
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
                # self.count += 1
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


def examine(content):
    if '插件不存在或已关闭' not in content and len(content) > 1000 \
            and 'http://error.www.xiaomi.cn' not in content:
        return True
    return False


def fetch_vul(addon):
    fetch_url = 'http://dzscan.org/index.php/welcome/view?plugin=%s' % addon
    json_data = json.loads(requests.get(fetch_url).content)
    for vul in json_data:
        return "http://dzscan.org/index.php/welcome/view?id=%s" % vul['id']


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
