# Project: SmartPulse Monitor

## Objective
Create a robust web application using Flask for the surveillance and prediction of data from two types of devices.

## Monitored Equipment
1. **End Devices:**
   - Utilizing SNMP as the communication protocol.
   - Monitored values: memory usage, CPU load, and disk space usage.

2. **IoT Devices (Simulated):**
   - Periodic transmission of ambient temperature.
   - Communication protocols: MQTT and HTTP.

3. **Open Meteo API Integration:**
   - Retrieving historical precipitation data for a specified city for future predictions.

## Front-end
1. **Authentication:**
   - Admin privileges to manage clients (CRUD operations).
   - Display of a table or map containing added clients.

2. **Data Visualization:**
   - Visual representation of historical data through dynamic curves.
   - Date filter for precise data interval selection.

3. **Client Addition Form:**
   - Collection of essential client information (name, IP or MAC address, longitude, and latitude).
   - Data format: JSON.

## Required Libraries
1. **Communication Protocols:**
   - Flask-MQTT, Paho-MQTT (MQTT).
   - PySNMP (SNMP).
   - Requests (HTTP).

2. **Authentication:**
   - Flask-Login or Flask-JWT-Extended.

3. **Prediction Model:**
   - Scikit-learn for predictions.

4. **Database Integration:**
   - SQLAlchemy or PyMongo.

5. **Data Visualization:**
   - Matplotlib.

## Deployment
   - Deployment using a monitoring image with two Flask services and a chosen database system.
   - Validation from the cloud environment is highly recommended.
