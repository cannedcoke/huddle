import math 
# funcion para mostrar el Laberinto
laberinto = [
    list("@@@@@@@@@@@@@@"),
    list("@######## ###@"),
    list("@#     ##    @"),
    list("@###M####C###@"),
    list("@###      ###@"),
    list("@#### ### ###@"),
    list("@  ## ### ###@"),
    list("@# ## ### ###@"),
    list("@# ## ### ###@"),
    list("@# ## ### ###@"),
    list("@# ## ### ###@"),
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
def mostrarLaberinto():
    for fila in laberinto:
        print(" ".join(fila))
                                  
def distance(a,b):
    return math.dist(a,b)

contador = 0
def hacerMovimiento():
    catPos = encontrar("C")
    mousePos = encontrar("M")
    mejorMovimiento = None
    mejor = float("inf")
    
    for move in near(catPos):
        val=minimax(move,mousePos,depth=3,turno=False)
        if val < mejor:
            mejor = val
            mejorMovimiento = move
        
    if mejorMovimiento:
        x,y = catPos
        x1,y1 = mejorMovimiento
        laberinto[y][x] = " "
        laberinto[y1][x1] = "C"
        
        if encontrar("C") == encontrar("M") or (encontrar("M") is None):
            print("atrapada")
            return
    catPos = encontrar("C")
    mousePos = encontrar("M")
    mejorMovimiento = None
    mejor = float("-inf")
    
    # movimientos posibles, incluyendo chequeo de escape
    posibles = near(mousePos,es_raton=True)

    # si no hay movimientos, significa que está acorralado o fuera de rango
    if not posibles:
        laberinto[mousePos[1]][mousePos[0]] = " "
        print("el ratón escapó")
        return

    for move in posibles:
        if laberinto[move[1]][move[0]] == "@":
            laberinto[mousePos[1]][mousePos[0]] = " "
            print("el ratón escapó")
            mostrarLaberinto()
            return
        val = minimax(catPos, move, depth=2, turno=True)
        if val > mejor:
            mejor = val
            mejorMovimiento = move

        
    if mejorMovimiento:
        x, y = mousePos
        if contador < 2:
            dx = random.randint(-1,1)
        else:
            x1, y1 = mejorMovimiento
        if not (0 <= y1 < len(laberinto) and 0 <= x1 < len(laberinto[y1])):
            laberinto[y][x] = " "   # borra al ratón
            print("el ratón escapó")
            return
        # si el movimiento del ratón va hacia el gato
        if laberinto[y1][x1] == "C":
            print("atrapada")
            mostrarLaberinto()
            return

    laberinto[y][x] = " "
    laberinto[y1][x1] = "M"


    mostrarLaberinto()

            
        
        



def encontrar(animal):
    for y, fila in enumerate(laberinto):
        for x, cell in enumerate(fila):
            if cell == animal:
                return(x,y)
    return None

def near(posicion,es_raton = False):
    x, y = posicion
    posibles = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
    valido = []
    for x1,y1 in posibles:
        if 0 <= y1 < len(laberinto) and 0 <= x1 < len(laberinto[y1]):
            cell = laberinto[y1][x1]
            if cell != "#":
                if es_raton or cell != "@":
                    valido.append((x1,y1))
    return valido 
        
def minimax(catPos,mousePos, depth,turno):
    if catPos == mousePos:
        return 0
    if depth == 0:
        return distance(catPos,mousePos)
    
    if turno:
        mejor= float("inf") # here it defines mejor as a really big number
        for move in near(catPos):# this iterates each valid position
            val=minimax(move,mousePos,depth -1, False) #here is were i get lost bc why am i calling the function im already in
            if val < mejor:
                mejor = val
        return mejor
    else:
        mejor= float("-inf")#este inf representa un numero que es menor a todos pero en realidad es como un placeholder 
        for move in near(mousePos, es_raton=True):
            if laberinto[move[1]][move[0]] == "@":
                return 9999 # favorece ir a la salida

            val=minimax(catPos,move,depth -1, True)
            if val > mejor:
                mejor = val
        return mejor
    
       
mostrarLaberinto()
contador = 0
while contador < 15:
    print("------------------------")
    cat = encontrar("C")
    mouse = encontrar("M")

    # si ya se atraparon o el ratón desapareció
    if cat is None or mouse is None or cat == mouse:
        print("se escapo")
        break

    hacerMovimiento()

    # volver a verificar después de mover
    cat = encontrar("C")
    mouse = encontrar("M")
    if cat is None or mouse is None or cat == mouse:
        break
    contador += 1

