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
PATH = set()

INITIAL = [ [1, 2, 3], [8, 0, 4], [7, 6, 5], ]
GOAL = [ [1, 2, 3], [0, 8, 4], [7, 6, 5], ]

board = [row[:] for row in INITIAL]
gboard = [row[:] for row in GOAL]
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

def solve(): #need upfront check (if s0 is goal)
    global winState
    winState = False
    OPEN.clear()
    CLOSED.clear()

    s0 = [row[:] for row in board] #save init state
    heapq.heappush(OPEN, HeapItem(s0, calcEuclidean(s0), 0, None))
    while winState == False and OPEN:
        sol = Astar()

    if winState == False:
        print("cant be solved")
    else:
        reconstructPath(sol)

def searchPos(grid):
    solStack = []
    stop = False
    for row in range(3):
        for col in range(3):
            if grid[row][col] == 0:
                br, bc = row, col
                stop = True
                break
        if stop == True:
            break

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
    PATH.clear()
    print(Item.grid)

    x = Item
    y= 0
    while x.parentState:
        PATH.add(x)
        x= x.parentState
        y = CLOSED[key(x.grid)]
        pass

    print("total steps req: " + str(Item.g))
    for g in PATH:
        print(g.grid)
    return PATH


#----------------------------------------------------------------------


#gui need rebuilding
def clicked(e):
    col = e.x // 100
    row = e.y // 100
    erow, ecol = empty()
    print("click (" + str(col) + "," + str(row) + ")= " + str(board[row][col]))
    if abs(col - ecol) + abs(row - erow) == 1 : 
        board[row][col], board[erow][ecol] = board[erow][ecol] , board[row][col]
        print("swapped")
        createBoard()
    else:
        print("unable not adj")

def empty():
    for row in range(3):
        for col in range(3):
            if board[row][col] == 0 :
                return row, col

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

root = tk.Tk()
root.title("Taquin")
root.geometry("600x600")
root.configure(bg="#18252D")
print("helllooooooo")

title = tk.Label(root, text="test", fg="white", bg="#421615",
                 font=("Helvetica", 20, "bold"))
title.pack(pady=10)
status = tk.Label(root, text="idk man text", fg="gray", bg="#421615")
status.pack(side="right")
canvas = tk.Canvas(root, width=300, height=300, bg="#448fe6",
                   highlightthickness=0)
canvas.pack(padx=10, pady=10)
canvas.bind("<Button-1>", clicked)
btn = tk.Button(root, text="Solve", command=solve)
btn.pack(pady=20)

createBoard()
root.mainloop()
