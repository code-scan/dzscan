#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import argparse, json
from random import randint


USAGE = './dzscan.py [options]'


HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",
            "X-Forwarded-For": '%s:%s:%s:%s' % (randint(1, 255),
                randint(1, 255), randint(1, 255), randint(1, 255)),
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Connection': 'keep-alive'}


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
