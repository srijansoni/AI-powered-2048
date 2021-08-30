import random
import itertools
import numpy as np
import math
from tkinter import *
import tkinter
import time

SIZE = 500
GRID_LEN = 4
GRID_PADDING = 5

BACKGROUND_COLOR_GAME = "#92877d"
BACKGROUND_COLOR_CELL_EMPTY = "#9e948a"
BACKGROUND_COLOR_DICT = {   2:"#eee4da", 4:"#ede0c8", 8:"#f2b179", 16:"#f59563",                             32:"#f67c5f", 64:"#f65e3b", 128:"#edcf72", 256:"#edcc61",                             512:"#edc850", 1024:"#edc53f", 2048:"#edc22e",4096:"#f2b179", 8192:"#f59563",16384:"#f67c5f"}
CELL_COLOR_DICT = { 2:"#776e65", 4:"#776e65", 8:"#f9f6f2", 16:"#f9f6f2",                     32:"#f9f6f2", 64:"#f9f6f2", 128:"#f9f6f2", 256:"#f9f6f2",                     512:"#f9f6f2", 1024:"#f9f6f2", 2048:"#f9f6f2",4096:"#f9f6f2", 8192:"#f9f6f2",16384:"#f9f6f2"}
FONT = ("Arial", 40, "bold")

def merge_right(b):
    def reverse(x):
        return list(reversed(x))
    t=map(reverse,b)
    return [reverse(x) for x in merge_left(t)]

def merge_up(b):
    t = merge_left(zip(*b))
    return [list(x) for x in zip(*t)]


def merge_down(b):
    t = merge_right(zip(*b))
    return [list(x) for x in zip(*t)]

def merge_left(b):
    def merge(row,a):
        if not row:
            return a
        x=row[0]
        if len(row)==1:
            return a+[x]
        return merge(row[2:], a + [2*x]) if x == row[1] else merge(row[1:], a + [x])   
    board=[]
    for row in b:
        merged=merge([x for x in row if x!=0],[])
        merged=merged+[0]*(len(row)-len(merged))
        board.append(merged)
    return board
    
def move_exists(b):
    for row in b:
        for x,y in zip(row[:-1],row[1:]):
            if x==y or x==0 or y==0:
                return True
    return False

merge_functions={'left': merge_left, 'right':merge_right,'up':merge_up,'down':merge_down}

class Game:
    def __init__(self):
        self.board=[[0]*4 for _ in range(4)]
        self.spawn(2)
        
    def play_move(self, direction):
        self.board = merge_functions[direction](self.board)
        return self.spawn()
    
    def spawn(self,k=1):
        rows=list(range(4))
        cols=list(range(4))
        random.shuffle(rows)
        random.shuffle(cols)
        #print(rows)
        #print(cols)
        distribution=[2]*9+[4]
        count=0
        for i,j in itertools.product(rows,cols):
            if count==k:
                return True
            if self.board[i][j]!=0:
                continue
            self.board[i][j]=random.sample(distribution,1)[0]
            count+=1
            #print(self.board)
        return False
    
    def __str__(self):
        return str(self.board)
    
game=Game()

w=[[1073741824,268435456,67108864,16777216],[65536,262144,1048576,4194304],[16384,4096,1024,256],[1,4,16,64]]
w=np.array(w)
grid=np.array(game.board)
grid=np.array(grid)
        
def expectimax(grid):
    
    def score_cal(grid):
        score=0
        for i in range(0,4):
            for j in range(0,4):
                score+=grid[i][j]*w[i][j]

        penalty=0
        for i in range(0,4):
            for j in range(0,4):
                if grid[i][j]!=0:
                    if j+1<=3:
                        penalty+=abs(grid[i][j+1]-grid[i][j])
                    if j-1>=0:
                        penalty+=abs(grid[i][j-1]-grid[i][j])
                    if i+1<=3:
                        penalty+=abs(grid[i+1][j]-grid[i][j])
                    if i-1>=0:
                        penalty+=abs(grid[i-1][j]-grid[i][j])
        return score-penalty
    
    def bestmove(grid,depth,player=False):
        if depth==0 or (player and not move_exists(grid)):
            return score_cal(grid)

        temp=score_cal(grid)
        if player:
            for a,action in merge_functions.items():
                child=action(grid)
                temp=max(temp,bestmove(child,depth-1))
        else:
            temp=0
            zeros=[(i,j) for i,j in itertools.product(range(4),range(4)) if grid[i][j]==0]
            for i,j in zeros:
                c1=[[x for x in row] for row in grid]
                c2=[[x for x in row] for row in grid]
                c1[i][j]=2
                c2[i][j]=4
                temp+=(0.9*bestmove(c1,depth-1,True)/len(zeros))+(0.1*bestmove(c2,depth-1,True)/len(zeros))
        return temp
    
    results = []
    for direction, action in merge_functions.items():
        result = direction, bestmove(action(grid), 3)
        results.append(result)
    return results

