nmap -v 192.168.0.0/19 | 
	grep -i discovered |  
		awk -F" " '{print " "}' | 
			awk -F"/" '{print " "}' | 
				sed -e "s|\(.*\)\ \([0-9]*\.[0-9]*\.[0-9]*\)\.\([0-9]*\).*|\1 \2\.\3 \2\.0|g" >> scanned_open_ports.cvs
