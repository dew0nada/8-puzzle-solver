import tkinter as tk


INITIAL = [
    [1, 2, 3],
    [8, 0, 4],
    [7, 6, 5],
]

GOAL = [
    [1, 2, 3],
    [0, 8, 4],
    [7, 6, 5],
]

board = [row[:] for row in INITIAL]
gboard = [row[:] for row in GOAL]
blockS = 100

def checkWin():
    for row in range(3):
        for col in range(3):
            if board[row][col] != gboard[row][col]:
                return
    print("WIN? (like its hard)")



def clicked(e):
    col = e.x // 100
    row = e.y // 100
    erow, ecol = empty()
    print("click (" + str(col) + "," + str(row) + ")= " + str(board[row][col]))
    if abs(col - ecol) + abs(row - erow) == 1 : 
        board[row][col], board[erow][ecol] = board[erow][ecol] , board[row][col]
        print("swapped")
        createBoard()
        checkWin()
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

createBoard()


"""rect_id = canvas.create_rectangle(10, 10, 100, 100, fill="blue", outline="white")
text_id = canvas.create_text(55, 20, text="1", fill="white",
                             font=("Helvetica", 24, "bold"))

circle_id = canvas.create_oval(40, 10, 50, 600, fill="white", outline="red")"""

root.mainloop()
