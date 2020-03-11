import matplotlib.image as mpimg
from skimage import exposure, transform, io
from skimage.color import rgb2gray
import threading
import logging
from archivos import leer_imagen, escribir_imagen
import recursos
import os
import guardar

class Efectos(threading.Thread):
    carpeta_imagenes = './imagenes'

    inicio= 0
    fin= 0
    imag=''
    logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)
    def __init__(self, semaforo, lst, rotar, ancho, alto, listaEfectos):
        super().__init__()
        self.semaforo = semaforo
        self.lst = lst
        self.rotar = rotar
        self.ancho = ancho
        self.alto = alto
        self.listaEfectos = listaEfectos

    def procesar(self, img):
        log=0
        logging.info('efecto iniciado')
        try:
            imagen = leer_imagen(img)
            if "contraste" in self.listaEfectos:  
                imagen = self.contraste_adaptativo(imagen)
                log=1
            if "rotacion" in self.listaEfectos:  
                imagen = self.rotacion(imagen, self.rotar)
                log=2
            if "redimencion" in self.listaEfectos:  
                imagen = self.redimensionar(imagen, self.ancho, self.alto)
                log=3
            if "escalagris" in self.listaEfectos: 
                imagen = rgb2gray(imagen)
                log=4
        except:
            logging.info(f'error aplicando efectos, volviendo a intentar...log({log})')
            self.procesar(img)
        finally:
            # grabar = True
            # while grabar:
                # try:
            th = guardar.thGuardar(f'conEfectos_{img}',imagen, recursos.semaforoGuardar,recursos.rutasConEfectos)
            th.start()
                    # escribir_imagen(f'conEfectos_{img}', imagen)
                # except:
                #     print('error grabando imagen')
            
            # recursos.rutasConEfectos.append(f'conEfectos_{img}')
            logging.info('efecto terminado')


    def contraste_adaptativo(self,img):
        return exposure.equalize_adapthist(img, clip_limit=0.03)


    def rotacion(self,img, angulo):
        return transform.rotate(img, angulo)


    def redimensionar(self,img, ancho, alto):
        return transform.resize(img, (ancho, alto))


    def run(self):
        while True:
            self.semaforo.acquire()
            try:
                if len(recursos.rutasSinEfectos)>0:
                    self.imag = recursos.rutasSinEfectos.pop(0)
            finally:
                self.semaforo.release()
            if self.imag != '' : self.procesar(self.imag)
            self.imag = ''

