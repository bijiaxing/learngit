#encoding: utf-8
import requests
import json
header={'content-type':'application/json','Accept':'application/json'}
requests.delete('http://112.74.109.30/api/v0.1/sensors/1/',headers=header)
#requests.delete('http://localhost:5000/api/v0.1/sensors/2/',headers=header)
#requests.delete('http://localhost:5000/api/v0.1/sensors/5/',headers=header)
#requests.delete('http://localhost:5000/api/v0.1/sensors/51/',headers=header)
