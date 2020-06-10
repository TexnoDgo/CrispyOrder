import requests

import json

empty_field = 'edrpou'
value = '32601315'
prelink = '{%22' + empty_field + '%22:%22' + value + '%22}'
print(prelink)
link = 'http://edr.data-gov-ua.org/api/companies?where=' + prelink
print(link)
response = requests.get(link)
data = json.loads(response.text)
print(data)
first = data[0]
print(first)
print(first["name"])