#!/usr/bin/env python
# -*- coding:utf-8 -*-

from gevent import monkey; monkey.patch_all()
from string import strip
from urlparse import urljoin
from Queue import Queue, Empty

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

    parser.add_argument('--update', dest='update', action='store_true', default=False,
                        help='Update database to the latests version.')

    parser.add_argument('-v', '--verbose', action='store_true',
                        default=False, help='Show verbose message during scaning')

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
    http://dzscan.org @Cond0r
_______________________________________________________________
    """
    print str


class DzscanBase():

    def __init__(self, argsDic):
        self.plugin_pages = 169
        self.addonTol = set()
        self.url = argsDic['url'] or 'http://www.discuz.net'
        self.addon_path = '%s?id=' % urljoin(self.url, '/plugin.php')
        self.queue = Queue()
        self.gevents = argsDic['gevent'] or 10
        self.pool = []
        self.count = 0
        self.ctn = True
        self.verbose = argsDic['verbose']

    def update(self):
        print '[i] Updateing Database ...'
        fetch_url = 'http://addon.discuz.com/index.php?view=plugins&f_order=create&page=%s'
        pattern = re.compile(r'<img src="resource/plugin/(.*)"')

        for page in xrange(1, 2):
            req = requests.get(fetch_url % page)
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
        if req.status_code == 200:
            print '[!] The Discuz! \'%s\' file exists exposing a version number.' % robots_path
            ver = req.content.split('#')[2].split(' for ')[1]
            print '[+] Discuz! version \'%s\' identified from fingerprinting.' % strip(ver)

    def fetch_addons(self):
        while self.ctn:
            try:
                addon_name = self.queue.get_nowait()
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
        req = requests.get(examine_url)
        if 'charset=gbk' in req.content:
            exist = rule(req.content.decode('gbk').encode('utf8'))
        else:
            exist = rule(req.content)

        if exist:
            sucMsg = '\n[!] Find addon \'{}\' : \'{}\' !\n'.format(addon_name, examine_url)
            print sucMsg


def rule(content):
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
    banner()
    cmdArgs = parseCmd()

    base = DzscanBase(cmdArgs)
    # {'url': None, 'force': False, 'update': True, 'verbose': False}

    if cmdArgs['update']:
        base.update()
    else:
        # fetch_vul('cnqn_rollad')
        base.fetch_version()
        base.init_addon()
        base.execute()
