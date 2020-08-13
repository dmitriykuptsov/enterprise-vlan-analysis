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
		if d["eth"]["proto"] != "0x00000800" and d["vlan"]["proto"] != "0x00000800":
			print line
		#if d["eth"]["proto"] == "":
		#	if d["eth"]["dst"] == "01:00:0c:cc:cc:cc":
		#		d["eth"]["proto"] = "0x00002000"

