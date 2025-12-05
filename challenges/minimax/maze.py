import os
import random
import math
# importacion es para limpiar la consola, movimiento random de raton y math para ls distancia
# defino una variable para elegir el laberinto
maze = 0
# uso un bucle para qu emientras no sea una de las respoestas solicitadas no pare
# crear tablero bidimencional
while maze != 1 and maze != 2:
    maze = int(input("modo de jueg0 1 o 2: "))
    laberinto = []
    if maze == 1:
        laberinto = [
            list("@@@@@@@@@@@@@@@@@@@"),
            list("@#################@"),
            list("@#      #        #@"),
            list("@## ### #####  # #@"),
            list("@##😾##🐭        # #@"),
            list("@## ###### ##### #@"),
            list("@##              #@"),
            list("@## ##############@"),
            list("@@@@@@@@@@@@@@@@@@@")
        ]
    elif maze == 2:
        laberinto = [
            list("@@@@@@@@@@@@@@"),
            list("@######## ###@"),
            list("@#😾   #      @"),
            list("@### #### ###@"),
            list("@###      ###@"),
            list("@####🐭### ###@"),
            list("@# ## # # ###@"),
            list("@# ## # # ###@"),
            list("@# ## # # ###@"),
            list("@# ## # # ###@"),
            list("@# ## # # ###@"),
            list("@#        ###@"),
            list("@######## ###@"),
            list("@#      # ###@"),
            list("@# #### # ###@"),
            list("@# #🧀   # ###@"),
            list("@# ###### ###@"),
            list("@#        ###@"),
            list("@############@"),
            list("@@@@@@@@@@@@@@")
        ]
    else:
        print("1 o 2 nomas era")

# uso un bucle for para recorrer la lista de listas e imprimir su contenido con espacio
# gestionar
def mostrar():
    for fila in laberinto:
        print("   ".join(fila))#join inserta caracteres en medio


jugador = 0

#esta funcion pide input para guardar una variable con el personaje qu eel usuario va a estar usando
def modoDeJuego():
    print("como queres juegar?")
    print("1 -queres ser el gato?")
    print("2- queres ser el raton")
    print("3 -queres que la computadora juegue con ella misma?")
    jugador = int(input())
    match jugador:
        case 1:
            jugador = "gato"
        case 2:
            jugador = "raton"
        case 3:
            jugador = "computadora"
        case _:
            print("intenta usar una opcion valida")
            return modoDeJuego()
    return jugador

# aca esta funcion coordenadas o puntos como parametros y calcula la distancia usando la  formula euclidiana
# the manhattan one just didint work for me
def distancia(a, b):
    return math.dist(a, b)

# here is basically the same as the choose character one pero en vez de gauradr en un avriable retorna 
def WASD(position):
    x, y = position
    dir = input().lower()#el lower es para convertir a minuscula
    match dir:
        case "w":
            return (x, y - 1)
        case "a":
            return (x - 1, y)
        case "s":
            return (x, y + 1)
        case "d":
            return (x + 1, y)
        case _:
            print("usa W A S D")
            return WASD(position)#si no ingresa un valor valido vuelve a llamar a si misma

#here i used enumerate bc its basically for for obtaining indexes, it returns the number and the contents wich helps me get the coordenates
def encontrar(player):
    for y, fila in enumerate(laberinto):
        for x, cell in enumerate(fila):
            if cell == player:#si el contendio de la celda es igual al jugador que esta buscando entonces y solo enconces retorna la coordenada que seria la posicion del jugador
                return (x, y)
    return None# si no esta en la tabla devuelve none

#esta funcion es para efinir hacia donde se puede mover cada personaje
def movimientosPosibles(posicion, isMouse=False):
    x, y = posicion
    valid = []
    # The line `posibles = [(x, y - 1), (x - 1, y), (x, y + 1), (x + 1, y)]` is creating a list of possible movements in a grid based on the current position `(x, y)`. Each tuple in the list represents a potential movement in a specific direction:
    posibles = [(x, y - 1), (x - 1, y), (x, y + 1), (x + 1, y)]#esto es arriba, abajo, derecha y izquierda
    for x1, y1 in posibles:
        if 0 <= y1 < len(laberinto) and 0 <= x1 < len(laberinto[y1]):#esto es para ver si esta dentro del rango del laberinto
            cell = laberinto[y1][x1]
            if cell != "#":#si el movimiento no es una pared entonces es valido
                if isMouse or (cell != "🧀"): # si el personaje es el raton o el movimiento no es queso lo guarda como valido
                    valid.append((x1, y1))
    return valid

#depth is like how deep into the three it ill see
def minimax(posCat, posMouse, depth, turno):
    if posCat == posMouse:# si el el rato fue atrapado termina
        return 0
    if depth == 0:
        return distancia(posCat, posMouse)#cuando la profundidad llega a 0 devuelve la distancia que es lo que va a comparar
    if turno:
        mejor = float("inf")
        for movimiento in movimientosPosibles(posCat, isMouse=False):#hace todos los movimientos posibles(more like it imagines bc it doest actually moves it)
            val = minimax(movimiento, posMouse, depth - 1, False)
            if val < mejor:
                mejor = val#compara el valor del numero grande y si es menor al valor retornado lo guarda
        return mejor
    else:
        mejor = float("-inf")
        for movimiento in movimientosPosibles(posMouse, isMouse=True):
            if laberinto[movimiento[1]][movimiento[0]] == "🧀" or laberinto[movimiento[1]][movimiento[0]] == "@":#condicion para hace rmas atractivas las salidas y el queso
                return 999
            else:
                val = minimax(posCat, movimiento, depth - 1, True)
            if val > mejor:
                mejor = val
        return mejor


