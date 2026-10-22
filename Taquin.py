import tkinter as tk
import heapq
import math

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
board = [row[:] for row in GOAL]
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
    PATH.clear()

    s0 = [row[:] for row in board]
    if key(s0) == key(gboard):
        result.config(text="Already solved!")
        return
    
    heapq.heappush(OPEN, HeapItem(s0, calcEuclidean(s0), 0, None))
    sol = None
    while not winState and OPEN:
        sol = Astar()

    if not winState:
        result.config(text="Cant solve")
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
    global winState, OPEN, CLOSED
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

def empty(grid):
    for row in range(3):
        for col in range(3):
            if grid[row][col] == 0 :
                return row, col

# ---------------- GUI ----------------

def clicked(e):
    col = e.x // 100
    row = e.y // 100
    erow, ecol = empty(board)
    if abs(col - ecol) + abs(row - erow) == 1 : 
        board[row][col], board[erow][ecol] = board[erow][ecol] , board[row][col]
        createBoard()

def spot():
    global board
    try:
        vals2 = [int(e.get()) for e in entries]
        vals = sorted(vals2)
    except ValueError:
        result.config(text="Invalid input!")
        return
    i = 0
    if set(vals) == target_set:
        for col in range(3):
            for row in range(3):
                board[row][col] = vals2[i]
                i+=1
        createBoard()
        result.config(text="Grid updated")
    else:
        result.config(text="Must use 0-8")

def createBoard():
    canvas.delete("all")
    canvas.create_rectangle(0, 0, 300, 300, fill="#2b2b3d", outline="")
    for row in range(3):
        for col in range(3):
            num = board[row][col]
            x0 = col * 100
            y0 = row * 100
            x1 = x0 + 100
            y1 = y0 + 100
            if num != 0:
                canvas.create_rectangle(x0, y0, x1, y1, fill= "#7B64B6")
                canvas.create_text((x1+ x0)/2, (y1+y0)/2, text= str(num),
                                   fill="#A3A29A", font=("Helvetica", 30))

def pathVisual():
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

#in case u saw this hi (have fun reading my code cuz i had fun writing it)

title = tk.Label(root,
                 text="Taquin solver using A* algorithm",
                 fg="#545C7E", bg="#121313",
                 font=("Helvetica", 20, "bold"))
title.pack(pady=10)

canvas = tk.Canvas(root,
                   width=300, height=300,
                   bg="#545C7E",
                   highlightthickness=0)
canvas.pack(side= "left")
canvas.bind("<Button-1>", clicked)

rightF = tk.Frame(root,
                 bg="#121313")
rightF.pack(side="left", fill="both", expand=True, padx= 10, pady= 10)

resultF  = tk.Frame(rightF,
                        bg="#121313")
resultF.pack(side="bottom", fill="both", expand=True, pady= 20)

controlF  = tk.Frame(rightF,
                         bg="#121313",
                          height= 200)
controlF.pack(side="top", fill="both", expand=True, pady= 10)

btnF  = tk.Frame(controlF,
                         bg="#121313")
btnF.pack(side="left", fill="both", expand=True, padx= 20, pady= 10)

manualF  = tk.Frame(controlF,
                         bg="#121313")
manualF.pack(side="left", fill="both", expand=True, padx= 20, pady= 10)

btn_update = tk.Button(btnF ,
                       text="Update Grid", command=spot,
                       bg="#7B64B6", fg="white",
                       font=("Helvetica", 11, "bold"),
                       relief="flat",
                       padx=10, pady=4)
btn_update.pack(side="top", padx=4, pady= 10)

btn_solve = tk.Button(btnF ,
                      text="Solve", command=solve,
                      bg="#7B64B6", fg="white",
                      font=("Helvetica", 11, "bold"),
                      relief="flat",
                      padx=10, pady=4)
btn_solve.pack(side="top", padx=4, pady= 10)

btn_path = tk.Button(btnF ,
                     text="Show Path", command=pathVisual,
                     bg="#7B64B6", fg="white",
                     font=("Helvetica", 11, "bold"),
                     relief="flat",
                     padx=10, pady=4)
btn_path.pack(side="top", padx=4, pady= 10)

result = tk.Label(resultF,
                  text=" ",
                  bg="#545C7E", fg="white",
                  font=("Helvetica", 13, "bold"),
                  height=2, width=34,
                  relief="flat")
result.pack(pady=10, anchor="w", side= "left")

entries = []
target_set = set(range(9))
for i in range(9):
    e = tk.Entry(manualF, width=5)
    e.place(x=(20 +((i // 3) * 40)), y=(20 +((i % 3) * 40)))
    entries.append(e)

createBoard()
root.mainloop()