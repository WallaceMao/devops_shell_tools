#coding=utf-8
import subprocess
import time
import logging
import requests

# 对tomcat应用进行健康检查，连续三次健康url检查失败，则执行重启操作

# global variables
# log日志文件所在的位置
log_file = './app_check.log'
# 健康度检查的url
check_url = 'http://localhost:8080/main/checkpreload.htm'
#check_url = 'http://localhost:8080/task/login/authAjax'
# 最大重试次数，当健康度检查的url连续不成功达到最大重试次数时，执行重启等操作
retry_times = 3
# 每次健康度检查之间的间隔
delay_sec = 5
# 服务重启后，重新开始健康度检查的时间间隔
delay_sec_restart = 60
# http请求的超时时间，请求响应的时长超过该事件，即认定健康度检查失败
timeout = 1

# basic config
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
#logging.basicConfig(filename=log_file, level=logging.INFO)
fail_times = 0 

# monitor script
while 1:
  hasError = False
  r = None 
  try:
    logging.debug('health checking: ' + check_url)
    r = requests.get(check_url, timeout=timeout)
    if r.status_code != 200:
      logging.warning('request is not 200: %d' % (r.status_code))
      hasError = True
  except requests.exceptions.RequestException as e: 
    logging.warning(e)
    hasError = True 
  
  if hasError:
    logging.debug('check url error: ' +  check_url)
    fail_times += 1
    if fail_times >= retry_times:
      logging.error('reach max try times, trying to restart application...')
      # restart server
      logging.debug('trying to restart server')
      resp = subprocess.call(['bash', 'tomcat_restart.sh'])
      logging.info('=================')
      logging.debug('command response after restart server: %s' % resp)
      fail_times = 0
      time.sleep(delay_sec_restart) 
    else:
      logging.debug('not reach max retry times, try again later...')
      time.sleep(delay_sec)
  else:
    logging.debug('check url success:' + check_url)
    fail_times = 0
    time.sleep(delay_sec)
