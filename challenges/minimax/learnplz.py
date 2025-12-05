import math
import random
import os
mode = 0
while mode != 1 and mode != 2:
    mode = int(input("ingrese 1 para modo facil y 2 para modo dificil: "))
    laberinto = []
    if mode == 1:
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
        
    elif mode == 2:
        laberinto = [
            list("@@@@@@@@@@@@@@"),
            list("@######## ###@"),
            list("@#😾   #    @"),
            list("@### #### ###@"),
            list("@###      ###@"),
            list("@####🐭### ###@"),
            list("@# ## #🧀# ###@"),
            list("@# ## # # ###@"),
            list("@# ## # # ###@"),
            list("@# ## # # ###@"),
            list("@# ## # # ###@"),
            list("@#        ###@"),
            list("@######## ###@"),
            list("@#      # ###@"),
            list("@# #### # ###@"),
            list("@# #    # ###@"),
            list("@# ###### ###@"),
            list("@#        ###@"),
            list("@############@"),
            list("@@@@@@@@@@@@@@")
    ]
    else:
        print("1 o 2 nomas era")
            



def mostrarLaberinto():
    for fila in laberinto:
        print(" ".join(fila))# esta funcion imprime las matrices recorriendolas con dos bucles for que utilizan su propio largo para que se pueda usar en matrices de tamanos diferentes
    
    
    
    
def distancia(a,b):# math.dist usa la formula euclidiana para calcular la distancia entre dos puntos(como pitagoras)
    return math.dist(a,b)




def encontrar(animal):# this function checks the whole matrix and if it finds that the value of the current cell is the same as the parameter it returns it, this is to get the coordenates of the cat or mouse
    for y, fila in enumerate(laberinto):
        for x, celda in enumerate(fila):
            if celda == animal:
                return(x,y)
    return None
    
    
    
    
    
def movimientosValidos(posicion, isMouse = False):#here the parameters are the position x,y of  the character and a sorta checker . if it its the mouse it has the posibility to run out of the maze(laberinth)
    x,y = posicion
    direcciones=[(x+1,y),(x-1,y),(x,y+1),(x,y-1)]#aca  se mueve una posicion arriba, abajo , derecha y izquierda
    valid=[]#lista vacia
    for x1, y1 in direcciones:
        if 0 <= y1 < len(laberinto) and 0 <= x1 < len(laberinto[y1]):#aca si la poscicon actual en y es mayorigual a cero y menor a la longitud del laberinto y x es menor igual a 0 y menor a la altura del laberinto (pyhton usa al reves x, y ), esto es para que no salga del rango
                celda = laberinto[y1][x1]
                if celda != "#":
                    if isMouse or celda != "🧀" or celda != "@":# el or devuelve true y pasa solo con un true, si era isMouse= true osea es el gato. no iba a gurdar la posicion de barrera con una posible movimiento
                        valid.append((x1,y1))#and here it saves the positions in valid
    return valid
    
    
    
    
    
def minimax(posCat,posMouse,depth,turno):#true es gato y false raton
    if posCat == posMouse:#si el gato alcanzo al raton se corta
        return 0
    if depth == 0:
        return distancia(posCat,posMouse) #si la profundidad alcanza 0 devuleve la distancia
    
    if turno:
        mejor= float("inf")#inf es un numero muy grande ya que el objetivo del gato es minimizar
        for movimiento in movimientosValidos(posCat):#aca recorre todos los movimientos validos
            val=minimax(movimiento,posMouse,depth - 1,False) #here each iteration sends one of the valid movements, the position of the mouse, reduces depth and changes the turn to the mouse
            if val < mejor:
                mejor = val                         #movimiento representa cual de los personajes se esta moviendo
        return mejor
    else:
        mejor = float("-inf")
        for movimiento in movimientosValidos(posMouse, isMouse=True):
            if laberinto[movimiento[1]][movimiento[0]] == "🧀":#aca si el movimiento es una salida la prioriza subiendo su valor
                return 999
            val = minimax(posCat, movimiento, depth - 1, True)
            if val > mejor:
                mejor = val
        return mejor





contador = 0
lastCat = None
lastMouse = None

def Mover():
    global lastCat
    # The line `global lastMouse` is declaring the variable `lastMouse` as a global variable within the function `Mover()`. By using the `global` keyword, you are telling the Python interpreter that when you refer to `lastMouse` within the `Mover()` function, you are referring to the global variable `lastMouse` defined outside of the function.
    global lastMouse
    global contador
    

    posCat = encontrar("😾") #usa la funcion encontrar para busacr las coordenadas del gato y del raton
    posMouse = encontrar("🐭")
    if posMouse is None:
        return

    mejorMovimiento = None #variable paar guaradr el mejor movimiento
    mejor = float("inf")
    
    for movimiento in movimientosValidos(posCat):
        penalize = 0
        if lastCat == movimiento:
            penalize = 5
        val = minimax(movimiento, posMouse, depth=6, turno=False)+ penalize
        if val < mejor:
            mejor = val
            mejorMovimiento = movimiento

    if mejorMovimiento:# aca se "mueve" el gato usando la posicion acula y la mejor opcion
        x,y = posCat
        x1,y1= mejorMovimiento
        laberinto[y][x] = " "
        laberinto[y1][x1] = "😾"
        
        lastCat = (x,y)
        posCat = encontrar("😾")
        posMouse = encontrar("🐭")
        
        if posCat == posMouse and posMouse is not None:
            laberinto[posMouse[1]][posMouse[0]] = "😾"
            print("te comio el gato")
            mostrarLaberinto()
            exit()
        if posMouse is None:
            print("te comio el gato")
            mostrarLaberinto()
            exit()

    posMouse = encontrar("🐭")
    posCat = encontrar("😾")
    if posMouse is None:
        return

    mejorMovimiento = None
    mejor = float("-inf")
    
    posibles = movimientosValidos(posMouse, isMouse=True)
    if not posibles:
        laberinto[posMouse[1]][posMouse[0]] = " "
        print("se perdio")
        return
    
    for movimiento in posibles:
        
        if laberinto[movimiento[1]][movimiento[0]] == "🧀" or laberinto[movimiento[1]][movimiento[0]] == "@":
            laberinto[posMouse[1]][posMouse[0]] = " "
            mostrarLaberinto()
            print("el raton  gano")
            exit()
        
        penalize = 0
        if lastMouse == movimiento:
            penalize = 5

        val = minimax(posCat, movimiento, depth=8, turno=True) - penalize

        if val > mejor:
            mejor = val
            mejorMovimiento = movimiento
            
            
    if mejorMovimiento:
        x,y = posMouse
        
        if contador < 2:
            mov = movimientosValidos(posMouse, isMouse=True)
            x1,y1 = random.choice(mov)
            contador += 1
        else:
            x1, y1 = mejorMovimiento

        if not(0 <= y1 < len(laberinto) and 0 <= x1 < len(laberinto[y1])):
            laberinto[y][x] = " "
            print("she got away")
            return
            
        if laberinto[y1][x1] == "😾":
            print("busted")
            mostrarLaberinto()
            return

    laberinto[y][x] = " "
    laberinto[y1][x1] = "🐭"
    lastMouse = (x,y)
    mostrarLaberinto()

    
mostrarLaberinto()

while True:
    input("Enter para mover:")
    os.system("cls")
    Mover()
