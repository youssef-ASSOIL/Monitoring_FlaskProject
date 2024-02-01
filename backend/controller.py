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

app=Flask(__name__)
matplotlib.use('agg')


serve=AppService(IotDao(),EndDao())
serve.start()
service = IotService()
serviceEnd = EndService()

@app.route('/')
def index():
    figure=plt.figure()
    data=service.getAllTemp()
    temp=[]
    dates=[]
    for id,mac,t,date,L,l in data:
        temp.append(t)
        dates.append(date)
    plt.plot(dates,temp)
    img=BytesIO()
    figure.savefig(img)
    img.seek(0)
    return send_file(img,mimetype='image/png')


@app.route('/get-iot-devices')
def get_iot_devices():
    iot_devices = service.getAllDevices()
    
    return render_template("IotHome.html",devices=iot_devices)
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
    return render_template('index.html')


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

