import os
import math
import random

dificultad = 0
while dificultad != 1 and dificultad != 2:
    dificultad = int(input("elige 1 para facil o 2 para dificil: "))
    laberinto = []
    if dificultad == 1:
        laberinto = [
            list("@@@@@@@@@@@@@@@@@@@"),
            list("@#################@"),
            list("@#      #        #@"),
            list("@## ### #####  # #@"),
            list("@##😾##🐭       # #@"),
            list("@## ###### ##### #@"),
            list("@##              #@"),
            list("@## ##############@"),
            list("@@@@@@@@@@@@@@@@@@@")
        ]
    elif dificultad == 2:
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

control = ""

def quienJuega():
    print("Quién querés controlar?")
    print("1 = gato manual")
    print("2 = ratón manual")
    print("3 = IA vs IA")

    control = int(input("Elige: "))

    match control:
        case 1:
            control = "gato"
        case 2:
            control = "raton"
        case 3:
            control = "ninguno"
        case _:
            print("1, 2 y 3 claramente decia")
            return quienJuega()
    return control

def WASD(pos):
    x, y = pos
    direccion = input().lower()  # Sin mensaje, solo lee la tecla
    match direccion:
        case "w":
            return (x, y-1)  # Arriba
        case "s":
            return (x, y+1)  # Abajo
        case "a":
            return (x-1, y)  # Izquierda
        case "d":
            return (x+1, y)  # Derecha
        case _:
            print("Usa W, A, S o D")
            return WASD(pos)

def mostrar():
    for fila in laberinto:
        print(" ".join(fila))

def distancia(a, b):
    return math.dist(a, b)

def encontrar(character):
    for y, fila in enumerate(laberinto):
        for x, celda in enumerate(fila):
            if celda == character:
                return (x, y)  # CORREGIDO: (x, y) como en el original
    return None

def valMove(posicion, isMouse=False):
    x, y = posicion  # CORREGIDO: x, y
    moves = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
    valid = []
    for x1, y1 in moves:
        if 0 <= y1 < len(laberinto) and 0 <= x1 < len(laberinto[y1]):
            celda = laberinto[y1][x1]
            if celda != "#":
                if isMouse or (celda != "🧀" and celda != "@"):  # CORREGIDO
                    valid.append((x1, y1))
    return valid

def minimax(posCat, posMouse, depth, turno):
    if posMouse == posCat:
        return 0
    if depth == 0:
        return distancia(posCat, posMouse)
    
    if turno:  # Turno del gato (minimizar distancia = atrapar)
        mejor = float("inf")
        for movimiento in valMove(posCat):
            val = minimax(movimiento, posMouse, depth - 1, False)
            if val < mejor:
                mejor = val
        return mejor
    else:  # Turno del ratón (maximizar distancia = escapar)
        mejor = float("-inf")
        for movimiento in valMove(posMouse, isMouse=True):
            if laberinto[movimiento[1]][movimiento[0]] == "🧀" or laberinto[movimiento[1]][movimiento[0]] == "@":
                return 999  # El ratón puede escapar - MUY BUENO
            val = minimax(posCat, movimiento, depth - 1, True)
            if val > mejor:  # Busca MAYOR distancia del gato
                mejor = val
        return mejor

contador = 0
lastCat = None
lastMouse = None

