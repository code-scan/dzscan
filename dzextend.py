#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
import re
import random
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
    #创始人登录
    def LoginFounder(self,target,password,path='/uc_server/'):
        url="%s/%s/index.php?m=app&a=add"%(target,path)      
        ip=str(random.randint(1,255))+"."+str(random.randint(1,255))+"."+str(random.randint(1,255))+"."+str(random.randint(1,255))
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0","X-Forwarded-For":ip,'Content-Type':'application/x-www-form-urlencoded','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Connection':'keep-alive'}

        data=requests.post(url,data={'ucfounderpw':password},headers=headers)
        #fail return -1 
        #success return database connect info
        return data.content
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
        plugin=[r'plugin.php\?id=(.*)\&',r'src="plugin.php\?id=(.*)"','href="plugin.php\?id=(.*)"']
        for p in plugin:
            plugin_find=re.findall(p,respone)
            for p in plugin_find:
                if ':' in p:
                    p=p.split(":")[0]
                plugin_finds.append(p)
        return set(plugin_finds)
