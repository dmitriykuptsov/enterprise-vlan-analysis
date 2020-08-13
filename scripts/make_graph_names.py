#!/usr/bin/python
import sys
from sys import argv
import json
filename=argv[1];
lines=[];
with open(filename) as f:
	for l in f:
		lines.append(json.loads(l.replace("'", "\"").replace("u\"", "\"")));
addrs=[];
uniq={};
for d in lines:
	src=d["src"];
	dst=d["dst"];
	uniq[src]="";
	uniq[dst]="";
addrs=uniq.keys();
addrs.sort();
s=len(addrs);
matrix = [[0 for x in range(s)] for y in range(s)];
for d in lines:
	src=d["src"];
	dst=d["dst"];
	idx1=addrs.index(src);
	idx2=addrs.index(dst);
	matrix[idx1][idx2] = 1;

#sys.stdout.write(",");
#for x in range(s):
#	sys.stdout.write(addrs[x] + ",");
#	if x < s - 1:
#		sys.stdout.write("\""+addrs[x] + "\",");
#	else:
#		sys.stdout.write("\""+addrs[x] + "\"");
#sys.stdout.write("\n");
#for x in range(s):
#	#sys.stdout.write(addrs[x] + ",");
#	for y in range(s):
#		if y < s - 1:
#			sys.stdout.write(str(matrix[x][y]) + ",");
#		else:
#			sys.stdout.write(str(matrix[x][y]));
#	sys.stdout.write("\n");

for a in addrs:
	print a
