#/bin/bash
# kill  process
serverid=`ps -ef|grep health_check.py|grep -v grep|awk '{print $2}'`
if [ "$serverid" != "" ]; then
  kill -9 $serverid
fi

