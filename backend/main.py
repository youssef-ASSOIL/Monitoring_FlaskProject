from controller import app
import threading
from controller import handle_mqtt
if __name__ == '__main__':
    mqtt_thread = threading.Thread(target=handle_mqtt, daemon=True)
    mqtt_thread.start()
    app.run(debug=True,host='0.0.0.0',port=8080)