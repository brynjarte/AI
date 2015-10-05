from sys import stdin
from math import fabs

True = 1
False = 0

def manhattan_number(node):
	return fabs(node.x - goal.x) + fabs(node.y -goal.y)

def get_cost(current_node):
        if current_node.type == 'w':
                return 100
        elif current_node.type == 'm':
                return 50
        elif current_node.type == 'f':
                return 10
        elif current_node.type == 'g':
                return 5
        elif current_node.type == 'r':
                return 1
        else:
                return 0

class Node:
	x = None
	y = None
	navigated_from = None
	goal = None
	type = None
	on_path = None
	g = None
	f = None
	def __init__(self, x, y, type):
		self.x = x
		self.y = y
		self.type = type
		self.on_path = False
		self.g = None
		self.f = None


open_list = list()
closed_list = list()
board = []
fil = open('board-2-1.txt')

goal = None
done = False
y = 0

for line in fil:
	temp_line = []
	for x in range(len(line)-1):
		if line[x] != '\n':
			temp_node = Node(x, y, line[x])
			if temp_node.type == 'B':
				temp_node.goal = True                   
				goal = temp_node
			elif temp_node.type == 'A':
				start = temp_node
				open_list.append(temp_node)
			elif temp_node.type == '#':
				closed_list.append(temp_node)
				
			temp_line.append(temp_node)
	board.append(temp_line)
	y = y+1
if len(open_list) > 0:
	open_list[0].g = 0
	open_list[0].f = manhattan_number(open_list[0]) + get_cost(open_list[0])
	open_list[0].on_path = True


size_y = len(board)
size_x = len(board[0])

shortest_path = [['.' for x in range(0,size_x)]for z in range(0,size_y)]

def sort_open_list(open_list, alg):
        if alg == 'astar':
                open_list = sorted(open_list, key=lambda x: x.f)
        if alg == 'dijkstra':
                open_list = sorted(open_list, key=lambda x: x.g)
                
        return open_list
        
def get_parents(node):
	parents = []
	if( node.y < size_y-1): # UP
		parents.append(board[node.y+1][node.x])
	if( node.y > 0): # DOWN
		parents.append(board[node.y-1][node.x])
	if( node.x < size_x -1): # RIGHT
	 	parents.append(board[node.y][node.x+1])
	if( node.x > 0): #LEFT
		parents.append(board[node.y][node.x-1])
	return parents

def construct_path(current_node):

	shortest_path[current_node.y][current_node.x] = 'o'
	if current_node.navigated_from != None:
		current_node.on_path = True
		construct_path(current_node.navigated_from)
		
def print_board():
        for x in range(size_y-1):
                for y in range(size_x-1):
                        if board[x][y].type == '#':
                                shortest_path[x][y] = '#' 
        print ''
        for i in shortest_path:
                print ' '.join(i)
        print ''

def a_star(sorted_list):
        
        current = sorted_list[0]
        
        if current.type == 'B':
                construct_path(current)
                sorted_list.pop(0)
                closed_list.append(current)
                shortest_path[current.y][current.x] = 'x'
                return True

        sorted_list.pop(0)
        closed_list.append(current)
        shortest_path[current.y][current.x] = 'x'
        temp_parents = get_parents(current)
        for parent in temp_parents:
                if parent in closed_list:
                        shortest_path[parent.y][parent.x] = 'x'
                        continue
                
                new_g = current.g + get_cost(parent)
                if parent not in sorted_list or new_g < parent.g:
                        parent.navigated_from = current
                        parent.g = new_g
                        parent.f = parent.g + manhattan_number(parent)

                        if parent not in sorted_list:
                                sorted_list.append(parent)
                                shortest_path[parent.y][parent.x] = '*'
        return False



def BFS():

        current = open_list[0]
        if current.type == 'B':
                construct_path(current)
                open_list.pop(0)
                closed_list.append(current)
                shortest_path[current.y][current.x] = 'x'
                return True
                
        open_list.pop(0)
        closed_list.append(current)
        shortest_path[current.y][current.x] = 'x'
        temp_parents = get_parents(current)
        for parent in temp_parents:
                if parent in closed_list:
                        continue
                if parent not in open_list:
                        parent.navigated_from = current
                        open_list.append(parent)
                        shortest_path[parent.y][parent.x] = '*'
        return False

def dijkstra(sorted_list):
        current = sorted_list[0]
        
        if current.type == 'B':
                construct_path(current)
                sorted_list.pop(0)
                closed_list.append(current)
                shortest_path[current.y][current.x] = 'x'
                return True

        sorted_list.pop(0)
        closed_list.append(current)
        shortest_path[current.y][current.x] = 'x'
        temp_parents = get_parents(current)
        for parent in temp_parents:
                if parent in closed_list:
                        continue
                
                new_g = current.g + get_cost(parent)
                if parent not in sorted_list or new_g < parent.g:
                        parent.navigated_from = current
                        parent.g = new_g

                        if parent not in sorted_list:
                                sorted_list.append(parent)
                                shortest_path[parent.y][parent.x] = '*'
        return False



def run_algorithm(alg):
        done = False
        sorted_list = sort_open_list(open_list, alg)

        if alg == 'astar':
                while len(sorted_list) > 0 and not done:
                        sorted_list = sort_open_list(sorted_list, alg)
                        done = a_star(sorted_list)
                        #print_board()
        elif alg == 'BFS':
                while len(open_list) > 0 and not done:
                        done = BFS()
                        #print_board()
        elif alg == 'dijkstra':
                while len(sorted_list) > 0 and not done:
                        sorted_list = sort_open_list(sorted_list, alg)
                        done = dijkstra(sorted_list)
        
        print_board()
        print len(sorted_list)
        print len(closed_list)                        
                
def run():
        print 'Choose algorithm: astar, BFS or dijkstra:'
        alg = input('')
        #board = input('Choose board: board-x-y (x: 1-2, y: 1-5)'
        run_algorithm(str(alg))#,board)



run()

	
