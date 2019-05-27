### Usage

批量查看多台机器是否ping通，并把成功的机器和失败的机器分别各自文件中

> eg:查看 openstack01.zoushiwen.com 到 openstack10.zoushiwen.com 能否ping通
~~~
zoujiangtao:~$ python xre.py openstack[1-10].zoushiwen.com
openstack01.zoushiwen.com DOWN
openstack02.zoushiwen.com DOWN
openstack03.zoushiwen.com DOWN
openstack04.zoushiwen.com DOWN
openstack05.zoushiwen.com DOWN
openstack06.zoushiwen.com DOWN
openstack07.zoushiwen.com DOWN
openstack08.zoushiwen.com DOWN
openstack09.zoushiwen.com DOWN

DOWN: ping失败
UP: ping成功
~~~


#### Result

~~~
在根目录生成success_file和 fail_file两个文件

cat ~/success_hosts

zoujiangtao:~$ cat ~/fail_hosts
openstack01.zoushiwen.com
openstack02.zoushiwen.com
openstack03.zoushiwen.com
openstack04.zoushiwen.com
openstack05.zoushiwen.com
openstack06.zoushiwen.com
openstack07.zoushiwen.com
openstack08.zoushiwen.com
openstack09.zoushiwen.com

~~~
