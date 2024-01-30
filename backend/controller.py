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

# MQTT Broker settings
MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_TOPIC = "target/machine/info"

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

from queue import Queue
import subprocess
import json

messages = Queue()  # Shared thread-safe queue
def handle_mqtt():
    command = ["mosquitto_sub", "-h", "test.mosquitto.org", "-t", "target/machine/info"]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, text=True)
    
    try:
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                message_json = output.strip()
                print(f"Received MQTT message: {message_json}")
                message_data = json.loads(message_json)  # Parse the JSON message
                temperature = float(message_data.get('temperature'))
                mac_address = '34.95.40.18'  # Replace with actual MAC address or extract from message if included
                datetime = message_data.get('time')
                if temperature is not None and datetime is not None:
                    message_info = {
                    "temperature": temperature,
                    "mac_address": mac_address,
                    "datetime": datetime
                    }
                    messages.put(message_info)
                    try:
                          IotDao.insertIntoTemperature(temperature, mac_address, datetime)  # Insert into database
                    except Exception as e:
                        print(f"An error occurred: {e}")
    finally:
        process.stdout.close()
        process.wait()

@app.route('/test-iot')
def testIOT1():
    all_messages = []
    while not messages.empty():
        all_messages.append(messages.get())  # Get messages from the queue
    return jsonify(all_messages)

@app.route('/iot1dashboard')
def dashboard():
    return render_template('IotDashboard.html')

@app.route('/get-temperature-readings')
def get_temperature_readings():
    data = IotDao.getAllTempReadings()
    return jsonify(data)
