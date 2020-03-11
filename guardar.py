from skimage import io, img_as_ubyte
import threading
from pathlib import Path
import time
class thGuardar(threading.Thread):

    directorio_actual = Path.cwd()

    def __init__(self, imgName, imagen, semaforo, lstDestino):
        super().__init__()
        self.imagen = imagen
        self.semaforo = semaforo
        self.imgName = imgName
        self.lstDestino = lstDestino

    def armar_ruta(self, nombre):
        return (self.directorio_actual / 'imagenes' / nombre).resolve()

    def leer_imagen(self, nombre):
        return io.imread(self.armar_ruta(nombre))

    def escribir_imagen(self):
        try:
            ruta = self.armar_ruta(self.imgName)
            if not (ruta is None):
                io.imsave(ruta, img_as_ubyte(self.imagen))
            else:
                print('ruta no definida')
            self.lstDestino.append(self.imgName)
            print('archivo guardado')
            return True
        except Exception as e:
            print(e)
            time.sleep(1)
            return False

    def run(self):
        self.semaforo.acquire()
        try:
            while not self.escribir_imagen():
                continue
            print('aparentemente lo guarde')
        except:
            print('aparentemente no pude guardar')
        finally:
            self.semaforo.release()
