#!/bin/bash
route_number=0
neighbor_status=0
proto=
protocmd=
isiscmd="show clns is-neighbors"
ospfcmd="show ip ospf neighbor"
bgpcmd="show ip bgp summary"

show_route(){
   route_number=`sudo /usr/bin/env TERM=xterm /usr/bin/imish -e 'show ip route summary' | grep $proto | awk '{print $2}'`
   if [ -n "$route_number" ];then
      echo $route_number
    else 
     echo 0
   fi
}

show_bgpneighbor(){
   neighbor_up_number=`sudo /usr/bin/env TERM=xterm /usr/bin/imish -e "$protocmd" | grep Established | awk '{print $6}' `
   echo $neighbor_up_number
}  

show_ospfneighbor(){
   neighbor_up_number=`sudo /usr/bin/env TERM=xterm /usr/bin/imish -e "$protocmd" | grep Total | awk '{print $6}'`
     echo $neighbor_up_number
}  

show_isisneighbor(){
   neighbor_status=`sudo /usr/bin/env TERM=xterm /usr/bin/imish -e "$protocmd" | grep Up| wc -l `
   echo $neighbor_status
}


case "$1" in
    bgp_route)
         proto=bgp
         show_route
    ;;
    ospf_route)
         proto=ospf
         show_route
    ;;
    isis_route)
         proto=isis
         show_route
    ;;
    static_route)
         proto=static
         show_route
    ;;
    isis_neighbor)
         protocmd=$isiscmd
         show_isisneighbor
    ;;
    ospf_neighbor)
         protocmd=$ospfcmd
         show_ospfneighbor
    ;;
    bgp_neighbor)
         protocmd=$bgpcmd
         show_bgpneighbor
    ;;
esac
