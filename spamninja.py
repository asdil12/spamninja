#!/usr/bin/python2

import os
import socket
import datetime

as_list = [
	("AS25489", "Aquatix")
]

def get_as_networks(as_id):
	sock = socket.create_connection(('whois.ripe.net', 43))
	try:
		sock.sendall("-T route -i origin %s\r\n" % as_id)
		for line in sock.makefile().readlines():
			line = line.strip()
			if line.startswith("route:"):
				net = line.split(" ")[-1]
				yield net
	finally:
		sock.close()

with open("/etc/postfix/cidr_spamninja", "w") as f:
	f.write("# Autogenerated by SpamNinja on %s\n\n" % datetime.datetime.now().ctime())
	for as_id, as_name in as_list:
		print "Querying %s (%s)" % (as_name, as_id)
		f.write("# %s (%s)\n" % (as_name, as_id))
		for net in get_as_networks(as_id):
			print "  %s" % net
			f.write("%s REJECT Blocked by SpamNinja\n" % net)

os.system("postfix reload 2>&1")
