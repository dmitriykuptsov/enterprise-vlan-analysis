#!/usr/bin/python

import os
import gc
from hashlib import md5
import json
from sys import argv

data   = [];
hashes = [];
ttls   = [];

with open(argv[1]) as file:
	for line in file:
		# strip off the end of line and last comma
		line=line[0:len(line) - 1]
		# convert to json object
		d = json.loads(line)
		# if ttl field is present than this packet can be forwarded,
		# otherwise the packet for sure will be contained within the
		# same vlan
		if (d["eth"]["src"] != "00:30:05:4f:39:87" and d["eth"]["dst"] != "00:30:05:4f:39:87") and d["eth"]["dst"] != "ff:ff:ff:ff:ff:ff" and d["eth"]["dst"] != "01:00:0c:cc:cc:cd" and not d["eth"]["dst"].startswith("33:33") and d["eth"]["dst"] != "01:80:c2:00:00:00" and not d["eth"]["dst"].startswith("01:00:5e:") and not d["eth"]["dst"].startswith("01:00:0c:cc:cc:cc") and not d["eth"]["dst"] == "01:00:0c:cc:cc:cd" and not d["eth"]["proto"] == "0x00009000" and not d["eth"]["dst"].startswith("03:00:00"):
			print line
		#if d["eth"]["proto"] == "":
		#	if d["eth"]["dst"] == "01:00:0c:cc:cc:cc":
		#		d["eth"]["proto"] = "0x00002000"
