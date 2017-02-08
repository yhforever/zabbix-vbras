#!/bin/bash
natPara=
smgrPara=
number=
traffic=
traffic_in=
traffic_out=
interface=$2
natshow(){
   number=`(sleep 1;echo show nat statistic;sleep 1) | sudo confd_cli --noaaa | grep $natPara | awk '{print $4}'`
if [ -n "$number" ];then
      echo $number
  else
     echo 0
  fi
}

natall(){
number=`(sleep 1;echo show nat statistic;sleep 1) | sudo confd_cli --noaaa`
if [ -n "$number" ];then
      echo $number
  else
     echo 0
  fi
}

smgrshow(){
   (sleep 1;echo show smgr-session summary;sleep 1) | sudo confd_cli --noaaa | grep $smgrPara | awk '{print $4}'
}

smgrall(){
   (sleep 1;echo show smgr-session summary;sleep 1) | sudo confd_cli --noaaa
   (sleep 1;echo show smgr-session peak;sleep 1) | sudo confd_cli --noaaa
}

traffic_in(){
  traffic=`(sleep 1;echo show interfaces-state interface "$interface";sleep 1) | sudo confd_cli --noaaa | grep in-octets | awk '{print $3}'`
  traffic_in=$[$traffic * 8]
  echo $traffic_in
}

traffic_out(){
   traffic=`(sleep 1;echo show interfaces-state interface "$interface";sleep 1) | sudo confd_cli --noaaa | grep out-octets | awk '{print $3}'`
   traffic_out=$[$traffic * 8]
   echo $traffic_out
}


   case "$1" in
    nat_totaluser)
        natPara=totalUser
        natshow
    ;;
    nat_totalsess)
        natPara=totalSess
        natshow
    ;;
    smgr_ipoesess)
        smgrPara=ipoe
        smgrshow
    ;;
    smgr_pppoesess)
        smgrPara=pppoe
        smgrshow
    ;;
    smgr_iphostsess)
        smgrPara=iphost
        smgrshow
    ;;
    traffic_in)
        traffic_in
    ;;
    traffic_out)
        traffic_out
    ;;
    all)
       natall
       smgrall
     
     
esac
