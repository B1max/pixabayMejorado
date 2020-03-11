import numpy as np
from PIL import Image
from archivos import leer_imagen, escribir_imagen
import threading
import logging
import recursos
import cv2
import os
from skimage import io
import guardar

class Concatenador(threading.Thread):
    carpeta_imagenes = './imagenes'
    inicio = 0
    fin = 0

    logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)
    def __init__(self, sem, nIptico, lst):
        super().__init__()
        self.semaforo = sem
        self.nIptico = nIptico
        self.lst = lst
    
        
    def concatenar_horizontal(self, imagenes):
        alto_minimo = min(im.shape[0] for im in imagenes)

        imagenes_redimensionadas = [cv2.cv2.resize(im, (int(im.shape[1] * alto_minimo / im.shape[0]), alto_minimo))for im in imagenes]

        return cv2.cv2.hconcat(imagenes_redimensionadas)

    def concatenar_vertical(self, imagenes):
        ancho_minimo = min(im.shape[1] for im in imagenes)

        imagenes_redimensionadas = [cv2.cv2.resize(im, (ancho_minimo, int(im.shape[0] * ancho_minimo / im.shape[1])))for im in imagenes]

        return cv2.cv2.vconcat(imagenes_redimensionadas)
    def str2img(self,lst):
        imagenes = []
        try:
            for img in lst:
                imagenes.append(self.leer_imagen(img))
            return imagenes
        except:
            print('error generando lista de lectura de imagenes')

    def procesar(self, imagenesStr):
        # estadoh = True
        # estadov = True
        # # horizontal = ''
        # # nombreH = ''
        # vertical = ''
        # nombreV = ''
        logging.info('concatenar iniciado')
        # while estadoh:
        # while estadoh:
            # try:
        horizontal = self.concatenar_horizontal(self.str2img(imagenesStr))
        nombreH = str(recursos.nConcaEjecutables) +'_concatenacion_horizontal.jpg'
        th = guardar.thGuardar(nombreH,horizontal, recursos.semaforoGuardar, recursos.rutasConcatenadas)
        th.start()
                # th.join()
                # self.escribir_imagen(nombreH, horizontal)
        logging.info('concatenar horizontal terminado(creado th)')
        # estadoh = False
            # except Exception as e:
                # print(e)
                # logging.info(f'Reintentando concatenacion horizontal')
                # estadoh = True
            # finally:
            #     horizontal = ''
            #     nombreH = ''
        recursos.nConcaEjecutables -= 1
        # # while estadov:
        # try:
        #     while vertical is None or nombreV is None:
        #         vertical = self.concatenar_vertical(self.str2img(imagenesStr))
        #         nombreV = str(recursos.nConcaEjecutables) +'_concatenacion_vertical.jpg'
        #         threading.Thread(target=escribir_imagen,args=[nombreV,vertical]).start()
        #         # self.escribir_imagen(nombreV, vertical)
        #     estadov = False
        # except:
        #     logging.info(f'Reintentando concatenacion vertical')
        #     estadov =True
        # finally:
        #     vertical = ''
        #     nombreV = ''



    def armar_ruta(self, nombre):
        return os.path.join(self.carpeta_imagenes, nombre)


    def leer_imagen(self, nombre):
        return io.imread(self.armar_ruta(nombre))


    def escribir_imagen(self, nombre, imagen):
        io.imsave(self.armar_ruta(nombre),imagen)

    def run(self):
        while True:
            self.semaforo.acquire()
            try:
                while recursos.listaConLen() >= self.nIptico:
                    lista = recursos.sacarImagenesConEfectos(self.nIptico)
                    recursos.restarEjecutables()
                    self.procesar(lista)
            finally:
                self.semaforo.release()
            if recursos.nConcaEjecutables <= 0:
                break
