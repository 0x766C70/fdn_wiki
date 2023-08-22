#!/bin/sh

# @uthor belette
# version v.1.0

if [ "$3" = "CRITICAL" ] && [ "$4" = "HARD" ]; then
  cd /usr/lib/nagios/plugins/cagios
  /bin/echo "$(date)" "$1" "$2" "$3" "$4" >> ircbot_cachet.log
  ./cagios.py -d -u "$1" "$2" "4" "$3" "$4"
  /bin/echo $1 $2 $3 > ircpipe &
elif [ "$3" = "OK" ] && [ "$4" = "HARD" ]; then
  cd /usr/lib/nagios/plugins/cagios
  /bin/echo "$(date)" "$1" "$2" "$3" "$4" >> ircbot_cachet.log
  ./cagios.py -d -u "$1" "$2" "1" "$3" "$4"
  /bin/echo $1 $2 $3 > ircpipe &
fi
