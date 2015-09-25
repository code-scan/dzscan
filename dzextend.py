#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
import re

class dzextend:
    def Request_Get(self,target):
        try:
            req=requests.get(target)
            respone=req.content
            if 'charset=gbk' in req.content:
                respone=respone.decode('gbk').encode('utf8')
            return respone
        except:
            return ''
    #遍历管理员账号
    def GetAdminId(self,target,start=1,stop=20):
        adminlist=[]
        username=r'<meta name="description" content="(.*?)" />'
        group=r'amp;gid=(.*)" target="_blank">'
        for id in range(start,stop):
            #print id
            url=target+"/home.php?mod=space&uid=%d"%id
            respone=self.Request_Get(url)
            try:
                username_find=re.findall(username,respone)[0]
                group_find=re.findall(group,respone)[0]
                if '" target=' in group:
                    group_find=group_find.split('" target=')[0]
                if int(group_find)==1:
                    admin=username_find.split("的个人资料")[0]
                    adminlist.append(admin)
            except:
                pass
        return adminlist
    #抓取首页的插件
    def GetIndexPlugin(self,target):
        respone=self.Request_Get(target)
        plugin_finds=[]
        plugin=r'<a href="plugin.php\?id=(.*?)" hidefocus="true"'
        plugin_find=re.findall(plugin,respone)
        for p in plugin_find:
            if ':' in p:
                p=p.split(":")[0]
            plugin_finds.append(p)
        return set(plugin_finds)
