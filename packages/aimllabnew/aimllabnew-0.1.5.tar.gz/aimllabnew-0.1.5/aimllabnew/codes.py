def a_star():
    code = '''import heapq

class Node:
    def __init__(self, name, heuristic):
        self.name = name
        self.heuristic = heuristic
        self.neighbors = []

    def add_neighbor(self, neighbor, weight):
        self.neighbors.append((neighbor, weight))

def a_star_search(start, goal):
    open_list = []
    heapq.heappush(open_list, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: start.heuristic}

    while open_list:
        current_f, current = heapq.heappop(open_list)
        if current == goal:
            path = []
            while current in came_from:
                path.append(current.name)
                current = came_from[current]
            path.append(start.name)
            return path[::-1], g_score[goal]

        for neighbor, weight in current.neighbors:
            tentative_g_score = g_score[current] + weight
            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + neighbor.heuristic
                heapq.heappush(open_list, (f_score[neighbor], neighbor))

    return None, float('inf')

nodes = {}
num_nodes = int(input("Enter the number of nodes: "))
for _ in range(num_nodes):
    name = input("Enter node name: ")
    heuristic = float(input(f"Enter heuristic value for {name}: "))
    nodes[name] = Node(name, heuristic)

num_edges = int(input("Enter the number of edges: "))
for _ in range(num_edges):
    node1 = input("Enter the start node of the edge: ")
    node2 = input("Enter the end node of the edge: ")
    weight = float(input(f"Enter the weight of the edge between {node1} and {node2}: "))
    nodes[node1].add_neighbor(nodes[node2], weight)
    nodes[node2].add_neighbor(nodes[node1], weight)

start_node = nodes[input("Enter the start node: ")]
goal_node = nodes[input("Enter the goal node: ")]

path, cost = a_star_search(start_node, goal_node)
if path:
    print("Path found:", " -> ".join(path))
    print("Total cost:", cost)
else:
    print("No path found")'''
    print(code)


def eight_puzzle():
    code = '''import heapq

def manhattan_distance(state, goal):
    distance = 0
    for i in range(1, 9):
        current_index = state.index(i)
        goal_index = goal.index(i)
        current_row, current_col = divmod(current_index, 3)
        goal_row, goal_col = divmod(goal_index, 3)
        distance += abs(current_row - goal_row) + abs(current_col - goal_col)
    return distance

class Node:
    def __init__(self, state, parent=None, move=None, depth=0, cost=0):
        self.state = state
        self.parent = parent
        self.move = move
        self.depth = depth
        self.cost = cost

    def __lt__(self, other):
        return (self.cost + self.depth) < (other.cost + other.depth)

def get_neighbors(state):
    neighbors = []
    index = state.index(0)
    row, col = divmod(index, 3)
    
    if row > 0:
        new_state = state[:]
        new_state[index], new_state[index - 3] = new_state[index - 3], new_state[index]
        neighbors.append((new_state, "Up"))
        
    if row < 2:
        new_state = state[:]
        new_state[index], new_state[index + 3] = new_state[index + 3], new_state[index]
        neighbors.append((new_state, "Down"))
        
    if col > 0:
        new_state = state[:]
        new_state[index], new_state[index - 1] = new_state[index - 1], new_state[index]
        neighbors.append((new_state, "Left"))
    if col < 2:
        new_state = state[:]
        new_state[index], new_state[index + 1] = new_state[index + 1], new_state[index]
        neighbors.append((new_state, "Right"))
        
    return neighbors

def a_star(start, goal):
    open_list = []
    closed_list = set()
    
    start_node = Node(start, None, None, 0, manhattan_distance(start, goal))
    heapq.heappush(open_list, start_node)
    
    while open_list:
        current_node = heapq.heappop(open_list)
        
        if current_node.state == goal:
            moves = []
            while current_node.parent:
                moves.append(current_node.move)
                current_node = current_node.parent
            return moves[::-1]
        
        closed_list.add(tuple(current_node.state))
        
        for neighbor, move in get_neighbors(current_node.state):
            if tuple(neighbor) in closed_list:
                continue
            
            neighbor_node = Node(
                neighbor,
                current_node,
                move,
                current_node.depth + 1,
                manhattan_distance(neighbor, goal)
            )
            
            heapq.heappush(open_list, neighbor_node)
            
    return None

def get_puzzle_input():
    print("Enter the 8-puzzle start state (9 numbers, 0 for the empty space):")
    start = list(map(int, input().split()))
    if len(start) != 9 or any(x < 0 or x > 8 for x in start):
        print("Invalid input. Please enter exactly 9 numbers between 0 and 8.")
        return None, None
    print("Enter the 8-puzzle goal state (9 numbers, 0 for the empty space):")
    goal = list(map(int, input().split()))
    if len(goal) != 9 or any(x < 0 or x > 8 for x in goal):
        print("Invalid input. Please enter exactly 9 numbers between 0 and 8.")
        return None, None
    
    return start, goal

start, goal = get_puzzle_input()
if start and goal:
    solution = a_star(start, goal)
    if solution:
        print("Moves to solve the puzzle:", solution)
    else:
        print("No solution found.")

'''
    print(code)



