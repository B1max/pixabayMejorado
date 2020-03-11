from mainEjecutable import MainEjecutable
respuesta = 0
respuestasPosibles = [1,2]
while not respuesta in respuestasPosibles:
        respuesta = int(input('ingrese (1) para modo Automatico / (2)-para modo manual parametrizado:'))
if  respuesta == 1:
        query ="random"
        nIptico = 10
        imagenesEntotal = 10
        descargasEnSimultaneo = 5
        #si sobrepasa los 5 efectos en simultaneo se va de memoria..
        efectosEnSimultaneo = 5 
        nIpticosEnSimultaneo = 2
        rotacion = 20
        ancho = 500
        alto = 500
        # posibles efectos : contraste, rotacion, redimencion, escalagris
        efectosAplicados = ["contraste"]
if  respuesta == 2:
        query = str(input('ingrese la imagen a buscar:'))

        nIptico = int(input('ingrese la cantidad de nIpticos a buscar:'))

        imagenesEntotal = int(input('ingrese la cantidad de imagenes que desea buscar:')) 

        descargasEnSimultaneo = int(input('ingrese la cantidad de imagenes que desea bajar en simultaneo:'))

        efectosEnSimultaneo = int(input('ingrese la cantidad de efectos que desea bajar en simultaneo:'))

        nIpticosEnSimultaneo = int(input('ingrese la cantidad de nIpticos que desea bajar en simultaneo:'))

        rotacion = 20
        ancho = 500
        alto = 500
        
        listaDeEfectos =  ['contraste', 'rotacion', 'redimencion', 'escalaGrises']

        efectosAplicados = []

        for fx in listaDeEfectos:
                ingreso = str(input(f'Desea aplicar el efecto {fx} ? : (si/no)'))
                if ingreso == "si": efectosAplicados.append(fx)


ejecutar = MainEjecutable(query,nIptico,imagenesEntotal,descargasEnSimultaneo,efectosEnSimultaneo,nIpticosEnSimultaneo,rotacion,ancho,alto,efectosAplicados)
ejecutar.iniciar()
