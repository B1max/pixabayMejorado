import logging
from api import PixabayAPI
import threading
import time
import requests
import json
import os
import archivos
import recursos

class HiloDescarga(threading.Thread):
    logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S',
                        level=logging.INFO)
    url = ''
    carpeta_imagenes = './imagenes'



    def __init__(self, _url, _semaforo, _api):
        super().__init__()
        self.semaforo = _semaforo
        self.url = _url
        self.api = _api



    def descargar_imagen(self, url):
        if recursos.debug : logging.info(f'----Descarga iniciada url:{url}')

        bytes_imagen = requests.get(url)

        nombre_imagen = url.split('/')[-1]

        ruta_archivo = os.path.join(self.carpeta_imagenes, nombre_imagen)
        
        with open(ruta_archivo, 'wb') as archivo:
            archivo.write(bytes_imagen.content)

        if recursos.debug : logging.info(f'Descarga finalizada {url}')

        recursos.rutasSinEfectos.append(nombre_imagen)
        


    def run(self):
        while True:
            self.semaforo.acquire()
            try:
                if len(self.url)>0:
                    self.descargar_imagen(self.url.pop(0))
            finally:
                self.semaforo.release()
            if len(recursos.rutasSinEfectos) == recursos.descargadas:
                break
