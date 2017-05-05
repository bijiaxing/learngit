#encoding: utf-8
import requests
import json
header={'content-type':'application/json','Accept':'application/json'}
#Accept:浏览器可以接受服务器可以发回来的媒体类型
#
value={'no':2,'id':1,'axisX':100,'axisY':150,'axisZ':690,'state':0}
r=requests.put('http://112.74.109.30/api/v0.1/sensors/1/',data=json.dumps(value),headers=header)
