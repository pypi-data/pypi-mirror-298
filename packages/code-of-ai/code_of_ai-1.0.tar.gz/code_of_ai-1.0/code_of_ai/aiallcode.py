
def alpha():
    code ="""
MAX, MIN = 1000, -1000
 
# Returns optimal value for current player 
#(Initially called for root and maximizer) 
def minimax(depth, nodeIndex, maximizingPlayer, 
            values, alpha, beta): 
  
    # Terminating condition. i.e 
    # leaf node is reached 
    if depth == 3: 
        return values[nodeIndex] 
 
    if maximizingPlayer: 
      
        best = MIN
 
        # Recur for left and right children 
        for i in range(0, 2): 
             
            val = minimax(depth + 1, nodeIndex * 2 + i, 
                          False, values, alpha, beta) 
            best = max(best, val) 
            alpha = max(alpha, best) 
 
            # Alpha Beta Pruning 
            if beta <= alpha: 
                break
          
        return best 
      
    else:
        best = MAX
 
        # Recur for left and 
        # right children 
        for i in range(0, 2): 
          
            val = minimax(depth + 1, nodeIndex * 2 + i, 
                            True, values, alpha, beta) 
            best = min(best, val) 
            beta = min(beta, best) 
 
            # Alpha Beta Pruning 
            if beta <= alpha: 
                break
          
        return best 
      
 
values = [3, 5, 6, 9, 1, 2, 0, -1]  
print("The optimal value is :", minimax(0, 0, True, values, MIN, MAX)



"""
    return code

def bfs():
  code = """
graph = {
  '5' : ['3','7'],
  '3' : ['2', '4'],
  '7' : ['8'],
  '2' : [],
  '4' : ['8'],
  '8' : []
}

visited = [] 
queue = []     

def bfs(visited, graph, node): 
  visited.append(node)
  queue.append(node)

  while queue:          
    m = queue.pop(0) 
    print (m, end = " ") 

    for neighbour in graph[m]:
      if neighbour not in visited:
        visited.append(neighbour)
        queue.append(neighbour)

print("Following is the Breadth-First Search")
bfs(visited, graph, '5') 


"""
  return code

def cannibal():
    code = """
from collections import deque
#define the initial and goal states
START_STATE = (3,3,0,0,0) #(left_missionaries,left_cannibals,right_missionaries,right_cannibals,boat_position)
GOAL_STATE = (0,0,3,3,1) #(left_missionaries,left_cannibals,right_missionaries,right_cannibals,boat_position)
def is_valid_state(state):
    lm, lc, rm, rc,_ = state # the  '_' is given because we dont want to
    
    if (lm > 0 and lm < lc) or (rm > 0 and rm < rc):         #check if missionaries are safe on both sides
        return False
    return True

def get_next_states(state):
    lm, lc, rm, rc, boat = state
    next_states = []
    if boat == 0: #Boat on the left side
        for m, c in [(2,0),(1,0),(0,1),(1,1),(0,2)]:
            new_lm = lm - m
            new_lc = lc - c
            new_rm = rm + m
            new_rc = rc + c
            if 0 <= new_lm <= 3 and 0 <= new_lc <= 3 and 0 <= new_rm <= 3 and 0 <= new_rc <= 3:
                if is_valid_state((new_lm,new_lc,new_rm,new_rc, 1)):
                    next_states.append((new_lm, new_lc, new_rm,new_rc,1))
    else: #Boat on the right side
        for m,c in [(2,0),(1,0),(0,1),(1,1),(0,2)]:
            new_lm = lm + m
            new_lc = lc + c
            new_rm = rm - m
            new_rc = rc - c
            if 0 <= new_lm <= 3 and 0 <= new_lc <= 3 and 0 <= new_rm <= 3 and 0 <= new_rc <= 3:
                if is_valid_state((new_lm,new_lc,new_rm,new_rc, 0)):
                    next_states.append((new_lm,new_lc,new_rm,new_rc, 0))
    return next_states

def bfs(start,goal):
    queue = deque([(start, [])])
    visited = set()
    while queue:
        state, path = queue.popleft()
        if state in visited:
            continue
        visited.add(state)
        if state == goal:
            return path
        for next_state in get_next_states(state):
            queue.append((next_state, path + [next_state]))
    return None

def print_state(state):
    lm, lc, rm, rc, boat = state
    boat_position = 'left' if boat == 0 else 'right'
    print(f"Left:{lm} missionaries, {lc} cannibals | Right: {rm} missionaries, {rc} cannibals | Boat: {boat_position}")

#Example usage
solution = bfs(START_STATE,GOAL_STATE)
if solution:
    for state in solution:
        print_state(state)
        print()
else:
    print("No solution found.")


"""
    return code

def card():
    code = """
import random

suits = ['Hearts' , 'Diamonds' , 'Clubs' , 'Spades']
ranks = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']

deck= [f'{rank} of {suit}' for suit in suits for rank in ranks]

random.shuffle(deck)

for i in range(3):
    print(deck[i])


"""
    return code

