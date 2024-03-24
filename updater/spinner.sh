#!/bin/bash
# Clear Line
CL="\e[2K"
# Spinner Character
SPINNER=(▰▱▱▱▱▱▱ ▰▰▱▱▱▱▱ ▰▰▰▱▱▱▱ ▱▰▰▰▱▱▱ ▱▱▰▰▰▱▱ ▱▱▱▰▰▰▱ ▱▱▱▱▰▰▰ ▱▱▱▱▱▰▰ ▱▱▱▱▱▱▰ ▱▱▱▱▱▱▱ ▱▱▱▱▱▱▱ ▱▱▱▱▱▱▱ ▱▱▱▱▱▱▱)
LEN=${#SPINNER}
function spinner() {
  delay="${2:-0.01}"
  msg=$1
  start_time=$SECONDS
  i=0
  while :; do
    jobs %1 > /dev/null 2>&1
    [ $? = 0 ] || {
      elapsed=$((SECONDS - start_time))
      printf "${CL}✓ ${msg} : done in ${elapsed} seconds.\n"
      break
    }
    printf "${CL}${msg} ${SPINNER[$i%($LEN+5)]} \r"
    i=$((i+1))
    sleep $delay
  done
}
