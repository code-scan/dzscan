# dzscan


##新版本刚发布 可能存在一些bug，正在修复中,若有问题请提交[issue](https://github.com/code-scan/dzscan/issues)带上图是最好不过辣
*关注的人们啊, 被关注不是目的, 要来贡献代码或者反馈bug哦(●'◡'●)ﾉ♥*

依赖：
需要安装 gevent
```
pip install gevent
```
windows需要安装vcforpython2.7

想做这个项目的时候大概在半年前左右，当时写了扫描器的第一版bug多多，虽然至今半年过去了仍没太多的变化，已知的bug就是线程会假死，自定义错误页面会存在预报等等,而且说实在的程序很烂，勉强能跑…

本来的打算是等我的漏洞库存够一百个漏洞就公开项目的，但是看到已经有人发布了类似的小玩意我就觉得没必要藏着掖着了，不如拿出来大家一起维护提意见。 

首先是漏洞裤首页http://dzscan.org/ ，因为这里的漏洞全部都是团队成员或者自己独立发现的，所以现在其实并没有多少漏洞，因为一直没有太多的时间去专心的挖漏洞，希望大家知道什么漏洞可以告知我一份，感谢。 
codescan@yeah.net  若有朋友有兴趣一起长期做下去也可以联系我。 

这里感谢dzscan团队成员的支持 @sin @range  @ra0mb1er @ca1n @b 这里也欢迎更多的朋友加入我们。 

程序下载地址:https://github.com/code-scan/dzscan 

如果adds.txt在linux下存在乱码的问题请执行 

```
iconv -f gb2312  -t utf-8 adds.txt > adds.txt
```

使用方法： 
```
dzscan.py -u  http://dzscan.org/ --gevent 20
dzscan.py --update
```