def func(grid):
    def score_cal(grid):
        score=0
        for i in range(0,4):
            for j in range(0,4):
                score+=grid[i][j]*w[i][j]

        penalty=0
        for i in range(0,4):
            for j in range(0,4):
                if grid[i][j]!=0:
                    if j+1<=3:
                        penalty+=abs(grid[i][j+1]-grid[i][j])
                    if j-1>=0:
                        penalty+=abs(grid[i][j-1]-grid[i][j])
                    if i+1<=3:
                        penalty+=abs(grid[i+1][j]-grid[i][j])
                    if i-1>=0:
                        penalty+=abs(grid[i-1][j]-grid[i][j])
        return score-penalty
    def minimax(grid,depth,player=False):
        if depth==0 or (player and not move_exists(grid)):
            return score_cal(grid)
        #best_score=score_cal(grid)
        if player:
            best_score=-float("inf")
            for a,action in merge_functions.items():
                child=action(grid)
                best_score=max(best_score,minimax(child,depth-1,False))
            #return best_score
        else:
            best_score=float("inf")
            zeros=[(i,j) for i,j in itertools.product(range(4),range(4)) if grid[i][j]==0]
            a=[2,4]
            for i,j in zeros:
                for x in a:
                    child=grid
                    child[i][j]=x
                    best_score=min(best_score,minimax(child,depth-1,True))
        return best_score
    results=[]
    for direction,action in merge_functions.items():
        result=direction,minimax(action(grid),3)
        results.append(result)
    return results

def greedy(grid):
    def score_cal(grid):
        score=0
        for i in range(0,4):
            for j in range(0,4):
                score+=grid[i][j]*w[i][j]

        penalty=0
        for i in range(0,4):
            for j in range(0,4):
                if grid[i][j]!=0:
                    if j+1<=3:
                        penalty+=abs(grid[i][j+1]-grid[i][j])
                    if j-1>=0:
                        penalty+=abs(grid[i][j-1]-grid[i][j])
                    if i+1<=3:
                        penalty+=abs(grid[i+1][j]-grid[i][j])
                    if i-1>=0:
                        penalty+=abs(grid[i-1][j]-grid[i][j])
        return score
    def bstmove(grid,depth,player=False):
        if depth==0 or (player and not move_exists(grid)):
            return score_cal(grid)
        #best_score=score_cal(grid)
        if player:
            best_score=-float("inf")
            for a,action in merge_functions.items():
                child=action(grid)
                best_score=max(best_score,bstmove(child,depth-1,False))
            #return best_score
        else:
            best_score=float("inf")
            zeros=[(i,j) for i,j in itertools.product(range(4),range(4)) if grid[i][j]==0]
            a=[2,4]
            for i,j in zeros:
                for x in a:
                    child=grid
                    child[i][j]=x
                    best_score=min(best_score,bstmove(child,depth-1,True))
        return best_score
    results=[]
    for direction,action in merge_functions.items():
        result=direction,bstmove(action(grid),1)
        results.append(result)
    return results

game=Game()

def aiplay(game):
    m=tkinter.Tk()
    m.grid()
    m.title('2048')
    m.grid_cells = []
    background = Frame(m, bg=BACKGROUND_COLOR_GAME, width=SIZE, height=SIZE)
    background.grid()
    dirdict={1:'left',2:'right',3:'up',4:'down'}
    for i in range(GRID_LEN):
        grid_row = []
        for j in range(GRID_LEN):
            cell = Frame(background, bg=BACKGROUND_COLOR_CELL_EMPTY, width=SIZE/GRID_LEN, height=SIZE/GRID_LEN)
            cell.grid(row=i, column=j, padx=GRID_PADDING, pady=GRID_PADDING)
            t = Label(master=cell, text="", bg=BACKGROUND_COLOR_CELL_EMPTY, justify=CENTER, font=FONT, width=4, height=2)
            t.grid()
            grid_row.append(t)
        m.grid_cells.append(grid_row)
        
    def task():
        for i in range(GRID_LEN):
            for j in range(GRID_LEN):
                new_number = table[i][j]
                if new_number == 0:
                    m.grid_cells[i][j].configure(text="", bg=BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    m.grid_cells[i][j].configure(text=str(new_number), bg=BACKGROUND_COLOR_DICT[new_number], fg=CELL_COLOR_DICT[new_number])
            m.update_idletasks()
    
    while True:
        print(str(game))
        table=game.board
        m.after(0,task)
        m.update()
        
        #random
#         x=random.randint(1,4)
#         direction=dirdict[x]
        
        #greedy
#         direction= max(greedy(game.board),key=lambda x:x[1])[0]
        
        #expectimax
        direction= max(expectimax(game.board),key=lambda x:x[1])[0]
        
        #minimax
#         direction= max(func(game.board),key=lambda x:x[1])[0]
        
        if not game.play_move(direction):
            sum=0
            for i in range(GRID_LEN):
                for j in range(GRID_LEN):
                    sum+= table[i][j]
            print(sum)
            break
    m.mainloop()
aiplay(game)


