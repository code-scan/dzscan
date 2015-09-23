#coding=utf-8
import re
import urllib
import threading
from sys import argv
import sys,time
import json
class scan(threading.Thread):
	def __init__(self,target,addone):
		threading.Thread.__init__(self)
		self.target=target
		self.addone=addone
	def getvulinfo(self,plugin):
		url="http://dzscan.org/index.php/welcome/view?plugin="+plugin
		json_data=urllib.urlopen(url).read()
		print json_data
		json_data=json.loads(json_data)
		print json_data
		if len(json_data)==1:
			return "http://dzscan.org/index.php/welcome/view?id="+json_data[0]['id']
		return False
	def run(self):
		global flush,scanow,click
		target=self.target
		try:
			for addone in self.addone:
				click=click+1
				add=addone.split(' ')[0]
				name=addone.split(' ')[1]
				url=target+"/plugin.php?id="+add
				data=urllib.urlopen(url).read()	
				#print data 
				scanow="[*]Scan %s "%add
				sys.stdout.write(str(scanow)+" "*20+"\b\b\r")
				sys.stdout.flush()
				if 'charset=gbk' in data:
					data=data.decode('gbk')
					data=data.encode('utf-8')
				if rule(data):
					flush=flush+"[!] Find Addon %s\n"%addone
					print "[!] Find Addon %s"%addone
					flush=flush+"[!] "+url+"\n"
					print "[!] "+url
					'''vulinfo=self.getvulinfo(add)
					if vulinfo:
						print "[!]VuL Info "+vulinfo'''
					print "\n"
		except Exception,ex:
			pass
			#print Exception,ex
def update_plugin():
	alladds=[]
	for i in range(1,169):
		url="http://addon.discuz.com/index.php?view=plugins&f_order=create&page="+str(i)
		data=urllib.urlopen(url).read()
        
		addones=re.findall(r'<img src="resource/plugin/(.*)" />',data)
		for a in addones:
			u=a.split('.png?')[0]
			ux=a.split('alt="')[1].decode('gbk').encode('utf-8')
			adds="%s %s"%(u,ux)
			alladds.append(adds)
			print adds
		print "[*]Page %d"%i
	data=""
	for x in alladds:
		data=data+x+"\n"
	open('adds.txt','w').write(data)


def rule(data):
	switch=0
	
	if '插件不存在或已关闭' not in data and len(data)>1000 and 'http://error.www.xiaomi.cn' not in data: 
		return True
	#elif '抱歉，您尚未登录，无法进行此操作' in data:
		#return True
	else:
		return False
def getinfo(url):
	try:
		version=urllib.urlopen(url+"/robots.txt").read()
		print "[!]Robots.txt is Find!"
		print "[!]"+url+"/robots.txt"
		version=version.split("#")[2]
		ver=version.split(" for ")[1]
		print "[!]Version is %s"%(ver)
	except:
		pass
def helpinfo():
	print "Discuz Plugin Scan v0.1"
	print "Usage: %s  http://dzscan.org/[bbs]/ [thread|20]"%(argv[0])
	exit()
if len(argv)==2:
	thread_num=20
elif len(argv)==3:	
	thread_num=argv[2]
else:
	helpinfo()
if argv[1]=='update':
	update_plugin()
	exit()
thread_num=int(thread_num)
target=argv[1]
getinfo(target)
alladds=open('adds.txt').read()
alladds=alladds.split("\n")
thread=len(alladds)/thread_num
th=[]
flush=''
scanow=''
click=0
for i in range(1,thread+2):
	if ((i-1)*thread)>=len(alladds):
		break
	if i==1:
		addones=alladds[0:i*thread]
	else:
		addones=alladds[(i-1)*thread:i*thread]
	
	th.append(scan(target,addones))
for t in th:
		t.start()

