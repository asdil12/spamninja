#!/usr/bin/python2

import os
import requests

spam_mnts = [
	"AQUATIX-MNT",
]

def get_nets_from_mnt(mnt):
	params = {
		"inverse-attribute": "mnt-by",
		"type-filter": "route",
		"query-string": mnt
	}
	headers = {
		"Accept": "application/json"
	}
	r = requests.get("http://rest.db.ripe.net/search", params=params, headers=headers)
	nets = []
	for obj in r.json()["objects"]["object"]:
		if obj["type"] != "route":
			continue
		for atr in obj["primary-key"]["attribute"]:
			if atr["name"] == "route":
				nets.append(atr["value"])
	return nets

networks = []
for mnt in spam_mnts:
	networks.extend(get_nets_from_mnt(mnt))

with open("/etc/postfix/cidr_spamninja", "w") as f:
	for net in networks:
		print net
		f.write("%s REJECT Blocked by SpamNinja\n" % net)

os.system("postfix reload")
