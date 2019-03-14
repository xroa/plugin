#! /usr/bin/env python
# -*- coding: utf-8 -*-

import time, os, socket
import json,platform

metric = ['usr', 'nice', 'sys', 'idle', 'iowait', 'irq', 'soft', 'steal', 'guest']
host = socket.gethostname()
sysType, sysVer, scode = platform.dist()

def get_cpu_core_stat(num):
  data = []
  for x in range(num):
    try:
      handler = os.popen("cat /proc/stat | grep cpu%d " % x)
    except Exception,e:
      continue

    output = handler.read().strip().split()[1:]
    print output

    argLen = 8
    if sysType == 'centos' and float(sysVer[0:2]) < 7.0:
        argLen = 9
    if len(output) != argLen:
      continue

    index=0
    for m in output:
      t = {}
      t['metric'] = 'cpu.core.%s' % metric[index]
      t['endpoint'] = host
      t['timestamp'] = int(time.time())
      t['step'] = 60
      t['counterType'] = 'COUNTER'
      t['tags'] = 'core=%s' % str(x)
      t['value'] = m
      index += 1
      data.append(t)

  return data

if __name__ == "__main__":
  core_total = int(os.popen("cat /proc/cpuinfo | grep processor | tail -1 | cut -d' ' -f2").read().strip()) + 1
  print json.dumps(get_cpu_core_stat(core_total))
