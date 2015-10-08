from sys import stdin
from math import fabs
from PIL import Image, ImageDraw
import time
import webbrowser
import random


class Board:
        x = None #rows
        y = None #col
        k = None #Number of eggs allowed
        board = None
        placedEggs = None
        score = None
        moves = list()

        def __init__(self, m, n, k):
                self.x = m 
                self.y = n
                self.k = k
                self.board = [[0 for x in range(0,n)]for y in range(0,m)]
                self.placedEggs = 0
                score = -100000
        
        def place_egg(self, x, y):
                self.board[x][y] = 1
                self.placedEggs +=1
        
        def remove_egg(self, x, y):
                self.board[x][y] = 0
                self.placedEggs -= 1
        
        def draw(self):
                x_size_img = self.x*30
                y_size_img = self.y*30
                size = (x_size_img, y_size_img)
                img = Image.new("RGB", size, "white")
                draw = ImageDraw.Draw(img)
                
                for y in range(0,y_size_img,30):
                        draw.line([0, y, x_size_img, y], 'black', 1)
                for x in range(0,x_size_img,30):
                        draw.line([x, 0, x, y_size_img], 'black', 1)
                for x in range(self.x):
                        for y in range(self.y):
                                if self.board[x][y]:
                                        draw.ellipse([(30*y)+5,30*x+5, 25+30*y, 25+30*x], 'black', 'black')
                img.save('egg.png', 'PNG')
                webbrowser.open('C:\Users\Brynjar\Desktop\Assignment4\egg.png')

        def check_if_legal(self, x, y):
                eggsFound = 0
                for n in range(0,self.y):
                        if(self.board[x][n]):
                                eggsFound += 1 
                                if eggsFound > self.k:
                                        return False

                eggsFound = 0
                for m in range(0,self.x):
                        if( self.board[m][y]):
                                eggsFound += 1 
                                if eggsFound > self.k:
                                        return False
                eggsFound = 0
                temp_y = y
                temp_x = x
                
                while(temp_y >= 0 and temp_x >= 0):
                        if( self.board[temp_x][temp_y]):
                                eggsFound += 1 
                                if eggsFound > self.k:
                                        return False
                        temp_y = temp_y-1
                        temp_x = temp_x-1
                                        
                temp_y = y+1
                temp_x = x+1
                while(temp_y < self.y and temp_x < self.x):
                        if( self.board[temp_x][temp_y]):
                                eggsFound += 1 
                                if eggsFound > self.k:
                                        return False
                        temp_y = temp_y+1
                        temp_x = temp_x+1
                eggsFound = 0

                temp_y = y
                temp_x = x
                
                while(temp_x < self.x and temp_y >= 0):
                        if( self.board[temp_x][temp_y]):
                                eggsFound += 1 
                                if eggsFound > self.k:
                                        return False
                        temp_y = temp_y-1
                        temp_x = temp_x+1

                temp_y = y+1
                temp_x = x-1
                
                while(temp_x >= 0 and temp_y < self.y):
                        if( self.board[temp_x][temp_y]):
                                eggsFound += 1 
                                if eggsFound > self.k:
                                        return False
                        temp_y = temp_y+1
                        temp_x = temp_x-1 
                        
                return True

                                        
                        
                        

        def objective_function(self):
                newscore = self.placedEggs
                for n in range(0,self.x):
                        for m in range(0,self.y):
                                if not self.check_if_legal(n,m):
                                        newscore -= 1
                return newscore

        def neighbour(self, T):
                
                x = random.randint(0,self.x-1)#*T
                y = random.randint(0,self.y-1)#*T
                x = int(x)
                y = int(y)
                while [x,y] in self.moves:
                        x = random.randint(0,self.x-1)#*T
                        y = random.randint(0,self.y-1)#*T
                        x = int(x)
                        y = int(y)
                
                self.moves.append([x,y])
                return [x,y]

        def SA(self):
                t = 100
                while t > 0:
                        move = self.neighbour(t)
                        self.place_egg(move[0], move[1])
                        new = self.objective_function()
                        if not new >= self.score:
                                self.remove_egg(move[0], move[1])
                                self.moves.pop()
                        else:
                                self.score = new
                                print new
                                #print self.placedEggs
                                #print self.score
                                #self.draw()
                        
                        t -= 1
                return
                                
                


def run():
        m = 5
        n = 5
        k = 2
        board = Board(m, n, k)

        board.SA()
        print board.score
        print board.placedEggs
        board.draw()
        
def test():     

        m = 5
        n = 5
        k = 2
        board = Board(m, n, k)

        #for i in range(0,m):
        #       for j in range(0,n):
        #               board.place_egg(i,j)
                                
        #board.SA()
        #print board.objective_function()
        board.place_egg(2,0)
        #print board.objective_function()
        board.place_egg(2,1)
        #print board.objective_function()
        board.place_egg(2,3)
        #print board.objective_function()
        #print board.placedEggs
        #board.draw()
        #for n in range(0,board.x):
                        #for m in range(0,board.y):
                                #if not board.check_if_legal(n,m):
                                #       print 'yo'
        print board.check_if_legal(2,3)
                        

   
#test()
run()
        