def Mover():
    global contador
    global lastCat
    global lastMouse

    posCat = encontrar("😾")
    posMouse = encontrar("🐭")
    
    if posMouse is None:
        return
    
    # ===== MOVIMIENTO MANUAL DEL GATO =====
    if control == "gato":
        print("Tu turno (Gato) - W/A/S/D:")
        nuevo = WASD(posCat)
        x1, y1 = nuevo
        if (0 <= y1 < len(laberinto) and 
            0 <= x1 < len(laberinto[y1]) and 
            laberinto[y1][x1] != "#"):
            
            x, y = posCat
            laberinto[y][x] = " "
            laberinto[y1][x1] = "😾"
            posCat = nuevo
            
            if posCat == posMouse:
                print("¡Atrapaste al ratón!")
                mostrar()
                exit()
        else:
            print("Movimiento inválido")
        
        # CORREGIDO: NO hacer return aquí, continuar con el movimiento del ratón IA
        posCat = encontrar("😾")
        posMouse = encontrar("🐭")
        
        if posMouse is None:
            return
    
    # ===== MOVIMIENTO IA DEL GATO =====
    if control != "gato":  # CORREGIDO: Solo mover gato IA si NO es manual
        mejorMovimiento = None
        mejor = float("inf")
        
        for movimiento in valMove(posCat):
            penalize = 0
            if movimiento == lastCat:
                penalize = 5
            val = minimax(movimiento, posMouse, depth=6, turno=False) + penalize
            if val < mejor:
                mejor = val
                mejorMovimiento = movimiento
        
        if mejorMovimiento:
            x, y = posCat
            x1, y1 = mejorMovimiento
            laberinto[y][x] = " "
            laberinto[y1][x1] = "😾"
            
            lastCat = (x, y)  # Guardar posición anterior
            posCat = encontrar("😾")
            posMouse = encontrar("🐭")
            
            if posCat == posMouse and posMouse is not None:
                laberinto[posMouse[1]][posMouse[0]] = "😾"
                print("¡El gato atrapó al ratón!")
                mostrar()
                exit()
            
            if posMouse is None:
                print("¡El gato atrapó al ratón!")
                mostrar()
                exit()
    
    # ===== MOVIMIENTO MANUAL DEL RATÓN =====
    if control == "raton":
        print("Tu turno (Ratón) - W/A/S/D:")
        nuevo = WASD(posMouse)
        x1, y1 = nuevo
        if (0 <= y1 < len(laberinto) and 
            0 <= x1 < len(laberinto[y1]) and 
            laberinto[y1][x1] != "#"):
            
            if laberinto[y1][x1] == "@" or laberinto[y1][x1] == "🧀":
                x, y = posMouse
                laberinto[y][x] = " "
                mostrar()
                print("¡Escapaste! Ganaste!")
                exit()
            
            x, y = posMouse
            laberinto[y][x] = " "
            laberinto[y1][x1] = "🐭"
            posMouse = nuevo
            
            if nuevo == posCat:
                print("¡Te atrapó el gato!")
                mostrar()
                exit()
        else:
            print("Movimiento inválido")
        
        mostrar()
        return
    
    # ===== MOVIMIENTO IA DEL RATÓN =====
    if control != "raton":  # CORREGIDO: Solo mover ratón IA si NO es manual
        posMouse = encontrar("🐭")
        posCat = encontrar("😾")
        
        if posMouse is None:
            return
        
        mejorMovimiento = None
        mejor = float("-inf")  # El ratón quiere MAXIMIZAR (alejarse del gato)
        
        posibles = valMove(posMouse, isMouse=True)
        if not posibles:
            laberinto[posMouse[1]][posMouse[0]] = " "
            print("¡El ratón no tiene salida!")
            exit()
        
        for movimiento in posibles:
            if laberinto[movimiento[1]][movimiento[0]] == "@" or laberinto[movimiento[1]][movimiento[0]] == "🧀":
                laberinto[posMouse[1]][posMouse[0]] = " "
                mostrar()
                print("¡El ratón escapó!")
                exit()
            
            penalize = 0
            if lastMouse == movimiento:
                penalize = 5
            # CORREGIDO: turno=True porque estamos evaluando el SIGUIENTE turno (del gato)
            val = minimax(posCat, movimiento, depth=8, turno=True) - penalize
            if val > mejor:  # MAYOR distancia es MEJOR para el ratón
                mejor = val
                mejorMovimiento = movimiento
        
        if mejorMovimiento:
            x, y = posMouse
            
            if contador < 2:
                mov = valMove(posMouse, isMouse=True)
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
                exit()
            
            laberinto[y][x] = " "
            laberinto[y1][x1] = "🐭"
            lastMouse = (x, y)  # CORREGIDO: guardar posición ANTERIOR
    
    mostrar()

# Inicio del juego
mostrar()
control = quienJuega()

while True:
    if control == "ninguno":
        input("Enter para mover: ")
        os.system("cls")
    else:
        os.system("cls")
        mostrar()
    Mover()