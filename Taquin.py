import tkinter as tk
import heapq
import math

#hi again how's life

class HeapItem:
    def __init__(self, grid, f, g, parent = None):
        self.grid = grid
        self.f = f
        self.g = g
        self.parentState = parent

    def __lt__(self, other):
        return self.f < other.f

OPEN = []
CLOSED = {}
PATH = []

GOAL = [ [1, 2, 3], [8, 0, 4], [7, 6, 5], ]

gboard = [row[:] for row in GOAL]
board = [row[:] for row in GOAL] #copy not alias
goal_pos = {}
for r in range(3):
    for c in range(3):
        goal_pos[gboard[r][c]] = (r, c)

winState = False

def key(mat):
    return tuple(tuple(row) for row in mat)

def calcEuclidean(grid):
    h = 0
    for r in range(3):
        for c in range(3):
            tile = grid[r][c]
            if tile == 0:
                continue
            gr, gc = goal_pos[tile]
            h += math.sqrt((r - gr)**2 + (c - gc)**2 )
    return h

def solve():
    global winState

    winState = False
    OPEN.clear()
    CLOSED.clear()

    s0 = [row[:] for row in board] #save init state
    if key(s0) == key(gboard):
        result.config(text= "the grid already solved")
        return
    
    heapq.heappush(OPEN, HeapItem(s0, calcEuclidean(s0), 0, None))
    while winState == False and OPEN:
        sol = Astar()

    if winState == False:
        result.config(text= "cant solve")
    else:
        reconstructPath(sol)

def searchPos(grid):
    solStack = []
    br, bc = empty(grid)

    for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            nr, nc = br + dr, bc + dc
            if 0 <= nr < 3 and 0 <= nc < 3:
                newG = [row[:] for row in grid]
                newG[br][bc], newG[nr][nc] = newG[nr][nc], newG[br][bc]
                solStack.append(newG)
    return solStack
       
def Astar():
    global winState
    x = heapq.heappop(OPEN)
    if key(x.grid) not in CLOSED:
        CLOSED[key(x.grid)] = x
        for e in searchPos(x.grid):
            if calcEuclidean(e) == 0: #win
                winState = True
                return HeapItem(e, x.g+1, x.g+1, x)
            elif key(e) in CLOSED:
                continue
            else:
                heapq.heappush(OPEN, HeapItem(e, x.g+1+calcEuclidean(e), x.g+1, x))


def reconstructPath(Item):
    global PATH
    PATH = []
    x = Item
    while x:
        PATH.append(x)
        x = x.parentState
    PATH.reverse()
    PATH = PATH[1:]
    for g in PATH:
        print(g.grid, g.g, g.f)
    result.config(text=f"steps to solve (aka g): {Item.g}")


#----------------------------------------------------------------------


#gui need rebuilding
def clicked(e):
    col = e.x // 100
    row = e.y // 100
    erow, ecol = empty(board)
    print("click (" + str(col) + "," + str(row) + ")= " + str(board[row][col]))
    if abs(col - ecol) + abs(row - erow) == 1 : 
        board[row][col], board[erow][ecol] = board[erow][ecol] , board[row][col]
        print("swapped")
        createBoard()
    else:
        print("unable not adj")

def empty(grid):
    for row in range(3):
        for col in range(3):
            if grid[row][col] == 0 :
                return row, col

def spot():
    global board
    try:
        vals = [int(e.get()) for e in entries]
        vals2 = [int(e.get()) for e in entries]
        vals.sort()
    except ValueError:
        print("wrong input")
        return
    i = 0
    if set(vals) == target_set:
        for col in range(3):
            for row in range(3):
                board[row][col] = vals2[i]
                i+=1
        createBoard()
    else:
        print("no")

def createBoard():
    canvas.delete("all")
    for row in range(3):
        for col in range(3):
            num = board[row][col]
            x0 = col * 100
            y0 = row * 100
            x1 = x0 + 100
            y1 = y0 + 100
            if num != 0:
                canvas.create_rectangle(x0, y0, x1, y1, fill= "#7B64B6")
                canvas.create_text((x1+ x0)/2, (y1+y0)/2, text= str(num), fill="#000000", font=("Helvetica", 30))

def constShowup():
    global board
    for i in PATH:
        board = [row[:] for row in i.grid]
        createBoard()
        root.update()
        root.after(500)


root = tk.Tk()
root.title("Taquin solver")
root.geometry("900x400")
root.configure(bg="#121313")

title = tk.Label(root, text="Taquin solver using A* algorithm", fg="white", bg="#121313",
                 font=("Helvetica", 20, "bold"))
title.pack(pady=10)
canvas = tk.Canvas(root, width=300, height=300, bg="#448fe6",
                   highlightthickness=0)
canvas.pack(padx=10, pady=10, side= "left")
canvas.bind("<Button-1>", clicked)
btn = tk.Button(root, text="Solve", command=solve)
btn.pack(pady=20, side= "left")

entries = []
target_set = set(range(9))

for i in range(9):
    e = tk.Entry(root, width=5, justify="center")
    e.place(x=( 400 + ((i // 3) * 40)), y=( 100 + ((i % 3) * 40)))
    entries.append(e)

btn2 = tk.Button(root, text="update grid", command=spot)
btn2.place(x = 400, y= 220)

result = tk.Label(root, text=" ", bg= "black", fg= "white", 
                  font=("Helvetica", 20, "bold"))
result.place(x= 500, y= 220)

btncons= tk.Button(root, text="see solving path", command=constShowup)
btncons.place(x = 320, y= 300)



createBoard()
root.mainloop()
