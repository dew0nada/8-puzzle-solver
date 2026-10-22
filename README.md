# Taquin Solver — 8-Puzzle with A* Search

A Python desktop application that solves the classic **Taquin (8-puzzle)** using the **A\* search algorithm** with a **Euclidean distance heuristic**. Built with `tkinter`, no external dependencies.

![Python](https://img.shields.io/badge/python-3.x-blue)
![Tkinter](https://img.shields.io/badge/GUI-tkinter-green)

---

## Features

- **A\* search** with Euclidean distance heuristic
-  **Interactive board** — click a tile adjacent to the empty space to slide it
-  **Manual input** — type any valid 0–8 configuration
-  **Path reconstruction** — walk back through parent pointers
-  **Path animation** — watch the solution play out step by step
-  **Unsolvable case handling** — can detect whether the grid is solvable or not

---

## How It Works

### State representation
The board is a `3×3` list of lists; `0` marks the empty tile.

### Heuristic
For every tile `t` (excluding `0`):

$$h(n) = \sum \sqrt{(r - r_{goal})^2 + (c - c_{goal})^2}$$

This is **admissible** (never overestimates the true cost), so A\* is guaranteed to find an optimal solution.

### Algorithm
1. Push the start state onto a min-heap `OPEN` keyed by `f = g + h`.
2. Pop the lowest-`f` state. If it's the goal, reconstruct the path.
3. Otherwise mark it `CLOSED` and push its legal children.
4. Repeat until the goal is reached or `OPEN` is empty.

---


```bash
python Taquin.py
```
