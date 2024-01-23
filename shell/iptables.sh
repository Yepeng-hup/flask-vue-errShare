#!/bin/bash

x=$1

function save_rule() {
service iptables save >& /dev/null && systemctl restart iptables
}

function show_rule() {
    iptables -n -L INPUT --line-numbers|awk 'NR>2' > rule.txt
}

case $x in
save)
  save_rule;;
show)
  show_rule;;
*)
  echo -e "\e[31m Warning:$0 {save|show} \e[0m"
esac