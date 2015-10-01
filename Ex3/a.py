from sys import stdin
from math import fabs

# var ikke definert i den gamle python-versjonen som 
# ligger paa noen av stud sine maskiner
True = 1
False = 0

def manhattan_number(node):
	return fabs(node.x - goal.x) + fabs(node.y -goal.y)

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

goal = None
shortest_path = [['.' for x in range(0,20)]for z in range(0,7)]
y = 0


for line in stdin:
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
	if len(open_list) > 0:
		open_list[0].g = 0
		open_list[0].f = 0 # Maa ORDNES
		open_list[0].on_path = True
		
	y = y+1


def get_parents(node):
	parents = []
	if( node.y < 6): # UP
		parents.append(board[node.y+1][node.x])
	if( node.y > 0): # DOWN
		parents.append(board[node.y-1][node.x])
	if( node.x < 19): # RIGHT
	 	parents.append(board[node.y][node.x+1])
	if( node.x > 0): #LEFT
		parents.append(board[node.y][node.x-1])
	return parents

def construct_path(current_node):

	shortest_path[current_node.y][current_node.x] = 'o'
	if current_node.navigated_from != None:
		current_node.on_path = True
		construct_path(current_node.navigated_from)
		


def a_star():
	#if len(open_list) == 0:
		#return
	current = open_list[0]
	if current.type == 'B':
		construct_path(current)	
		open_list.pop(0)

		while len(open_list) > 0:
			open_list.pop(0)
		return

	open_list.pop(0)
	closed_list.append(current)
	
	temp_parents = get_parents(current)
	for parent in temp_parents:
		if parent in closed_list:
			continue

		new_g = current.g + 0
		if parent not in open_list or new_g < parent.g:
			parent.navigated_from = current
			parent.g = new_g
			parent.f = parent.g + manhattan_number(parent)
			
			if parent not in open_list:
				open_list.append(parent)
	

		

			
def run():
	while len(open_list) > 0:
		a_star()

	for x in range(7):
		for y in range(20):
			if board[x][y].type == '#':
				shortest_path[x][y] = '#' 

	for i in shortest_path:
		print i



run()

	