contador = 0
lastCat = None
lastMouse = None


def move():
    global contador#global lets me pull a avariable from outside my function
    global lastCat
    global lastMouse

    posCat = encontrar("😾")
    posMouse = encontrar("🐭")#busca las posiciones de los personajes

    if posMouse is None:#estos checks se hacen en muchas partes para los mensajes diferentes
        print("el raton fue comido")#si el raton no se pued enecontrar termina
        mostrar()
        exit()

    # turno manual del gato ----------------------------------------------------------------------------------------------------------------------------------
    if jugador == "gato":#condiciones para saber que jugador es
        print("tu turno W A S D ?")
        nuevo = WASD(posCat)
        x1, y1 = nuevo
        if 0 <= y1 < len(laberinto) and 0 <= x1 < len(laberinto[y1]) and laberinto[y1][x1] != "#":#validar que el movimiento elegido sea valido
            x, y = posCat
            laberinto[y][x] = " "
            laberinto[y1][x1] = "😾"
            posCat = nuevo

            if posCat == posMouse:
                print("atraspaste al gato")
                mostrar()
                exit()
        else:
            print("proba un movimiento valido ok?")

    posCat = encontrar("😾")
    posMouse = encontrar("🐭")

    if posMouse == posCat:
        print("el raton fue comido")
        mostrar()
        exit()

    # gato pero computaodra -------------------------------------------------------------------------------------------------------------------------------------
    if jugador != "gato":
        mejorMovimiento = None
        mejor = float("inf")
        mejorDistancia = float("inf")  

        for movimiento in movimientosPosibles(posCat, isMouse=False):
            penalize = 0
            if movimiento == lastCat:
                penalize = 5
            val = minimax(movimiento, posMouse, depth=7, turno=False) + penalize
            dist = distancia(movimiento, posMouse)
            # si 5 < 5      o   5  == 5       y  3   <   6  true
            #si minimax devuelve el mismo valor pero la distancia es menor la sigue guardando ya que es mas cercano aunque tenga el mismo valor
            if val < mejor or (val == mejor and dist < mejorDistancia):#here it uses the distance to kinda desmpatar in case the val is the same as teh last mejor it uses the distance
                mejor = val
                mejorDistancia = dist
                mejorMovimiento = movimiento
            
            # if val < mejor:
            #     mejor = val
            #     mejorMovimiento = movimiento

        if mejorMovimiento:
            x, y = posCat
            x1, y1 = mejorMovimiento
            laberinto[y][x] = " "
            laberinto[y1][x1] = "😾"

            lastCat = (x, y)

            posCat = encontrar("😾")
            posMouse = encontrar("🐭")

            if posCat == posMouse :
                laberinto[posMouse[1]][posMouse[0]] = "😾"
                print("el gato comio al raton")
                mostrar()
                exit()

        posMouse = encontrar("🐭")
        if posMouse is None:
                print("el raton fue comido")
                mostrar()
                exit()
# playrer human rat =-----------------------------------------------------------------------------------------------------------------------
    if jugador == "raton":
        print("turno del raton W A S D")
        nuevo = WASD(posMouse)
        x1, y1 = nuevo
        if 0 <= y1 < len(laberinto) and 0 <= x1 < len(laberinto[y1]) and laberinto[y1][x1] != "#":

            if laberinto[y1][x1] == "@" or laberinto[y1][x1] == "🧀":
                print("ganaste")
                mostrar()
                exit()

            x, y = posMouse
            laberinto[y][x] = " "
            laberinto[y1][x1] = "🐭"
            posMouse = nuevo

            if nuevo == posCat:
                print("te agarro el gato")
                mostrar()
                exit()
        else:
            print("cant")

        mostrar()
        return

    # rat computer ---------------------------------------------------------------------------------------------------------------
    if jugador != "raton":
        posMouse = encontrar("🐭")
        posCat = encontrar("😾")

        if posMouse is None:
                print("el raton fue comido")
                mostrar()
                exit()

        mejorMovimiento = None
        mejor = float("-inf")

        posibles = movimientosPosibles(posMouse, isMouse=True)
        if not posibles:
            print("el raton no tiene salida")
            exit()

        for movimiento in posibles:
            if laberinto[movimiento[1]][movimiento[0]] == "@" or laberinto[movimiento[1]][movimiento[0]] == "🧀":
                laberinto[posMouse[1]][posMouse[0]] = " "
                laberinto[posCat[1]][posCat[0]] = "😿"
                mostrar()
                print("she got awaaaaay")
                exit()

            penalize = 0
            if lastMouse == movimiento:
                penalize = 5

            val = minimax(posCat, movimiento, depth=10, turno=True) - penalize#made her smarter bc she was kinda dumb
            if val > mejor:
                mejor = val
                mejorMovimiento = movimiento

        if mejorMovimiento:
            x, y = posMouse
            if contador < 2:
                mov = movimientosPosibles(posMouse, isMouse=True)
                x1, y1 = random.choice(mov)
                contador += 1
            else:
                x1, y1 = mejorMovimiento

            if not (0 <= y1 < len(laberinto) and 0 <= x1 < len(laberinto[y1])):
                laberinto[y][x] = " "
                print("¡El ratón escapó!")
                return

            if laberinto[y1][x1] == "😾":
                print("¡El gato atrapó al ratón!")
                mostrar()
                exit()#exit closes the program

            laberinto[y][x] = " "
            laberinto[y1][x1] = "🐭"
            lastMouse = (x, y)

    mostrar()


mostrar()
jugador = modoDeJuego()

while True:
    if jugador == "computadora":
        input("enter para mover ")
        os.system("cls")
    else:
        os.system("cls")
        mostrar()
    move()
