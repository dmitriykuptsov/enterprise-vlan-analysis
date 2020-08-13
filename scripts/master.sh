#!/bin/bash
echo "Finding non IPv4 frames..."
python find_non_ip_frames.py ../tep_inter_vlan_1480919022.json > ../tep_inter_vlan_1480919022_proto_non_ip.json
echo "Looking for L2 and L3 (non IPv4) protocol types..."
total=`cat ../tep_inter_vlan_1480919022_proto_non_ip.json | wc -l`
arp=`cat ../tep_inter_vlan_1480919022_proto_non_ip.json | grep 0x00000806 | wc -l`
ipv6=`cat ../tep_inter_vlan_1480919022_proto_non_ip.json | grep 0x000086dd | wc -l`
ipx=`cat ../tep_inter_vlan_1480919022_proto_non_ip.json | grep -v 0x00000806 | grep -v 0x000086dd | grep -v 01:80:c2:00:00:00 | grep -v 01:00:0c:cc:cc:cd | grep -v 0x00009000 | grep -v 01:00:0c:cc:cc:cc | grep 00:c0:ee:78:8c:bc | wc -l` # Only Kyocera send the traffic over IPX
stp=`cat ../tep_inter_vlan_1480919022_proto_non_ip.json | grep 01:80:c2:00:00:00 | wc -l`
csstp=`cat ../tep_inter_vlan_1480919022_proto_non_ip.json | grep 01:00:0c:cc:cc:cd | wc -l`
clp=`cat ../tep_inter_vlan_1480919022_proto_non_ip.json | grep 0x00009000 | wc -l`
cdp=`cat ../tep_inter_vlan_1480919022_proto_non_ip.json | grep -i 01:00:0C:CC:CC:CC | wc -l`
printf 'ARP %.*f\n' 1 `echo $arp/$total*100.0|bc -l`
printf 'CSSTP %.*f\n' 1 `echo $csstp/$total*100.0|bc -l`
printf 'IPv6 %.*f\n' 1 `echo $ipv6/$total*100.0|bc -l`
printf 'STP %.*f\n' 1 `echo $stp/$total*100.0|bc -l`
printf 'IPX %.*f\n' 1 `echo $ipx/$total*100.0|bc -l`
printf 'CLP %.*f\n' 1 `echo $clp/$total*100.0|bc -l`
printf 'CDP %.*f\n' 1 `echo $cdp/$total*100.0|bc -l`
echo "Sanity check: "
echo "   Total packets: $total Accumulated: `echo "($arp+$csstp+$ipv6+$stp+$ipx+$clp+$cdp)"|bc -l`"
echo ""
echo "Finding IPv4 frames only..."
python  find_ip_frames.py ../tep_inter_vlan_1480919022.json > ../tep_inter_vlan_1480919022_proto_ip.json
echo "Looking for frames in native VLAN..."
python find_native_vlan_frames.py ../tep_inter_vlan_1480919022.json > ../tep_inter_vlan_1480919022_native_vlan.json
echo "Looking for L2 and L3 protocol types for native VLAN..."
total=`cat ../tep_inter_vlan_1480919022_native_vlan.json | wc -l`
arp=`cat ../tep_inter_vlan_1480919022_native_vlan.json   | grep 0x00000806 | wc -l`
ipv4=`cat ../tep_inter_vlan_1480919022_native_vlan.json  | grep 0x00000800 | wc -l`
stp=`cat ../tep_inter_vlan_1480919022_native_vlan.json   | grep 01:80:c2:00:00:00 | wc -l`
csstp=`cat ../tep_inter_vlan_1480919022_native_vlan.json | grep 01:00:0c:cc:cc:cd | wc -l`
clp=`cat ../tep_inter_vlan_1480919022_native_vlan.json   | grep 0x00009000 | wc -l`
cdp=`cat ../tep_inter_vlan_1480919022_native_vlan.json   | grep -i 01:00:0C:CC:CC:CC | wc -l`
printf 'CSSTP %.*f\n' 1 `echo $csstp/$total*100.0|bc -l`
printf 'STP %.*f\n' 1 `echo $stp/$total*100.0|bc -l`
printf 'CLP %.*f\n' 1 `echo $clp/$total*100.0|bc -l`
printf 'IPv4 (ICMP only) %.*f\n' 1 `echo $ipv4/$total*100.0|bc -l`
printf 'CDP %.*f\n' 1 `echo $cdp/$total*100.0|bc -l`
printf 'ARP %.*f\n' 1 `echo $arp/$total*100.0|bc -l`
echo "Sanity check: "
echo "   Total packets: $total Accumulated: `echo "($arp+$csstp+$ipv4+$stp+$clp+$cdp)" | bc -l`"
echo ""
echo "Matching invalid mac addresses..."
python find_invalid_mac_addresses_in_ip.py ../tep_inter_vlan_1480919022_proto_ip.json > ../tep_inter_vlan_1480919022_proto_ip_invalid_mac_frames.json 
cat ../tep_inter_vlan_1480919022_proto_ip_invalid_mac_frames.json | sed "s|.*eth.*src\":\"\([0-9,\:,a-f]*\)\"\,\"dst\"\:\"\([0-9,\:,a-f]*\)\".*ip.*src\":\"\([0-9,\.]*\)\"\,\"dst\"\:\"\([0-9,.]*\)\".*ppp.*|\1 \2 \3 \4|g" > ../tep_inter_vlan_1480919022_proto_ip_invalid_mac_frames.csv
echo "" >> ../tep_inter_vlan_1480919022_proto_ip_invalid_mac_frames.csv
cat ../tep_inter_vlan_1480919022_proto_ip_invalid_mac_frames.csv | grep -P "[0-9a-zA-Z]" | while read line;
do
  src_mac=`echo $line | awk -F" " '{print $1}'`;
  src_mac_oui=`echo $line | awk -F" " '{print $1}' | awk -F":" '{print $1":"$2":"$3}'`;
  dst_mac=`echo $line | awk -F" " '{print $2}'`;
  dst_mac_oui=`echo $line | awk -F" " '{print $2}' | awk -F":" '{print $1":"$2":"$3}'`;
  src_ip=`echo $line | awk -F" " '{print $3}'`;
  dst_ip=`echo $line | awk -F" " '{print $4}'`;
  src_mac_vendor=`grep -i $src_mac_oui ../vendor_mac_address_mapping.txt | dos2unix | awk -F" " '{print $2}'`;
  dst_mac_vendor=`grep -i $dst_mac_oui ../vendor_mac_address_mapping.txt | dos2unix | awk -F" " '{print $2}'`;
  echo "$src_mac $dst_mac $src_ip $dst_ip $src_mac_vendor/$dst_mac_vendor";
