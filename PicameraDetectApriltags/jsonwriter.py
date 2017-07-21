import json

data = {
	'0':'(0, 0)',
	'1':'(0, 10)',
	'2':'(10, 0)'
} 

json_str = json.dumps(data)

with open('config.json', 'w') as f:
	json.dump(json_str, f)

with open('config.json', 'r') as f:
	print json.load(f)
