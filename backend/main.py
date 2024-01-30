from controller import app
from service import AppService
if __name__ == '__main__':
    serve=AppService()
    serve.start()
    app.run(debug=True,host='0.0.0.0',port=8080)