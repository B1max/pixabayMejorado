import requests
import json
import os


class PixabayAPI():


    def __init__(self, key, carpeta_imagenes):
        self.key = key
        self.carpeta_imagenes = carpeta_imagenes
        self.imagenesDescargadas = []



    def buscar_imagenes(self, query, cantidad):

        url = f'https://pixabay.com/api/?key={self.key}&per_page={cantidad}&q={query}&image_type=photo&lang=es'

        response = requests.get(url)
        jsonResponse = json.loads(response.text)
        return map(lambda h: h['largeImageURL'], jsonResponse['hits'])

   
    def rutasImgDescargadas(self):
        return self.imagenesDescargadas
