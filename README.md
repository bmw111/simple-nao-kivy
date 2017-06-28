# simple-nao-kivy
simple nao control with socket kivy
请尊重分享成果，转载请注明出处，本文来自这名字取得好,原文链接： 
[http://www.jianshu.com/p/8a5d968afc7f](http://www.jianshu.com/p/8a5d968afc7f)

环境：
Centos 7.2 64位 
Python 2.7.12 64位

在百度上可以找到好几种Linux开机启动各种服务的方法,在这里我写的是我找到的感觉比较适合自己这样记性比较差的使用的，新建一个脚本放在自己能找到的目录,只用在系统的目录下配置一次,以后就在自己新建的脚本里面写启动服务的命令就好。

1. 自己新建一个脚本,如centnet-service.sh
-------------------------------
经过后面的几个步骤后,这个脚本在开机的时候会执行,在这个脚本里面可以写你开机的时候想执行的命令,如启动python等服务

2. 在脚本中输入启动服务的命令,如(开机启动python 服务端):
-------------------------------

```
#!/bin/bash
python /home/usr/bin/server.py 
```
or 

```
#!/bin/bash
export JDK_HOME=/home/java/jdk1.8.0_91
export JAVA_HOME=/home/java/jdk1.8.0_91
/home/tomcat/apache-tomcat-8.0.36/bin/startup.sh
```

3. 执行如下命令,将该脚本标记为可执行文件(添加可执行的权限)
--------------------------------

```
chmod +x /home/centnet/centnet-service.sh
```

4. 执行如下命令将/etc/rc.d/rc.local文标记为可执行文件
-------------------------------------
在centos7中,/etc/rc.d/rc.local文件的权限被降低了,开机的时候执行在自己的脚本是不能起动一些服务的,执行下面的命令可以文件标记为可执行的文件

```
chmod +x /etc/rc.d/rc.local
```

5. 打开/etc/rc.d/rc.local文件,在最后面添加如下脚本
------------------------------------

```
/home/centnet/centnet-service.sh
```

这样,centnet-service.sh这个脚本在开机的时候就会被执行了,以后再这里面写启动服务的命令就可以了.
