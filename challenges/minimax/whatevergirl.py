#i need to craete a laberinth
#show the laberinth
#find the characters
#find the distance betwwen them
#find the valid moves
#find the best move
#move them
import math
import os
choice = 0
while choice != 1:
    choice = int(input("ingrese una opcion: "))
    maze = [list("###########"),
            list("#C###     #"),
            list("# ### ### #"),
            list("#     #  M#"),
            list("## ## ## ##"),
            list("## ## ## ##"),
            list("##       ##"),
            list("#  ########"),
            list("###########"),
    ]
    
def mostrar():
    for fila in maze:
        print(" ".join(fila))

def find(player):
    for y,fila in enumerate(maze):
        for x,cell in enumerate(fila):
            if cell == player:
                return((x,y))
    return None

def distancia(a,b):
    return math.dist(a,b)

def validMoves(position):
    if position == None:
        print("the end")
        mostrar()
        exit()
    x,y = position
    valid = []
    moves = [(x+1,y),(x,y-1),(x-1,y),(x,y+1)]
    
    for dx,dy in moves:
        if 0 <= dy < len(maze) and 0 <= dx < len(maze[0]):
            cell = maze[dy][dx]
            if cell != "#":
                valid.append((dx,dy))
    return(valid)

    
def minimax(cat,mouse,depth,turn):
    if cat == mouse:
        return 0
    if depth == 0:
        return distancia(cat,mouse)
    
    if turn:
        best = float("inf")
        for move in validMoves(cat):
            val= minimax(move,mouse,depth-1,False)
            if val < best:
                best = val 
        return best
    else:
        best = float("-inf")
        for move in validMoves(mouse):
            val= minimax(cat,move,depth-1,True)
            if val > best:
                best = val 
        return best
    
def play():
            
    mouse = find("M")
    cat = find("C")
    mejor_movimiento = None
    best = float("-inf")
    
    for move in validMoves(mouse):
        val = minimax(cat,move,depth= 2,turn=True)
        if val > best:
            best = val
            mejor_movimiento = move
                    
    if mejor_movimiento:
        x,y = mouse
        x1,y1 = mejor_movimiento
        maze[y][x] = " "
        maze[y1][x1] = "M" 
        
    cat = find("C")
    mouse = find("M")
    mejor_movimiento = None
    best = float("inf")

    for move in validMoves(cat):
        val = minimax(move,mouse,depth=2,turn=False)
        if val < best:
            best = val
            mejor_movimiento = move
                
    if mejor_movimiento:
        x,y = cat
        x1,y1 = mejor_movimiento
        maze[y][x] = " "
        maze[y1][x1] = "C"
         
    mostrar()  
     
while True:
    input("enter")
    os.system("cls")
    play()
