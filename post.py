#encoding: utf-8
import requests
import json
header={'content-type':'application/json','Accept':'application/json'}
#Accept:浏览器可以接受服务器可以发回来的媒体类型
#
value={'id':2,'name':'liuweichao','type':9,'mac':'wangziqi','unit':1,'state':1,'brand':'shiyan','series':'T','description':'hellow worls'}
r=requests.put('http://112.74.109.30/api/v0.1/sensors/',data=json.dumps(value),headers=header)

