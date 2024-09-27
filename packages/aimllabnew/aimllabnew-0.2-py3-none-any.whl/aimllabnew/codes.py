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
node_data = input("Enter nodes with their heuristic values (e.g., 'A 1 B 2 C 3'): ").split()
for i in range(0, len(node_data), 2):
    name = node_data[i]
    heuristic = float(node_data[i+1])
    nodes[name] = Node(name, heuristic)

edge_data = input("Enter edges with weights (e.g., 'A B 1 B C 2'): ").split()
for i in range(0, len(edge_data), 3):
    node1 = edge_data[i]
    node2 = edge_data[i+1]
    weight = float(edge_data[i+2])
    nodes[node1].add_neighbor(nodes[node2], weight)
    nodes[node2].add_neighbor(nodes[node1], weight)

start_node = nodes[input("Enter the start node: ")]
goal_node = nodes[input("Enter the goal node: ")]

path, cost = a_star_search(start_node, goal_node)
if path:
    print("Path found:", " -> ".join(path))
    print("Total cost:", cost)
else:
    print("No path found")

    
    
  inputs: = Enter nodes with their heuristic values (e.g., 'A 1 B 2 C 3'): S 11.5 A 10.1 B 5.8 C 3.4 D 9.2 E 7.1 F 3.5 G 0
Enter edges with weights (e.g., 'A B 1 B C 2'): S A 3 S D 4 A B 4 A D 5 D E 2 B E 5 B C 4 E F 4 F G 3.5
Enter the start node: S
Enter the goal node: G
Path found: S -> D -> E -> F -> G
Total cost: 13.5
    
    '''
    print(code)


def eight_puzzle():
    code = '''import heapq

class PuzzleState:
    def __init__(self, board, goal, moves=0, prev=None):
        self.board = board
        self.goal = goal
        self.blank_pos = board.index('*')
        self.moves = moves
        self.prev = prev

    def __lt__(self, other):
        return (self.moves + self.heuristic()) < (other.moves + other.heuristic())

    def heuristic(self):
        """ Calculate Manhattan Distance """
        goal_positions = {i: (i // 3, i % 3) for i in range(1, 9)}
        goal_positions['*'] = (2, 2)  # The goal position for the empty tile
        distance = 0
        
        for i in range(9):
            tile = self.board[i]
            if tile == '*':
                continue
            tile = int(tile)  # Convert tile to integer for comparison
            goal_pos = goal_positions[tile]
            cur_pos = (i // 3, i % 3)
            distance += abs(cur_pos[0] - goal_pos[0]) + abs(cur_pos[1] - goal_pos[1])
        
        return distance

    def get_neighbors(self):
        """ Generate neighboring states by moving the blank tile """
        neighbors = []
        r, c = divmod(self.blank_pos, 3)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 3 and 0 <= nc < 3:
                new_blank_pos = nr * 3 + nc
                new_board = list(self.board)
                new_board[self.blank_pos], new_board[new_blank_pos] = new_board[new_blank_pos], new_board[self.blank_pos]
                neighbors.append(PuzzleState(tuple(new_board), self.goal, self.moves + 1, self))
        
        return neighbors

    def is_goal(self):
        return self.board == self.goal

    def __repr__(self):
        return '\n'.join([' '.join(map(str, self.board[i:i+3])) for i in range(0, 9, 3)])

def a_star(start_state):
    open_set = []
    heapq.heappush(open_set, start_state)
    closed_set = set()

    while open_set:
        current_state = heapq.heappop(open_set)

        if current_state.is_goal():
            return current_state

        closed_set.add(current_state.board)

        for neighbor in current_state.get_neighbors():
            if neighbor.board in closed_set:
                continue
            heapq.heappush(open_set, neighbor)

    return None

def get_user_input(prompt):
    """ Get a state from user input with validation """
    print(prompt)
    input_str = input().strip()
    input_list = input_str.split()
    
    if len(input_list) != 9 or '*' not in input_list or len(set(input_list)) != 9:
        raise ValueError("Invalid input. Make sure you enter exactly 9 values with numbers 1-8 and one '*' for the empty space.")

    return tuple(input_list)

# Main execution
if __name__ == "__main__":
    try:
        start_board = get_user_input("Enter the start state (9 values with numbers 1-8 and '*' for empty space):")
        goal_board = get_user_input("Enter the goal state (9 values with numbers 1-8 and '*' for empty space):")

        if start_board == goal_board:
            raise ValueError("Start state cannot be the same as the goal state.")

        start = PuzzleState(start_board, goal_board)
        solution = a_star(start)

        if solution:
            path = []
            while solution:
                path.append(solution)
                solution = solution.prev
            for state in reversed(path):
                print(state)
                print()
        else:
            print("No solution found.")
    except ValueError as e:
        print(e)

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