def constraint():
    code = """
from constraint import Problem
problem = Problem()
variables = ["x", "y", "z"]
domains = {"x": [1,2,3], "y":[1,2,3], "z":[1,2,3]}
for variable in variables:
    problem.addVariable(variable, domains[variable])
def constraint_func(x, y, z):
    return x + y + z == 6
problem.addConstraint(constraint_func, variables)
solutions = problem.getSolutions()
# Print the solutions
for solution in solutions:
    print(solution)

"""
    return code



def dfs():
    code = """
print("****** DEPTH FIRST SEARCH *******")
graph1 = {
    'A': set(['B', 'C']),
    'B': set(['A', 'D', 'E']),
    'C': set(['A', 'F']),
    'D': set(['B']),
    'E': set(['B', 'F']),
    'F': set(['C', 'E']) }
def dfs(graph, node, visited):
    if node not in visited:
        visited.append(node)
        for n in graph[node]:
            dfs(graph,n, visited)
        return visited
visited = dfs(graph1,'A', [])
print(visited)


"""
    return code


def hill():
    code = """
import math

def hill_climbing(f, x_start, step_size, max_iterations):
    x_current = x_start
    
    for i in range(max_iterations):
        current_value = f(x_current)
        
        x_left = x_current - step_size
        x_right = x_current + step_size
       
        left_value = f(x_left)
        right_value = f(x_right)
        
        if left_value > current_value:
            x_current = x_left
        elif right_value > current_value:
            x_current = x_right
       
        else:
            break
    
    return x_current, f(x_current)


def f(x):
    return -(x - 3) ** 2 + 10  

x_start = 0  
step_size = 0.1  
max_iterations = 100 

solution, max_value = hill_climbing(f, x_start, step_size, max_iterations)

print(f"Found maximum at x = {solution}, f(x) = {max_value}")


"""
    return code


def puzzle():
    code = """
import random

def print_board(board):
    for row in board:
        print(" ".join(str(num) if num != 0 else ' ' for num in row))
    print()

def find_blank(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                return i, j

def is_valid_move(x, y):
    return 0 <= x < 3 and 0 <= y < 3

def make_move(board, dx, dy):
    blank_x, blank_y = find_blank(board)
    new_x, new_y = blank_x + dx, blank_y + dy
    if is_valid_move(new_x, new_y):
        board[blank_x][blank_y], board[new_x][new_y] = board[new_x][new_y], board[blank_x][blank_y]
        return True
    return False

def is_solved(board):
    return all(board[i][j] == i * 3 + j + 1 for i in range(3) for j in range(3) if board[i][j] != 0)

def shuffle_board(board, moves=100):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
    for _ in range(moves):
        dx, dy = random.choice(directions)
        make_move(board, dx, dy)

def main():
    solved_board = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    current_board = [row[:] for row in solved_board]
    shuffle_board(current_board)
    
    print("Welcome to the 8-puzzle game!")
    print_board(current_board)

    while not is_solved(current_board):
        move = input("Enter move (left, right, up, down): ").strip().lower()
        if move == "left":
            if make_move(current_board, 0, -1):
                print_board(current_board)
            else:
                print("Invalid move!")
        elif move == "right":
            if make_move(current_board, 0, 1):
                print_board(current_board)
            else:
                print("Invalid move!")
        elif move == "up":
            if make_move(current_board, -1, 0):
                print_board(current_board)
            else:
                print("Invalid move!")
        elif move == "down":
            if make_move(current_board, 1, 0):
                print_board(current_board)
            else:
                print("Invalid move!")
        else:
            print("Invalid input. Please enter left, right, up, or down.")
    
    print("Congratulations! You solved the puzzle.")

if __name__ == "__main__":
    main()

"""
    return code

def queen():
    code = """
n=int(input("Enter n  : "))
board=[[0 for i in range(n)]for i in range(n)]

for row in board:
    print(row)

def check_column(board,row,column):
    for i in range(row,-1,-1):
        if board[i][column]==1:
            return False
    return True

def check_diagonal(board,row,column):
    for i,j in zip(range(row,-1,-1),range(column,-1,-1)):
        if board[i][j]==1:
            return False
    for i,j in zip(range(row,-1,-1),range(column,n)):
        if board[i][j]==1:
            return False
    return True

def nqn(board,row):
    if row==n:
        return True
    
    for i in range(n):
        if(check_column(board,row,i)==True and check_diagonal(board,row,i==True)):
            board[row][i]=1
            if nqn(board,row+1):
                return True
            board[row][i]=0
    return False

nqn(board,0)

for row in board:
    print(row)


"""
    return code


def salesman():
   code = """

from itertools import permutations
V = 4
def travellingSalesmanProblem(graph,s):
   vertex = []
   for i in range(V):
       if i != s:
           vertex.append(i)


   min_path = 10000
   next_permutation = permutations(vertex)
   for i in next_permutation:
       current_pathweight = 0
       k = s
       for j in i:
           current_pathweight += graph[k][j]
           k = j
       current_pathweight += graph[k][s]
       min_path = min(min_path, current_pathweight)


   return min_path


graph = [[0,10,15,20],[10,0,35,25],[15,35,0,30],[20,25,30,0]]
s = 0
print(travellingSalesmanProblem(graph, s))


"""
   return code


