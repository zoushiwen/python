#!/usr/bin/env python
import sys
import subprocess
import re
import os.path


def getIndex(host):
    regx = re.compile(r'(.+)?\[(.*)\](.*)?')
    re_host = regx.match(host)
    start_domain, host_range, end_domain = re_host.group(1), re_host.group(2), re_host.group(3)
    separator = re.search('\W+', host_range).group()
    realHost = list()
    try:
        first, end = int(host_range.split(separator)[0]),int(host_range.split(separator)[1])
    except ValueError as e:
        print(e.message)
        sys.exit(1)

    if end < first:
        print("The index value must {} greater than {}.".format(end,first))
        sys.exit(1)

    for i in range(first, end):
        if i < 10:
            resHost = start_domain + '{:0d}'.format(0) + str(i) + end_domain
        else:
            resHost = start_domain + str(i) + end_domain
        realHost.append(resHost)

    return realHost

def check_alive(ip_list, count=1, timeout=1):
    suceessFile = os.path.join(os.path.expanduser('~'), 'success_hosts')
    failFile = os.path.join(os.path.expanduser('~'), 'fail_hosts')
    success_ip,fail_ip = list(),list()
    for ip in ip_list:
        cmd = 'ping -c %d -t %d  %s' % (count, timeout, ip)

        p = subprocess.Popen(cmd,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             shell=True
                             )

        result = p.stdout.read()
        if len(result) == 0:
            print "\033[31m%s DOWN\033[0m" % (ip)
            fail_ip.append(ip + '\n')
        else:
            regex = re.findall('100.0% packet loss', result)
            if len(regex) != 0:
                print "\033[31m%s DOWN\033[0m" % (ip)
                fail_ip.append(ip + '\n')
            else:
                print "\033[32m%s UP\033[0m" % (ip)
                success_ip.append(ip + '\n')
    fileOption(suceessFile,success_ip)
    fileOption(failFile,fail_ip)


def fileOption(file,contents):
    with open(file,'w+') as f:
        for content in contents:
            f.writelines(content)

if __name__ == '__main__':

    try:
        host = sys.argv[1]
    except IndexError as e:
        print (e.message)
        sys.exit(1)

    realHost = getIndex(host)
    check_alive(realHost)







