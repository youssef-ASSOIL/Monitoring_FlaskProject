from flask import (
    Flask,
    jsonify,
    render_template,
    send_file
)
from dal import IotDao
import matplotlib
from matplotlib import pyplot as plt
from io import BytesIO



app=Flask(__name__)
matplotlib.use('agg')

@app.route('/')
def index():
    figure=plt.figure()
    data=IotDao.getAllTemp()
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
    # Use the IotDao to get all IoT devices from the database.
    iot_devices = IotDao.getAllTemp()

    # Convert the devices to a JSON-serializable format
    devices_list = [
        {
            'id': device[0],  
            'mac': device[1], 
            'temp': device[2],  
            'datetime': device[3], 
            'latitude': device[4],
            'longitude': device[5]
        } for device in iot_devices
    ]

    # Return the list of devices as JSON
    return jsonify(devices_list)
@app.route('/home')
def home():
    return render_template('Home.html')