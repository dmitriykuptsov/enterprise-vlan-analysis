#!/usr/bin/python
import os
import gc
from hashlib import md5
import json
from sys import argv
import re

sipregex = re.compile("192\.168\..*\.254");
bipregex = re.compile("192\.168\..*\.255");
hashes  = {};
tcpapps = {};
udpapps = {};
counter = 0;

with open(argv[1]) as file:
	for line in file:
		# strip off the end of line
		line=line[0:len(line) - 1];
		# convert to json object
		d = json.loads(line);
		# if the packet is encapsulated (GRE protocol) 
		# we need to check the source and destination 
		# to see if it will be contained within the same
		# VLAN or not
		# Ignore broadcasts
		if d["eth"]["src"].startswith("ff:ff") or d["eth"]["dst"].startswith("ff:ff"):
			pass
		# Ignore special mutlicasts
		elif d["eth"]["src"].startswith("03:00") or d["eth"]["dst"].startswith("03:00"):
			pass
		# Ignore multicasts
		elif d["eth"]["src"].startswith("09:00") or d["eth"]["dst"].startswith("09:00"):
			pass
		# Ignore special multicasts sent by switches
		elif d["eth"]["src"].startswith("01:80") or d["eth"]["dst"].startswith("01:80"):
			pass
		elif d["eth"]["src"].startswith("01:00") or d["eth"]["dst"].startswith("01:00"):
			pass
		elif d["eth"]["src"].startswith("01:20") or d["eth"]["dst"].startswith("01:20"):
			pass
		# we should not see such frames here but anyways IPv6 multicasts
		elif d["eth"]["src"].startswith("33:33") or d["eth"]["dst"].startswith("33:33"):
			pass
		elif d["eth"]["src"].startswith("01:dd") or d["eth"]["dst"].startswith("01:dd"):
			pass
		elif d["eth"]["src"].startswith("ab:00") or d["eth"]["dst"].startswith("ab:00"):
			pass
		elif d["eth"]["src"].startswith("cf:00") or d["eth"]["dst"].startswith("cf:00"):
			pass
		elif d["ip"]["proto"] == "47":
			#if d["ppp"]["proto"] == "33":
			# The frame will be forwarded within the local area network
			# and so we need to find a corresponding pair to this packet
			if d["ppp"]["ip"]["src"].startswith("192.168.") and d["ppp"]["ip"]["dst"].startswith("192.168."):
				if d["ppp"]["ip"]["proto"] == "17":
					key1 = d["ppp"]["ip"]["src"] + ":" + d["udp"]["srcport"] + ":" + d["ppp"]["ip"]["dst"] + ":" +  d["udp"]["dstport"];
					key2 = d["ppp"]["ip"]["dst"] + ":" + d["udp"]["dstport"] + ":" + d["ppp"]["ip"]["src"] + ":" + d["udp"]["srcport"];
					bytes = int(d["udp"]["len"]);
					try:
						r = udpapps[key1];
						# Update the number of transmitted bytes
						r["bytes"] = r["bytes"] + bytes;
					except:
						try:
							r = udpapps[key2];
							r["bytes"] = r["bytes"] + bytes;
						except:
							udpapps[key1] = {
								"src": d["ppp"]["ip"]["src"],
								"dst": d["ppp"]["ip"]["dst"],
								"srcport": d["udp"]["srcport"],
								"dstport": d["udp"]["dstport"],
								"bytes": bytes
							};
				elif d["ppp"]["ip"]["proto"] == "6":
					key1 = d["tcp"]["stream_idx"] + d["ppp"]["ip"]["src"] + d["ppp"]["ip"]["dst"]
					key2 = d["tcp"]["stream_idx"] + d["ppp"]["ip"]["dst"] + d["ppp"]["ip"]["src"] 
					try:
						r = tcpapps[key1];
						r["bytes"] = r["bytes"] + int(d["tcp"]["len"]);
					except:
						try:
							r = tcpapps[key2];
							r["bytes"] = r["bytes"] + int(d["tcp"]["len"]);
						except:
							if int(d["tcp"]["flags"], 16) == 0x2:
								tcpapps[key1] = {};
								r = tcpapps[key1];
								r["src"] = d["ppp"]["ip"]["src"];
								r["dst"] = d["ppp"]["ip"]["dst"];
								r["srcport"] = d["tcp"]["srcport"];
								r["dstport"] = d["tcp"]["dstport"];
								r["bytes"]   = int(d["tcp"]["len"]);
			# for the following frames we should not see any duplicates
			elif d["ppp"]["ip"]["src"].startswith("192.168.") and not d["ppp"]["ip"]["dst"].startswith("192.168."):
				pass
			elif not d["ppp"]["ip"]["src"].startswith("192.168.") and d["ppp"]["ip"]["dst"].startswith("192.168."):
				pass
		# The frame contains plain IP packet
		# and if it contains the TCP or UDP header
		# we need to find a corresponding packet pair
		# which was forwarded with the same fields
		# but TTL decreased by 1
		else:
			if re.match(sipregex, d["ip"]["dst"]) or re.match(sipregex, d["ip"]["src"]):
				if d["ip"]["proto"] == "17":
					key1 = d["ip"]["src"] + ":" + d["udp"]["srcport"] + ":" + d["ip"]["dst"] + ":" + d["udp"]["dstport"];
					key2 = d["ip"]["dst"] + ":" + d["udp"]["dstport"] + ":" + d["ip"]["src"] + ":" + d["udp"]["srcport"];	
					bytes = int(d["udp"]["len"]);
					try:
						r = udpapps[key1];
						# Update the number of transmitted bytes
						r["bytes"] = r["bytes"] + bytes;
					except:
						try:
							r = udpapps[key2];
							r["bytes"] = r["bytes"] + bytes;
						except:
							udpapps[key1] = {
								"src": d["ip"]["src"],
								"dst": d["ip"]["dst"],
								"srcport": d["udp"]["srcport"],
								"dstport": d["udp"]["dstport"],
								"bytes": bytes
							};
				elif d["ip"]["proto"] == "6":
					key1 = d["tcp"]["stream_idx"] + d["ip"]["src"] + d["ip"]["dst"]
					key2 = d["tcp"]["stream_idx"] + d["ip"]["dst"] + d["ip"]["src"] 
					try:
						r = tcpapps[key1];
						r["bytes"] = r["bytes"] + int(d["tcp"]["len"]);
					except:
						try:
							r = tcpapps[key2];
							r["bytes"] = r["bytes"] + int(d["tcp"]["len"]);
						except:
							if int(d["tcp"]["flags"], 16) == 0x2:
								tcpapps[key1] = {};
								r = tcpapps[key1];
								r["src"] = d["ip"]["src"];
								r["dst"] = d["ip"]["dst"];
								r["srcport"] = d["tcp"]["srcport"];
								r["dstport"] = d["tcp"]["dstport"];
								r["bytes"]   = int(d["tcp"]["len"]);
			if re.match(bipregex, d["ip"]["dst"]) or re.match(bipregex, d["ip"]["src"]):
				if d["ip"]["proto"] == "17":
					key1 = d["ip"]["src"] + ":" + d["udp"]["srcport"] + ":" + d["ip"]["dst"] + ":" + d["udp"]["dstport"];
					key2 = d["ppp"]["ip"]["dst"] + ":" + d["udp"]["dstport"] + ":" + d["ppp"]["ip"]["src"] + ":" + d["udp"]["srcport"];
					bytes = int(d["udp"]["len"]);
					try:
						r = udpapps[key1];
						# Update the number of transmitted bytes
						r["bytes"] = r["bytes"] + bytes;
					except:
						try:
							r = udpapps[key2];
							r["bytes"] = r["bytes"] + bytes;
						except:
							udpapps[key1] = {
								"src": d["ip"]["src"],
								"dst": d["ip"]["dst"],
								"srcport": d["udp"]["srcport"],
								"dstport": d["udp"]["dstport"],
								"bytes": bytes
							};
				elif d["ip"]["proto"] == "6":
					key1 = d["tcp"]["stream_idx"] + d["ip"]["src"] + d["ip"]["dst"]
					key2 = d["tcp"]["stream_idx"] + d["ip"]["dst"] + d["ip"]["src"] 
					try:
						r = tcpapps[key1];
						r["bytes"] = r["bytes"] + int(d["tcp"]["len"]);
					except:
						try:
							r = tcpapps[key2];
							r["bytes"] = r["bytes"] + int(d["tcp"]["len"]);
						except:
							if int(d["tcp"]["flags"], 16) == 0x2:
								tcpapps[key1] = {};
								r = tcpapps[key1];
								r["src"] = d["ip"]["src"];
								r["dst"] = d["ip"]["dst"];
								r["srcport"] = d["tcp"]["srcport"];
								r["dstport"] = d["tcp"]["dstport"];
								r["bytes"]   = int(d["tcp"]["len"]);
			elif (d["ip"]["src"].startswith("192.168.") and not d["ip"]["dst"].startswith("192.168.")) or (not d["ip"]["src"].startswith("192.168.") and d["ip"]["dst"].startswith("192.168.")):
				if d["ip"]["proto"] == "17":
					key1 = d["ip"]["src"] + ":" + d["udp"]["srcport"] + ":" + d["ip"]["dst"] + ":" + d["udp"]["dstport"];
					key2 = d["ppp"]["ip"]["dst"] + ":" + d["udp"]["dstport"] + ":" + d["ppp"]["ip"]["src"] + ":" + d["udp"]["srcport"];
					bytes = int(d["udp"]["len"]);
					try:
						r = udpapps[key1];
						# Update the number of transmitted bytes
						r["bytes"] = r["bytes"] + bytes;
					except:
						try:
							r = udpapps[key2];
							r["bytes"] = r["bytes"] + bytes;
						except:
							udpapps[key1] = {
								"src": d["ip"]["src"],
								"dst": d["ip"]["dst"],
								"srcport": d["udp"]["srcport"],
								"dstport": d["udp"]["dstport"],
								"bytes": bytes
							};
				elif d["ip"]["proto"] == "6":
					key1 = d["tcp"]["stream_idx"] + d["ip"]["src"] + d["ip"]["dst"]
					key2 = d["tcp"]["stream_idx"] + d["ip"]["dst"] + d["ip"]["src"] 
					try:
						r = tcpapps[key1];
						r["bytes"] = r["bytes"] + int(d["tcp"]["len"]);
					except:
						try:
							r = tcpapps[key2];
							r["bytes"] = r["bytes"] + int(d["tcp"]["len"]);
						except:
							if int(d["tcp"]["flags"], 16) == 0x2:
								tcpapps[key1] = {};
								r = tcpapps[key1];
								r["src"] = d["ip"]["src"];
								r["dst"] = d["ip"]["dst"];
								r["srcport"] = d["tcp"]["srcport"];
								r["dstport"] = d["tcp"]["dstport"];
								r["bytes"]   = int(d["tcp"]["len"]);
			elif not d["ip"]["src"].startswith("192.168.") and d["ip"]["dst"].startswith("192.168."):
				pass
			elif d["ip"]["src"].startswith("10.10.10.254") or d["ip"]["dst"].startswith("10.10.10.254"):
				pass
			else:
				if d["ip"]["proto"] == "17":
					key1 = d["ip"]["src"] + ":" + d["udp"]["srcport"] + ":" + d["ip"]["dst"] + ":" + d["udp"]["dstport"];
					key2 = d["ip"]["dst"] + ":" + d["udp"]["dstport"] + ":" + d["ip"]["src"] + ":" + d["udp"]["srcport"];
					bytes = int(d["udp"]["len"]);
					try:
						r = udpapps[key1];
						# Update the number of transmitted bytes
						r["bytes"] = r["bytes"] + bytes;
					except:
						try:
							r = udpapps[key2];
							r["bytes"] = r["bytes"] + bytes;
						except:
							udpapps[key1] = {
								"src": d["ip"]["src"],
								"dst": d["ip"]["dst"],
								"srcport": d["udp"]["srcport"],
								"dstport": d["udp"]["dstport"],
								"bytes": bytes
							};
				elif d["ip"]["proto"] == "6":
					key1 = d["tcp"]["stream_idx"] + d["ip"]["src"] + d["ip"]["dst"]
					key2 = d["tcp"]["stream_idx"] + d["ip"]["dst"] + d["ip"]["src"] 
					try:
						r = tcpapps[key1];
						r["bytes"] = r["bytes"] + int(d["tcp"]["len"]);
					except:
						try:
							r = tcpapps[key2];
							r["bytes"] = r["bytes"] + int(d["tcp"]["len"]);
						except:
							if int(d["tcp"]["flags"], 16) == 0x2:
								tcpapps[key1] = {};
								r = tcpapps[key1];
								r["src"] = d["ip"]["src"];
								r["dst"] = d["ip"]["dst"];
								r["srcport"] = d["tcp"]["srcport"];
								r["dstport"] = d["tcp"]["dstport"];
								r["bytes"]   = int(d["tcp"]["len"]);

print "TCP APPS:"
for key in tcpapps.keys():
	print tcpapps[key];

print "UDP APPS:"
for key in udpapps.keys():
	print udpapps[key];


