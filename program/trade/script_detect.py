#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-10-17 21:55:41
# @Author  : Michael (mishchael@gmail.com)

#!/usr/bin/python
# -*- coding:utf-8 -*-
import subprocess,time,sys
from datetime import datetime

TIME = 180                    #程序状态检测间隔（单位：分钟）
CMD = script_path = 'python ../trade/bfx_main.py'                #需要执行程序的绝对路径，支持jar 如：D:\\calc.exe 或者D:\\test.jar


class Auto_Run():
    def __init__(self,sleep_time,cmd):
        self.sleep_time = sleep_time
        self.cmd = cmd
        self.ext = (cmd[-3:]).lower()        #判断文件的后缀名，全部换成小写
        self.p = None                        #self.p为subprocess.Popen()的返回值，初始化为None
        self.run()                           #启动时先执行一次程序

        try:
            while 1:
                time.sleep(sleep_time)  #休息10分钟，判断程序状态
                self.poll = self.p.poll()    #判断程序进程是否存在，None：表示程序正在运行 其他值：表示程序已退出
                if self.poll is None:
                    print("运行正常")
                else:
                    print("未检测到程序运行状态，准备启动程序")
                    self.run()
        except KeyboardInterrupt as e:
            print("检测到CTRL+C，准备退出程序!")
#            self.p.kill()                   #检测到CTRL+C时，kill掉CMD中启动的exe或者jar程序

    def run(self):
        if self.ext == ".py":
            print('start OK!')
            # 记录运行日志
            nohup_log_path = '../logs/nohup/EOS_USDT_' + str(datetime.now().timestamp()) +'.log'
            self.cmd = 'python -u ../trade/bfx_main.py > ' + nohup_log_path + ' 2>&1 &'
            print(self.cmd)
            self.p = subprocess.Popen(self.cmd, stdin = sys.stdin,stdout = sys.stdout, stderr = sys.stderr, shell = True)
            # self.p = subprocess.Popen(['nohup', 'python', '-u ','%s' % self.cmd, '>', nohup_log_path, '2>&1', '&'], stdin = sys.stdin,stdout = sys.stdout, stderr = sys.stderr, shell = False)
            # self.p = subprocess.Popen(['python', '%s' % self.cmd], stdin = sys.stdin,stdout = sys.stdout, stderr = sys.stderr, shell = False)
            # bufsize: 1 means line buffered (only usable if universal_newlines=True i.e., in a text mode)
            # self.p = subprocess.Popen(['python', '%s' % self.cmd], stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE, bufsize = 1 , universal_newlines = True, shell = False)
            # print('1')
            # try:
            #     while True:
            #         line = self.p.stdout.readline()
            #         print(2)
            #         print(line)
            #         if line:
            #             print('3')
            #             with open(log_path, mode = 'a') as log:
            #                 log.write(line)
            #         else:
            #             print("no data")
            #         time.sleep(2)

            # except KeyboardInterrupt:
            #     print("Killing child...")
            #     kill(self.p.pid, signal.SIGTERM)

            # for line in iter(self.p.stdout.readline, b''):
            #     with open(log_path, mode = 'w') as log:
            #     for line in lines:
            #         log.write(line)
            # p.stdout.close()
            # p.wait()
            
        else:
            pass
app = Auto_Run(TIME,CMD)
