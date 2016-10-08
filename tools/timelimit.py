#!/usr/bin/env python
# encoding: utf-8

import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import signal,functools

class TimeoutError(Exception):pass

#单线程时间控制
def timeout(seconds,error_message="Timeout Error: this page run time out!"):
    def decorated(func):
        result=""

        def _handle_timeout(signum,frame):
            global result
            result=error_message
            raise TimeoutError(error_message)

        def wrapper(*args,**kwargs):
            global result
            signal.signal(signal.SIGALRM,_handle_timeout)
            signal.alarm(seconds)

            try:
                result=func(*args,**kwargs)
            finally:
                signal.alarm(0)
                return result
            return result
        return functools.wraps(func)(wrapper)
    return decorated

@timeout(5)
def slowfunc(sleep_time):
    while 1:
        time.sleep(sleep_time)
        print "hello"

def foo():
    try:
        slowfunc(1)
    except TimeoutError:
        print "time out !!"
    while True:
        print "111"
        time.sleep(1)

foo()