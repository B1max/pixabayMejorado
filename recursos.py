import threading
import logging
monitorUltimoNiptico = threading.Condition()
semaforoGuardar = threading.Semaphore(1)
rutasSinEfectos = []
rutasConEfectos = []
rutasConcatenadas = []
rutasSinConcatenar = 0
nConcaEjecutables = 0
conEfectos = 0
descargadas=0
resto = 0
debug = True
fxContinuar = True
concatContinuar = True

semConEfectos = threading.Semaphore(1)


alerta = True
def sacarImagenesConEfectos(cant):
    global alerta
    listaImg = []
    semConEfectos.acquire()
    for _ in range(cant):      
        try:
            if hayItemsConFX:
                listaImg.append(rutasConEfectos.pop(0))
            else:
                logging.info('no se pudo obtener la lista, no hay elementos')
        except:
            if alerta : 
                logging.info('no se pudo obtener la lista')
                alerta = False
        finally:
            semConEfectos.release()
    return listaImg

def hayItemsConFX():
    return listaConLen > 0

def listaConLen():
    return int(len(rutasConEfectos))

def restarEjecutables():
    global nConcaEjecutables
    nConcaEjecutables = int(nConcaEjecutables) -1  