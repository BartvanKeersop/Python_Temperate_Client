import requests

def jsonify(time, temp):
	data = '{\'time\':\'%s\',\'temp\':\'%s\'}' % (time, temp)
	return data

def post_data(data):
	url = 'https://requestb.in/1ck7q7q1'
	headers = {'accept': 'application/json','content-type': 'application/json'}  
	r = requests.post(url, data = data, headers = headers)
	print r.status_code
	print r.content
	print r.headers


json_data = jsonify(11, 33)
post_data(json_data)
