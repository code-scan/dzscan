# dzscan

##新版本刚发布 可能存在一些bug，正在修复中,若有问题请提交[issue](https://github.com/code-scan/dzscan/issues)带上图是最好不过辣
**关注的人们啊, 被关注不是目的, 要来贡献代码或者反馈bug哦(●'◡'●)ﾉ♥**
##扫描的漏洞路径如下:
- deafult admin & uc_server login page
- develop.php
- X3
 - [X3 tools/tools.php  ~ Deafult password 188281MWWxjk](https://www.bugscan.net/#!/n/449)
 - [X3.1 utility/convert/index.php ~ Remote code execute](https://www.sebug.net/vuldb/ssvid-61217)
- 6.x
 - [6.x my.php ~ SQL ](http://www.wooyun.org/bugs/wooyun-2014-080359)
- 7.x
 - [7.2 faq.php ~ SQL](https://www.bugscan.net/#!/n/118)
 - [7.2 manyou/userapp.php ~ SQL](http://www.venustech.com.cn/NewsInfo/124/6791.Html)
 - [7.2 admincp.php ~ XSS](https://www.bugscan.net/#!/n/141)

#安装与使用方法
漏洞库首页 [Dzscan](http://dzscan.org/)
##windows
windows 需要安装VCForPython2.7

下载地址
```
http://download.microsoft.com/download/7/9/6/796EF2E4-801B-4FC4-AB28-B59FBF6D907B/VCForPython27.msi
```
然后切打开cmd，执行,其中需要把路径改成你python安装的所在路径
```
c:
cd C:\Python27\Scripts
easy_install pip
pip install gevent
```
##linux
linux就很简单，只需要执行
```
easy_install pip
pip install gevent
```

#使用方法
```
python dzscan.py --update //更新插件列表（目前已是最新无需更新）
python dzscan.py -u http://bbs.dzscan.org/ --gevent 20 //20是线程数量，可以自定义
```


想做这个项目的时候大概在半年前左右，当时写了扫描器的第一版bug多多，虽然至今半年过去了仍没太多的变化，已知的bug就是线程会假死，自定义错误页面会存在预报等等,而且说实在的程序很烂，勉强能跑…

本来的打算是等我的漏洞库存够一百个漏洞就公开项目的，但是看到已经有人发布了类似的小玩意我就觉得没必要藏着掖着了，不如拿出来大家一起维护提意见。 

首先是漏洞裤首页 http://dzscan.org/ ，因为这里的漏洞全部都是团队成员或者自己独立发现的，所以现在其实并没有多少漏洞，因为一直没有太多的时间去专心的挖漏洞，希望大家知道什么漏洞可以告知我一份，感谢。 
codescan@yeah.net  若有朋友有兴趣一起长期做下去也可以联系我。 

这里感谢dzscan团队成员的支持 @sin @range  @ra0mb1er @ca1n @b 这里也欢迎更多的朋友加入我们。 


