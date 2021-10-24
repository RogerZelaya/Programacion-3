#IMPORAR LAS LIBRERIAS 
import tensorflow as tf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

from urllib import parse
from http.server import HTTPServer, BaseHTTPRequestHandler

class servidorBasico(BaseHTTPRequestHandler):
    def do_GET(self):
        print("Peticion GET recibida")
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write('Server iniciado en el puerto 3006'.encode())


    def do_POST(self):
        print("POST")
        content_length = int(self.headers['Content-Length'])
        data = self.rfile.read(content_length)
        data = data.decode()
        data = parse.unquote(data)
        data = float(data)

        predict = modelo.predict([data])
        print('La predicción fue:', predict)
        predict = str(predict[0][0])
        
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(predict.encode())


Cefar = pd.read_csv("celsius-a-fahrenheit.csv", sep=";")
sb.scatterplot(Cefar["celsius"], Cefar["fahrenheit"])

#Crear los inputs y ouputs
ccs = Cefar["celsius"]
fahren = Cefar["fahrenheit"]

#creando el modelo de entrenamiento
modelo = tf.keras.Sequential()
modelo.add(tf.keras.layers.Dense(units=1, input_shape=[1]))

#compilar el modelo de entrenamiento
modelo.compile(optimizer=tf.keras.optimizers.Adam(1), loss='mean_squared_error')

#entrenar el modelo de IA
historial = modelo.fit(ccs,fahren,epochs=350)

fahrenheit = modelo.predict([1200])
print(fahrenheit)

print('Servidor iniciado')
server = HTTPServer(('localhost', 3006), servidorBasico)
server.serve_forever()