kind of algo, when reading pls ignore the fact that i don't respect syntax
read it before u ask me qs
also for potential outsiders: enjoy my nonsense cuz i have freewill to push stuff here

"""
f = h + g <--- priotiy
open / closed
open (state[3*3], f, g, motherstate)

open: sorted heap           closed: set


"""
def solve():
  """
  start = current pos
  open(start), closed()
  while goalfound == false AND open !empty:
    Astar()
  if empty:
    
  else:
    plan back
  """


def csGrid(g1, g2):
  """return false/true"""

def cdClosed(s): #one for open
  pass

def findMoves(grid):
  """
      abs rule
      output is gridStack"""

def calcManhattan(grid):
  #return h (heuristique)
  pass

def Astar():
  """
  x= pop open
  if csGrid(x.gr, goal.gr):
    win stuff
    goalfound = true
    return
  elif !csClosed(x):
    miniStack = findMoves(x)
    for s in miniStack:
      add to open((s, x.g + 1 + calcManhattan(s), x.g + 1, x))

  updated open closed
  """



"""
     TO DO:

  - cs open/closed fct
  - fix Astar so adding elements only after cs check
  - trace back code
"""
