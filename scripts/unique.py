#!/usr/bin/python

import sys
from sys import argv
import hashlib

f=open(argv[1]);
lines={}

for l in f:
	h = hashlib.md5(l).hexdigest();
	try:
		r = lines[h]
		lines[h]["count"] = lines[h]["count"] + 1
	except:
		lines[h]={"l": l, "count": 1}

for key in lines.keys():
	sys.stdout.write(str(lines[key]["count"]) + " " + lines[key]["l"]);

