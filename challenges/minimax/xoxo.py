table=[
    list(" | | "),
    list("---------"),
    list(" | | "),
    list("---------"),
    list(" | | "),
]
def mostrar():
    for fila in table:
        if "-" in fila:
           print("".join(fila))
        else:
            print(" ".join(fila))
def valid_moves():
    moves= []
    for y, fila in enumerate(table):
        for x, celda in enumerate(fila):
            if celda == " ":
                moves.append((x,y))
    print(moves)
    
valid_moves()