def tic():
    code = """

print("******TIC-TAC-TOE******") 
import os 
import time 

board = [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '] 
player = 1 
 
########win Flags########## 
Win = 1 
Draw = -1 
Running = 0 
Stop = 1 
########################### 
Game = Running 
Mark = 'X' 
 
#This Function Draws Game Board
def DrawBoard(): 
    print(" %c | %c | %c " % (board[1],board[2],board[3])) 
    print("___|___|___") 
    print(" %c | %c | %c " % (board[4],board[5],board[6])) 
    print("___|___|___") 
    print(" %c | %c | %c " % (board[7],board[8],board[9])) 
    print("   |   | ") 
 
#This Function Checks position is empty or not 
def CheckPosition(x): 
    if(board[x] == ' '): 
        return True 
    else: 
        return False 
 
#This Function Checks player has won or not 
def CheckWin(): 
    global Game 
    #Horizontal winning condition 
    if(board[1] == board[2] and board[2] == board[3] and board[1] != ' '): 
        Game = Win 
    elif(board[4] == board[5] and board[5] == board[6] and board[4] != ' '): 
        Game = Win 
    elif(board[7] == board[8] and board[8] == board[9] and board[7] != ' '): 
        Game = Win 
    #Vertical Winning Condition 
    elif(board[1] == board[4] and board[4] == board[7] and board[1] != ' '): 
        Game = Win 
    elif(board[2] == board[5] and board[5] == board[8] and board[2] != ' '): 
        Game = Win 
    elif(board[3] == board[6] and board[6] == board[9] and board[3] != ' '): 
        Game=Win 

    #Diagonal Winning Condition 
    elif(board[1] == board[5] and board[5] == board[9] and board[5] != ' '): 
        Game = Win 
    elif(board[3] == board[5] and board[5] == board[7] and board[5] != ' '): 
        Game=Win 
    #Match Tie or Draw Condition 
    elif(board[1]!=' ' and board[2]!=' ' and board[3]!=' ' and board[4]!=' ' and board[5]!=' ' and board[6]!=' ' and board[7]!=' ' and board[8]!=' ' and board[9]!=' '):
        Game=Draw 
    else: 
        Game=Running 
 
print("Tic-Tac-Toe Game") 
print("Player 1 [X] --- Player 2 [O]\n") 
print() 
print() 
print("Please Wait...") 
time.sleep(1) 
while(Game == Running): 
    os.system('cls') 
    DrawBoard() 
    if(player % 2 != 0): 
        print("Player 1's chance") 
        Mark = 'X' 
    else: 
        print("Player 2's chance") 
        Mark = 'O' 
    choice = int(input("Enter the position between [1-9] where you want to mark : ")) 
    if(CheckPosition(choice)): 
        board[choice] = Mark 
        player+=1 
        CheckWin() 
 
os.system('cls') 
DrawBoard() 
if(Game==Draw): 
    print("Game Draw") 
elif(Game==Win): 
    player-=1 
    if(player%2!=0): 
        print("Player 1 Won") 
    else: 
        print("Player 2 Won")


"""
    return code



def tower():
    code = """

def TowerOfHanoi(n , source, destination, auxiliary):
    if n==1:
        print ("Move disk 1 from source",source,"to destination",destination)
        return
    TowerOfHanoi(n-1, source, auxiliary, destination)
    print ("Move disk",n,"from source",source,"to destination",destination)
    TowerOfHanoi(n-1, auxiliary, destination, source)
         
# Driver code
n = 3
TowerOfHanoi(n,'A','B','C')


"""
    return code


def water():
    code = """
from collections import deque

def print_steps(steps):
    for step in steps:
        print(step)

def water_jug_problem(x,y,z):
    if z >max(x,y):
        return "not possible"
    visited = set()
    queue=deque([(0,0,[])])
    visited.add((0,0))
    while queue:
        a,b,path=queue.popleft()
        print(f"current state:jug1 ={a},jug2={b}")

        if a == z or b == z:
            path.append(f"reached target with jug1 ={a},jug2={b}")
            print_steps(path)
            return True
        possible_state=[
            (x,b,path+[f"fill jug1"]),
            (a,y,path+[f"fill jug2"]),
            (0,b,path+[f"fill jug1"]),
            (a,0,path+[f"fill jug2"]),
            (min(a+b,x),b-(min(a+b,x)-a),path +[f"pour jug2 into jug1"]),
            (a-(min(a+b,y)-b),min(a+b,y),path+[f"pour jug1 into jug2"]),
            ]
        for state in possible_state:
            new_a,new_b,new_path=state
            if(new_a,new_b) not in visited:
                visited.add((new_a,new_b))
                queue.append((new_a,new_b,new_path))
    print("No solution found")
    return False
x=4
y=3
z=2
result=water_jug_problem(x,y,z)
print("can measure",z,"liters?",result)


"""
    return code












