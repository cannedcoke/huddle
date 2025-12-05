import math

# ============================================================
# LABERINTO BASE
# ============================================================
laberinto = [
    list("###########"),
    list("#C###     #"),
    list("# ### ### #"),
    list("#     #  M#"),
    list("## ## ## ##"),
    list("## ## ## ##"),
    list("##       ##"),
    list("#  ########"),
    list("###########"),
]

# ------------------------------------------------------------
def encontrar(simbolo):
    for x, fila in enumerate(laberinto):
        for y,celda in enumerate(laberinto[fila]):
            if celda == simbolo:
                return((x,y))

# ------------------------------------------------------------
def distancia(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# ------------------------------------------------------------
def movimientosPosibles(pos):
    x, y = pos
    candidatos = [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
    validos = []
    for nx, ny in candidatos:
        if laberinto[ny][nx] != "#":
            validos.append((nx, ny))
    return validos

# ============================================================
# FUNCIÓN INCOMPLETA — PARA QUE LA COMPLETES
# ============================================================
def minimax(posCat, posMouse, depth, turnoGato):
    
    if posCat == posMouse:
        return -999
    if depth == 0:
        return distancia(posCat,posMouse)
    
    if turnoGato:
        mejor = float("inf")
        for move in movimientosPosibles(posCat):
            val= minimax(move,posCat,depth-1,False)
            if val > mejor:
                mejor =val
        return mejor
    """
    COMPLETAR:

    Esta función debe implementar Minimax con estas reglas:

        1. Si el gato atrapa al ratón → devolver un valor MUY negativo.
        2. Si depth == 0 → devolver distancia o heurística.
        3. Si turnoGato == True:
                el gato MINIMIZA el valor.
        4. Si turnoGato == False:
                el ratón MAXIMIZA el valor.

    Estructura sugerida (NO completar aquí):
        
        if posCat == posMouse:
            return ...

        if depth == 0:
            return ...

        if turnoGato:
            mejor = +inf
            for mov in movimientosPosibles(posCat):
                val = minimax(...)
                mejor = min(mejor, val)
            return mejor
        else:
            mejor = -inf
            for mov in movimientosPosibles(posMouse):
                val = minimax(...)
                mejor = max(mejor, val)
            return mejor
    """
    pass  # <<< COMPLETAR ACÁ
    if posCat == posMouse:
        return -999
    if depth == 0:
        return distancia(posMouse,posCat)
    if turnoGato:
        mejor = float("inf")
        for move in movimientosPosibles(posCat):
            val= minimax(move,posMouse,depth-1,False)
            if val < mejor:
                mejor = val
        return mejor
    else:
        mejor = float("-inf")
        for move in movimientosPosibles(posMouse):
            val= minimax(posCat,move,depth-1,True)
            if val > mejor:
                mejor = val
        return mejor
        

# ============================================================
# MOVIMIENTOS DE GATO Y RATÓN
# ============================================================
def mover_gato(posCat, posMouse):
    mejor = float("inf")
    mejorMov = posCat
    for mov in movimientosPosibles(posCat):
        v = minimax(mov, posMouse, 4, False)
        if v < mejor:
            mejor = v
            mejorMov = mov
    if mejorMov:
        x,y = posCat
        x1,y1 = mejorMov
        laberinto[y][x] = " "
        laberinto[y1][x1] = "😾"

def mover_mouse(posCat, posMouse):
    mejor = float("-inf")
    mejorMov = posMouse
    for mov in movimientosPosibles(posMouse):
        v = minimax(posCat, mov, 4, True)
        if v > mejor:
            mejor = v
            mejorMov = mov
    return mejorMov

# ------------------------------------------------------------
def mostrar():
    for fila in laberinto:
        print("".join(fila))
    print()

# ============================================================
# LOOP PRINCIPAL
# ============================================================
posCat = encontrar("C")
posMouse = encontrar("M")

turnoGato = True

while True:
    mostrar()

    if posCat == posMouse:
        print("El gato atrapó al ratón.")
        break

    if turnoGato:
        nuevo = mover_gato(posCat, posMouse)
        laberinto[posCat[1]][posCat[0]] = " "
        posCat = nuevo
        laberinto[posCat[1]][posCat[0]] = "C"
    else:
        nuevo = mover_mouse(posCat, posMouse)
        laberinto[posMouse[1]][posMouse[0]] = " "
        posMouse = nuevo
        laberinto[posMouse[1]][posMouse[0]] = "M"

    turnoGato = not turnoGato
