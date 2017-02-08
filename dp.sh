nat_um=
(sleep 1
echo Debug123456
sleep 1
echo terminal length 0
sleep 1
echo show nat_um
sleep 10

) | telnet 0 65535 > telnet.log 2>&1

sed -n '/napt-spr/p' telnet.log | awk '{print $1,$3,$8}' > nat_um.log
#nat_um=`cat nat_um.log | tr -cd "[0-9]"`
#echo $nat_um

