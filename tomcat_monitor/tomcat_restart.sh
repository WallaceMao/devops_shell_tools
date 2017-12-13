#/bin/bash
# kill tomcat process
serverid=`ps -ef|grep apache-tomcat-7.0.82-ding-main|grep -v grep|awk '{print $2}'`
if [ "$serverid" != "" ]; then
  kill -9 $serverid
fi
sleep 5
cd /usr/local/apache-tomcat-7.0.82-ding-main/bin
bash startup.sh
