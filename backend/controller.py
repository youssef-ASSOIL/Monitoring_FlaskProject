import json
from flask import (
    Flask,
    jsonify,
    render_template,
    send_file,
    request,
    redirect
)

from services.IotService import IotService
from services.EndService import EndService
import matplotlib
from matplotlib import pyplot as plt
from io import BytesIO
from models import EndDevice,EndDeviceInfo,IoT
from dal.EndDao import EndDao
from dal.IotDao import IotDao
from services.AppService import AppService
from services.CityService import CityService

cityService=CityService()


app=Flask(__name__)
matplotlib.use('agg')


serve=AppService(IotDao(),EndDao())
serve.start()
service = IotService()
serviceEnd = EndService()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/get-iot-devices')
def get_iot_devices():
    iot_devices = service.getAllDevices()
    
    return render_template("IotHome.html",devices=iot_devices)

@app.route('/get-iot-ds')
def get_iot_ds():
    iot_devices = service.getAllDevices()
    l=[]
    for d in iot_devices:
        l.append([d.latitude,d.longitude])
    return jsonify(l)
@app.route('/home')
def home():
    return render_template('Home.html')


@app.route('/iot1dashboard')
def dashboard():
    return render_template('IotDashboard.html')

@app.route('/get-temperature-readings/<string:iot_device_mac>')
def get_temperature_readings(iot_device_mac):
    data = service.getAllTempReadings(iot_device_mac)
    print(data,"-------------------------")
    return jsonify(data)


@app.route('/endDevicePage')
def addEndDevice():
    l=serviceEnd.getEndDevices()
    print(l)
    return render_template('EndDashboard.html',devices=l)

@app.route('/addIotDevice',methods=["POST"])
def addIotDevice():
    name=request.form["name"]
    d=IoT(name,None,None,None,None,None)
    service.addIotDevice(d)
    return redirect('/get-iot-devices')


@app.route('/InfoIot/<string:iot_device_id>')
def InfoIot(iot_device_id):
    return render_template('InfoIotDevicePage.html',id=iot_device_id)


@app.route('/addEndDevice',methods=["POST"])
def test():
    name=request.form["name"]
    ip=request.form["ip"]
    d=EndDevice(name,0,ip,{})
    serviceEnd.addEndDevice(d)
    return redirect("/endDevicePage")


@app.route('/InfoEndDevice/<int:end_device_id>')
def InfoEndDevice(end_device_id):
    return render_template('InfoEndDevicePage.html',id=end_device_id)


@app.route('/GetInfoEndDevice/<int:end_device_id>')
def GetInfoEndDevice(end_device_id):
    d=serviceEnd.getDeviceInfo(end_device_id)
    l=[[],[]]
    for k,v in d.infos.items():
        l[0].append(k)
        l[1].append(v)
    print(l)
    return jsonify(l)

@app.route('/addCity',methods=["POST"])
def addCity():
    name=request.form["name"]
    cityService.AddCity(name)
    return redirect("/getCities")

@app.route('/getCityinfo/<int:id>')
def getCityinfo(id):
    print("////////////")
    l=cityService.getCityById(id)
    print(l)
    return jsonify(l)

@app.route('/getCityinfoPage/<int:id>')
def getCityinfo2(id):
    return render_template('infoCity.html',id=id)

@app.route('/getCities')
def getCityinfos():
    r=cityService.getAllCity()
    return render_template('City.html',devices=r)


@app.route('/getMap')
def getMap():
    return render_template('map.html')
