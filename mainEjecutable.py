import logging
import threading
import time
import sys
import recursos
from api import PixabayAPI
from fx import Efectos
from thConcatenador import Concatenador
import thDescargas
    

class MainEjecutable():
    def __init__(self,query,nIptico,imagenesEntotal,descargasEnSimultaneo,efectosEnSimultaneo,nIpticosEnSimultaneo,rotacion,ancho,alto, lstEfectos):
        self.query=query
        self.nIptico=nIptico
        self.imagenesEntotal=imagenesEntotal
        self.descargasEnSimultaneo=descargasEnSimultaneo
        self.efectosEnSimultaneo=efectosEnSimultaneo
        self.nIpticosEnSimultaneo=nIpticosEnSimultaneo
        self.rotacion=rotacion
        self.ancho=ancho
        self.alto=alto
        self.lstEfectos = lstEfectos
        logging.info(f'Buscando imagenes de {query}')


    def iniciar(self):
        semDescargas = threading.Semaphore(3) 
        semFx = threading.Semaphore(1)
        semNipticos = threading.Semaphore(1)

        carpeta_imagenes = './imagenes'
        api = PixabayAPI('15310764-bd15e0c149f0eebab022bf004', carpeta_imagenes)
        recursos.sinEfectos = self.imagenesEntotal
        recursos.conEfectos = self.imagenesEntotal
        recursos.rutasSinConcatenar = self.imagenesEntotal
        if self.imagenesEntotal >= self.nIptico: 
            recursos.resto = self.imagenesEntotal-(self.imagenesEntotal-round(self.imagenesEntotal%self.nIptico))
            recursos.nConcaEjecutables = int((self.imagenesEntotal - recursos.resto)/self.nIptico)
        else:
            recursos.resto = 0
            recursos.nConcaEjecutables = int((self.imagenesEntotal - recursos.resto)/self.nIptico)

        urls = api.buscar_imagenes(self.query, self.imagenesEntotal)
        urlsLista = []
        for u in urls:
            urlsLista.append(u)
            recursos.descargadas+=1
        print(f'imagenes descargadas{len(urlsLista)}')


        for _ in range(self.descargasEnSimultaneo):
            t = thDescargas.HiloDescarga(urlsLista, semDescargas, api)
            t.start()

        imgDescargadas = api.rutasImgDescargadas()

        for _ in range(self.efectosEnSimultaneo):
            th = Efectos( semFx, imgDescargadas, self.rotacion, self.ancho, self.alto, self.lstEfectos)
            th.start() 


        for _ in range(self.nIpticosEnSimultaneo):
            th = Concatenador(semNipticos, self.nIptico, recursos.rutasConEfectos)      
            th.start()
