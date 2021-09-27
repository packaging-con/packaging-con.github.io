import os
import requests
import json

API_KEY=os.environ['PT_API']

def pretalx_api(stub):
	if "://" not in stub:
		url = f'https://pretalx.com/api/' + stub
	else:
		url = stub

	resp = requests.get(url, headers={"Authorization": f'Token {API_KEY}'})

	return resp.json()

api_endpoint="events/packagingcon-2021/submissions"

d = pretalx_api(api_endpoint)

export_json = []

have_next = True
print(d)
while have_next:
	for t in d["results"]:
		print(t["title"], t["state"])
		if t["state"] == 'confirmed':
			export_json.append({
				"title": t["title"],
				"speakers": t["speakers"],
				"abstract": t["abstract"]
			})

	have_next = d["next"] is not None
	if d["next"]:
		d = pretalx_api(d["next"])

with open('talks.json', 'w') as fo:
	json.dump(export_json, fo)