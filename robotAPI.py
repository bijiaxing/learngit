#encoding: utf-8

from flask import Flask, request
from flask_restful import Api, Resource, abort
from flask_sqlalchemy import SQLAlchemy
import time
app = Flask(__name__)
api = Api(app)
app.config['RESTFUL_JSON'] = {'ensure_ascii': False}
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///iotDB.db'
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql://web:web@localhost/robot'#用与链接数据库url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False#禁用跟踪
db = SQLAlchemy(app)

class Robots(db.Model):
    __tablename__ = 'Robots'#Robots表
    id = db.Column(db.Integer, primary_key=True)#设备的唯一标识
    name = db.Column(db.String(20))#机器人名称
    type = db.Column(db.Integer)#机器人类型
    mac = db.Column(db.String(20))#mac地址
    brand = db.Column(db.String(20))#机器人品牌
    series = db.Column(db.String(20))#机器人品牌系列号
    unit = db.Column(db.Integer)#传感器默认单位（如0表华师温度1表摄氏温度）
    state = db.Column(db.Integer)#传感器状态（01234工作没工作等等）
    register_time = db.Column(db.String(30))#传感器注册时间
    update_time = db.Column(db.String(30))#传感器数据更新时间
    count = db.Column(db.Integer)#传感器当前数据总量
    description = db.Column(db.String(40))#传感器描述

    # 如果没初值的情况写一下
    def __init__(self,
                 id,
                 name='101',
                 type=1,
                 mac='dslkfj',
                 unit=1,
                 state=1,
                 register_time='xinzi',
                 update_time='gangcai',
                 count=1,
                 brand='dfd',
                 series='chanshi',
                 description='cahnshg'):
        self.id = id
        self.name = name
        self.type = type
        self.mac = mac
        self.brand = brand
        self.series = series
        self.unit = unit
        self.state = state
        self.register_time = register_time
        self.update_time = update_time
        self.count = count
        self.description = description

    def __repr__(self):
        return self.id


class ROBOT(db.Model):
    __tablename__ = 'ROBOT'#ROBOT   表
    __table_args__ = {'sqlite_autoincrement': True}
    no = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer)#机器人编号
    axisX = db.Column(db.Integer)#传感器x坐标
    axisY = db.Column(db.Integer)#传感器Y坐标
    axisZ = db.Column(db.Integer)#传感器Z坐标
    state = db.Column(db.Integer)#是否工作

    def __init__(self, id, axisX, axisY, axisZ, state):
        self.id = id
        self.axisX = axisX
        self.axisY = axisY
        self.axisZ = axisZ
        self.state = state

    def __repr__(self):
        return self.id

#前两个针对数据库,调用Sensor()和SensorData()将产生行对象

class RobotListAPI(Resource):
    def get(self):
        results = []
        for result in Robots.query.all():
            d = {
                'id': result.id,
                'name': result.name,
                'type': result.type,
                'mac': result.mac,
                'brand': result.brand,
                'series': result.series,
                'unit': result.unit,
                'state': result.state,
                'register_time': result.register_time,
                'update_time': result.update_time,
                'count': result.count,
                'description': result.description,
            }
            results.append(d)
        return results

    def put(self):
        # todo 非空检测
        if request.json['id'] in map(lambda x: x.id, Robots.query.all()):#lambda为匿名函数之用,迭代出所有的已有id
            abort(400)
        sensor = Robots(request.json['id'], request.json['name'],
                         request.json['type'], request.json['mac'],
                         request.json['unit'], request.json['state'],
                         time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                         time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                         0, request.json['brand'], request.json['series'],
                         request.json['description'])
#生成新对象sensor
        db.session.add(sensor)
        db.session.commit()#提交到数据库

        # 这里的实现最好从数据库中查，不然时间不准
        d = dict()
        d['id'] = request.json['id']
        d['name'] = request.json['name']
        d['type'] = request.json['type']
        d['mac'] = request.json['mac']
        d['unti'] = request.json['unit']
        d['state'] = request.json['state']
        d['register_time'] = time.strftime("%Y-%m-%d %H:%M:%S",
                                           time.localtime())
        d['update_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        d['brand'] = request.json['brand']
        d['serise'] = request.json['series']
        d['description'] = request.json['description']
        return d, 201
#把字典和201参数返回,表示查询成功

class ROBOTAPI(Resource):
    def get(self, sensor_id):
        limit = request.args.get('limit', 5)
        if sensor_id not in map(lambda x: x.id, Robots.query.all()):
            abort(404)

        results = []
        for result in ROBOT.query.filter_by(
                id=sensor_id).limit(limit).all():
            d = {
                'id': result.id,
                'axisX': result.axisX,
                'axisY': result.axisY,
                'axisZ': result.axisZ,
                'state': result.state
            }
            results.append(d)
        return results, 201

    # count值不变
    def post(self, sensor_id):
        if sensor_id not in map(lambda x: x.id, Robots.query.all()):
            abort(400)
        if sensor_id != request.json['id']:
            abort(400)

        sensor = dict()
        sensor['id'] = request.json['id']
        sensor['axisX'] = request.json['axisX']
        sensor['axisY'] = request.json['axisY']
        sensor['axisZ'] = request.json['axisZ']
        sensor['state'] = request.json['state']

        sensor_data = ROBOT(request.json['id'], request.json['axisX'],
                                 request.json['axisY'], request.json['axisZ'],
                                 request.json['state'])
        db.session.add(sensor_data)
        db.session.commit()
        return sensor, 201

    def put(self, sensor_id):
        if sensor_id not in map(lambda x: x.id, Robots.query.all()):
            abort(400)
        if sensor_id != request.json['id']:
            abort(400)

        sensor = dict()
        sensor['id'] = request.json['id']
        sensor['axisY'] = request.json['axisY']
        sensor['axisX'] = request.json['axisX']
        sensor['axisZ'] = request.json['axisZ']
        sensor['state'] = request.json['state']
        sensor_data = ROBOT(request.json['id'], request.json['axisX'],
                                 request.json['axisY'], request.json['axisZ'],
                                 request.json['state'])
        db.session.add(sensor_data)
        db.session.commit()

        return sensor, 201

    # 删除一条信息呢
    def delete(self, sensor_id):
        if sensor_id not in map(lambda x: x.id, Robots.query.all()):
            abort(400)

        for sensor in Robots.query.filter_by(id=sensor_id).all():
            db.session.delete(sensor)
        for sensor_data in ROBOT.query.filter_by(id=sensor_id).all():
            db.session.delete(sensor_data)
        db.session.commit()
        return "", 204
db.create_all();
api.add_resource(RobotListAPI, '/api/v0.1/sensors/')
api.add_resource(ROBOTAPI, '/api/v0.1/sensors/<int:sensor_id>/')

if __name__ == '__main__':
    app.run(debug=True)


