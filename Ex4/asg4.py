from sys import stdin
from math import fabs, exp
import math
from PIL import Image, ImageDraw
import time
import webbrowser
from random import randint,random
from collections import deque
from copy import deepcopy

class SA(object):
    def __init__(self, m, n, k):
        self.x = m 
        self.y = n
        self.k = k
        self.checked_boards = []
        self.target = min(n,m)*k*1.0
        
    def generate_board(self):
        return [[False]*self.x for i in range(0, self.y)]

    def draw(self, board):
        x_size_img = self.x*30
        y_size_img = self.y*30
        size = (x_size_img, y_size_img)
        img = Image.new("RGB", size, "white")
        draw = ImageDraw.Draw(img)
        
        for y in range(0,y_size_img,30):
            draw.line([0, y, x_size_img, y], 'black', 1)
        for x in range(0,x_size_img,30):
            draw.line([x, 0, x, y_size_img], 'black', 1)
        for x in range(0, self.x):
            for y in range(0, self.y):
                if board[x][y]:
                    draw.ellipse([(30*y)+5,30*x+5, 25+30*y, 25+30*x], 'black', 'black')
        img.save('egg_'+str(self.x)+str('.png'), 'PNG')
        #webbrowser.open('C:\Users\Brynjar\Desktop\Assignment4\egg.png')

    def checkRowsAndColumns(self, board):
        eggsFound = 0
        collisions = 0
        totalNumOfEggs = 0
        #Check rows
        for m in range(0,self.x):
            for n in range(0, self.y):
                if board[m][n]:
                    eggsFound += 1
                    totalNumOfEggs += 1
                if(n == self.y-1):
                    collisions += max(0, eggsFound - self.k)
                    eggsFound = 0
        eggsFound = 0
        #check col
        for n in range(0,self.y):
            for m in range(0, self.x):
                if board[m][n]:

                    eggsFound += 1
                if(m == self.x-1):
                    collisions += max(0, eggsFound - self.k)
                    eggsFound = 0
        
        return collisions,totalNumOfEggs
            
    
    def checkDiags(self, board):
        eggsFound = 0
        collisions = 0

        y = 0 # Checks all the topleft -> downright diagonals.
        while y < self.y:
            for x in range(0, self.x-y):
                if board[x][x+y]:
                    eggsFound +=1
            y += 1
            collisions += max(0, eggsFound - self.k)
            eggsFound = 0

        y = 1 # Checks all the topleft -> downright diagonals.
        while y < self.y:
            for x in range(0, self.x-y):
                if board[x+y][x]:
                    eggsFound +=1
            y += 1
            collisions += max(0, eggsFound - self.k)
            eggsFound = 0

            

        eggsFound = 0
        y = self.y-1
        
        while y >= 0:
            for x in range(0, y+1):
                if board[y-x][x]:
                    eggsFound +=1
            y -= 1
            collisions += max(0, eggsFound - self.k)
            eggsFound = 0

        eggsFound = 0
        y = self.y
        j = 0
        while j < self.y:
            for x in range(1+j, self.y):
                if board[x][y-x]:
                    eggsFound +=1
            y += 1
            j += 1

            collisions += max(0, eggsFound - self.k)
            eggsFound = 0
                
    
        return collisions


    def checkForMisplacedEggs(self, board):  
        totalEggs = 0
        collisions = 0
        collisions += self.checkDiags(board)
        temp_collisions,totaleggs = self.checkRowsAndColumns(board)
        collisions += temp_collisions
        return collisions, totaleggs
        
    def objective_function(self, board):
        collisions = 0
        placedEggs = 0
        collisions, placedEggs = self.checkForMisplacedEggs(board)
        newscore = 0
        factor = 1/self.target
        newscore = min(self.target, placedEggs)*factor- collisions*0.1
        return min(1, max(0, newscore))
        

    def get_neighbors(self, board):
        neighbors = []
        for x in range(len(board)):
            for y in range(len(board[x])):
                new_board = deepcopy(board)
                new_board[x][y] = not board[x][y]
                for b in new_board:
                	print b
            	print ''
            	if y == 1:
                	return
                neighbors.append(new_board)              
        return neighbors

    def compare_boards(self, board, current_board):

        for x in range(0, len(board)):
            for y in range(0, len(board)):
                if board[x][y] != current_board[x][y]:
                    return False
        return True

    def board_is_checked(self, board):
        for checked_board in self.checked_boards:
            if self.compare_boards(board, checked_board):
                return True
        return False

    def run(self):
        T = 1
        dt = 0.01
        start_board = self.generate_board()
        boards = deque([start_board])   
        current_board = None
        while T > 0:
            current_board = boards.popleft()

            self.checked_boards.append(current_board)
            if self.objective_function(current_board) >= 1.0:
                print 'Finished'
                print 'col +rows: ' +str(self.checkRowsAndColumns(current_board))
                self.draw(current_board)
                print self.objective_function(current_board)
                return

            neighbors = self.get_neighbors(current_board)
            best_neighbor = None
            best_neighbor_score = -1
            
            for neighbor in neighbors:
                if self.board_is_checked(neighbor) or neighbor == None:
                    continue
                neighbor_score = self.objective_function(neighbor)
                if neighbor_score > best_neighbor_score:
                    best_neighbor_score = neighbor_score
                    best_neighbor = neighbor
            P = self.objective_function(current_board)
            P_max = self.objective_function(best_neighbor)

            if P != 0:
                q = (P_max-P)/P
            else: 
                q = 0

            p = min(1, exp(-q/T))
            if random() > p: # Exploiting
                boards.append(best_neighbor)
            else: # Exploring
                boards.append(neighbors[randint(0,len(neighbors)-1)])
            T -= dt


        if self.objective_function(current_board) < self.target:
            print ' Did not find a solution'
            print self.objective_function(current_board)
            self.draw(current_board)
            return

Sa = SA(5,5,2)
Sa.run()
