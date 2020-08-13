#!/usr/bin/python
import os
import gc
from hashlib import md5
import json
from sys import argv
import re

sipregex = re.compile("192\.168\..*\.254");
bipregex = re.compile("192\.168\..*\.255");
hashes = {};

with open(argv[1]) as file:
	for line in file:
		# strip off the end of line
		line=line[0:len(line) - 1];
		# convert to json object
		d = json.loads(line);
		# if the packet is encapsulated (GRE protocol)
		# we need to check the source and destination
		# to see if it will be contained within 192.168.0.0/16 subnetwork or not
		# Ignore broadcasts and multicasts since they are not forwarded between the subnetworks
		if d["eth"]["src"].startswith("ff:ff") or d["eth"]["dst"].startswith("ff:ff"):
			print line
		elif d["eth"]["src"].startswith("03:00") or d["eth"]["dst"].startswith("03:00"):
			print line
		elif d["eth"]["src"].startswith("09:00") or d["eth"]["dst"].startswith("09:00"):
			print line
		elif d["eth"]["src"].startswith("01:80") or d["eth"]["dst"].startswith("01:80"):
			print line
		elif d["eth"]["src"].startswith("01:00") or d["eth"]["dst"].startswith("01:00"):
			print line
		elif d["eth"]["src"].startswith("01:20") or d["eth"]["dst"].startswith("01:20"):
			print line
		elif d["eth"]["src"].startswith("33:33") or d["eth"]["dst"].startswith("33:33"):
			print line
		elif d["eth"]["src"].startswith("01:dd") or d["eth"]["dst"].startswith("01:dd"):
			print line
		elif d["eth"]["src"].startswith("ab:00") or d["eth"]["dst"].startswith("ab:00"):
			print line
		elif d["eth"]["src"].startswith("cf:00") or d["eth"]["dst"].startswith("cf:00"):
			print line
		elif d["ip"]["proto"] == "47":
			#if d["ppp"]["proto"] == "33":
			# The frame will be forwarded within the local area network
			# and so we need to find a corresponding pair to this packet
			# src - private IP, dst - public IP
			if d["ppp"]["ip"]["src"].startswith("192.168.") and not d["ppp"]["ip"]["dst"].startswith("192.168."):
				print line
			# src - public IP, dst - private IP
			elif not d["ppp"]["ip"]["src"].startswith("192.168.") and d["ppp"]["ip"]["dst"].startswith("192.168."):
				print line
			# src - private IP, dst - server's own IP address
			elif d["ppp"]["ip"]["src"].startswith("192.168.") and re.match(sipregex, d["ppp"]["ip"]["src"]):
				print line
			# src - private IP, dst - broadcast (curious fact on its own)
			elif d["ppp"]["ip"]["src"].startswith("192.168.") and re.match(bipregex, d["ppp"]["ip"]["src"]):
				print line
			# else both src and dst are private, non-broadcast, not server's own IP address
			elif d["ppp"]["ip"]["src"].startswith("192.168.") and d["ppp"]["ip"]["dst"].startswith("192.168."):
				# This is the packet which was forwarded with TTL reduced by 1
				if d["eth"]["src"] == "00:30:05:4f:39:87":
					print line
				# This is the packet to be forwarded with unmodified TTL field and so skip it
				elif d["eth"]["dst"] == "00:30:05:4f:39:87":
					pass
				# All other traffic needs accepted
				else:
					print line
			# for the following frames we should not see any duplicates
		# The frame contains plain IP packet
		# and if it contains the TCP or UDP header
		# we need to find a corresponding packet pair 
		# which was forwarded with the same fields 
		# but TTL decreased by 1
		else:
			# src or dst private, server's own IP
			if re.match(sipregex, d["ip"]["dst"]) or re.match(sipregex, d["ip"]["src"]):
				print line
			# dst - broadcast
			if re.match(bipregex, d["ip"]["dst"]):
				print line
			# src - private, dst - public
			elif d["ip"]["src"].startswith("192.168.") and not d["ip"]["dst"].startswith("192.168."):
				print line
			# src - public, dst - private
			elif not d["ip"]["src"].startswith("192.168.") and d["ip"]["dst"].startswith("192.168."):
				print line
			# src or dst private, server's own IP address
			elif d["ip"]["src"].startswith("10.10.10.254") or d["ip"]["dst"].startswith("10.10.10.254"):
				print line
			else:
				# This is the packet which was forwarded with TTL reduced by 1
				if d["eth"]["src"] == "00:30:05:4f:39:87":
					print line
				# This is the packet to be forwarded with the unmodified TTL and so skip it
				elif d["eth"]["dst"] == "00:30:05:4f:39:87":
					pass
				# Print out all other frames (perhaps they are having wrong destination MAC address)
				else:
					print line