def csp():
    code = '''import itertools

def solve_cryptarithm(words, result):
    unique_letters = ''.join(set(''.join(words) + result))
    
    if len(unique_letters) > 10:
        print("Too many unique letters for a single-digit solution.")
        return
    
    digits = '0123456789'
    
    for perm in itertools.permutations(digits, len(unique_letters)):
        letter_to_digit = dict(zip(unique_letters, perm))
        
        def word_to_number(word):
            return int(''.join(letter_to_digit[letter] for letter in word))
        
        if any(letter_to_digit[word[0]] == '0' for word in words + [result]):
            continue
        
        sum_words = sum(word_to_number(word) for word in words)
        
        if sum_words == word_to_number(result):
            print("Solution found!")
            for word in words:
                print(f"{word} = {word_to_number(word)}")
            print(f"{result} = {word_to_number(result)}")
            print(f"Letter to Digit Mapping: {letter_to_digit}")
            return
    
    print("No solution found.")

input_words = input("Enter the words to sum (space-separated): ").upper().split()
input_result = input("Enter the result word: ").upper()

solve_cryptarithm(input_words, input_result)


'''
    print(code)



def sudoku():
    code = '''
def is_valid(board, row, col, num):
    for x in range(9):
        if board[row][x] == num or board[x][col] == num:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def solve_sudoku(board):
    empty = find_empty_location(board)
    if not empty:
        return True
    row, col = empty
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            board[row][col] = 0
    return False

def find_empty_location(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return (row, col)
    return None

def print_board(board):
    for row in board:
        print(" ".join(str(num) if num != 0 else '.' for num in row))

def input_board():
    print("Enter the Sudoku puzzle (9x9 grid). Use 0 for empty cells:")
    board = []
    for i in range(9):
        while True:
            try:
                row = list(map(int, input(f"Row {i+1}: ").strip().split()))
                if len(row) != 9:
                    raise ValueError("Each row must have exactly 9 numbers.")
                if any(num < 0 or num > 9 for num in row):
                    raise ValueError("Numbers must be between 0 and 9.")
                board.append(row)
                break
            except ValueError as e:
                print(f"Invalid input: {e}. Please enter the row again.")
    return board

if __name__ == "__main__":
    board = input_board()
    if solve_sudoku(board):
        print("Solved Sudoku:")
        print_board(board)
    else:
        print("No solution exists")

'''
    print(code)




def ttt():
    code = '''
import itertools

def print_board(board):
    print('\n'.join(' '.join(row) for row in board), end='\n\n')

def check_win(board, player):
    win = [player] * 3
    return (any(all(cell == player for cell in row) for row in board) or        # Check rows
            any(all(board[i][j] == player for i in range(3)) for j in range(3)) or  # Check columns
            all(board[i][i] == player for i in range(3)) or                # Check main diagonal
            all(board[i][2 - i] == player for i in range(3)))              # Check anti-diagonal

def is_board_full(board):
    return all(cell != ' ' for row in board for cell in row)

def minimax(board, depth, is_maximizing):
    if check_win(board, 'X'): return 10 - depth
    if check_win(board, 'O'): return depth - 10
    if is_board_full(board): return 0

    best_score = float('-inf') if is_maximizing else float('inf')
    for i, j in itertools.product(range(3), repeat=2):
        if board[i][j] == ' ':
            board[i][j] = 'X' if is_maximizing else 'O'
            score = minimax(board, depth + 1, not is_maximizing)
            board[i][j] = ' '
            best_score = max(score, best_score) if is_maximizing else min(score, best_score)
    return best_score

def find_best_move(board):
    best_move = None
    best_score = float('-inf')
    for i, j in itertools.product(range(3), repeat=2):
        if board[i][j] == ' ':
            board[i][j] = 'X'
            score = minimax(board, 0, False)
            board[i][j] = ' '
            if score > best_score:
                best_score = score
                best_move = (i, j)
    return best_move

def convert_to_indices(position):
    return (position - 1) // 3, (position - 1) % 3

board = [[' ' for _ in range(3)] for _ in range(3)]
print_board(board)

while True:
    try:
        pos = int(input("Enter position for O (1-9): "))
        row, col = convert_to_indices(pos)
        if board[row][col] == ' ':
            board[row][col] = 'O'
            print("O moves:")
            print_board(board)
            if check_win(board, 'O'):
                print("O wins!")
                break
            if is_board_full(board):
                print("It's a tie!")
                break
        else:
            print("Cell already taken. Try again.")
    except (ValueError, IndexError):
        print("Invalid input. Enter a number between 1 and 9.")

    move = find_best_move(board)
    if move:
        board[move[0]][move[1]] = 'X'
        print("X moves:")
        print_board(board)
        if check_win(board, 'X'):
            print("X wins!")
            break
        if is_board_full(board):
            print("It's a tie!")
            break


'''
    print(code)