done > ../tep_inter_vlan_1480919022_proto_ip_invalid_mac_frames_formated.csv;
./unique.py ../tep_inter_vlan_1480919022_proto_ip_invalid_mac_frames_formated.csv;
echo "Matching packet pairs...";
python find_packet_pair.py ../tep_inter_vlan_1480919022_proto_ip.json > ../tep_inter_vlan_1480919022_proto_ip_no_duplicates.json;
echo "Binning flows by port numbers...";
python find_applications.py ../tep_inter_vlan_1480919022_proto_ip_no_duplicates.json > ../tep_inter_vlan_1480919022_applications.json;

echo "Separating UDP and TCP applications..."
udp_apps_start_line=$((`grep -n UDP  ../tep_inter_vlan_1480919022_applications.json | awk -F":" '{print $1}'`+1));
tcp_apps_start_line=1;
udp_apps_end_line=`wc -l ../tep_inter_vlan_1480919022_applications.json | awk -F" " '{print $1}'`;
tcp_apps_end_line=$(($udp_apps_start_line-2));
num_tcp_apps=$(($tcp_apps_end_line-$tcp_apps_start_line));
num_udp_apps=$(($udp_apps_end_line-$udp_apps_start_line+1));
head -n $tcp_apps_end_line ../tep_inter_vlan_1480919022_applications.json | tail -n $num_tcp_apps > ../tep_inter_vlan_1480919022_tcp_applications.json;
tail -n $num_udp_apps ../tep_inter_vlan_1480919022_applications.json > ../tep_inter_vlan_1480919022_udp_applications.json;

echo "Counting application frequencies..."
cat ../tep_inter_vlan_1480919022_tcp_applications.json | sed "s|.*dstport\x27\:\su\x27\([0-9]*\)\x27.*|\1|g" > ../tcp_ports.csv
echo "Top 10 TCP applications"
python ./unique.py ../tcp_ports.csv | sort -n -r | head -n 10

cat ../tep_inter_vlan_1480919022_udp_applications.json | sed "s|.*dstport\x27\:\su\x27\([0-9]*\)\x27.*|\1|g" > ../udp_ports.csv
echo "Top 10 UDP applications"
python ./unique.py ../udp_ports.csv | sort -n -r | head -n 10

echo "Building distribution of bytes transmitted by UDP and TCP applications"
cat ../tep_inter_vlan_1480919022_tcp_applications.json | sed "s|.*bytes\x27\:\s\([0-9]*\)\,\s\x27.*|\1|g" > ../tcp_bytes.csv
cat ../tep_inter_vlan_1480919022_udp_applications.json | sed "s|.*bytes\x27\:\s\([0-9]*\)\,\s\x27.*|\1|g" > ../udp_bytes.csv
