from typing import List, Optional, Tuple

# Returns the letter of the non-specified player
def _switch_player(player: str) -> str:
    return 'X' if player == 'O' else 'O'

# Returns a copy of the given board
def _copy_board(board: List[List]) -> List[List]:
    return [[x for x in row] for row in board]

# Returns whether the specified spot in the board is empty or not
def _empty_index(board: List[List], row: int, col: int) -> bool:
    return board[row][col] == ' '

# Returns the winner's letter, or None if there is no winner
def _check_winner(board: List[List]) -> Optional[str]:
    for letter in ['X', 'O']:
        # Check rows
        for i in range(3):
            winner = True

            for j in range(3):
                if board[i][j] != letter:
                    winner = False
                    break
            
            if winner:
                return letter

        # Check columns 
        for i in range(3):
            winner = True

            for j in range(3):
                if board[j][i] != letter:
                    winner = False
                    break
            
            if winner:
                return letter
            
        # Check top-left to bottom-right diagonal
        winner = True

        for i in range(3):
            if board[i][i] != letter:
                winner = False
                break
        
        if winner:
            return letter
        
        # Check bottom-left to top-right diagonal
        winner = True

        for i in range(3):
            if board[i][2-i] != letter:
                winner = False
                break
        
        if winner:
            return letter

    return None

# Returns whether the board is full or not
def _check_draw(board: List[List]) -> bool:
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                return False

    return True

# Prints the game board
def _print_board(board: List[List]):
    for i in range(3):
        for j in range(3):
            print(board[i][j], end=("\n" if j == 2 else " | "))

        print("" if i == 2 else "---------")

class Game:

    def __init__(self, human: str):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.human = human
        self.cpu = _switch_player(human)
        self.turn = 'X'

    # Game loop
    # Returns the winner's corresponding letter, or None if there was a draw
    def play(self) -> Optional[str]:
        while True:
            self._take_turn()

            winner = _check_winner(self.board)

            if winner:
                _print_board(self.board)
                return winner
            
            if _check_draw(self.board):
                return None

    # Prompts the appropriate player to take their turn and updates the board accordingly
    def _take_turn(self):
        _print_board(self.board)

        row, col = 0, 0

        if self.turn == self.human:
            input_num = 0
            
            while input_num < 11 or input_num > 33 or not _empty_index(self.board, row, col):
                user_input = input("Your turn (<row><col>, 11-33): ")

                if not user_input.isdigit():
                    continue
                
                input_num = int(user_input)
                row = (input_num // 10) - 1
                col = (input_num % 10) - 1
        else:
            print("CPU's turn.")

            row, col = self._minimax()

        self.board[row][col] = self.turn
        self.turn = _switch_player(self.turn)

        print("\n=================================\n")

    # Returns the optimal move (row, col)
    def _minimax(self) -> Tuple[int, int]:
        row, col, max_value = 0, 0, float('-inf')

        for i in range(3):
            for j in range(3):
                if not _empty_index(self.board, i, j):
                    continue

                new_board = _copy_board(self.board)
                new_board[i][j] = self.cpu

                # Check if immediate move is a winner
                if _check_winner(new_board) == self.cpu:
                    return i, j

                value = self._dfs(new_board, self.human)
                
                if value > max_value:
                    row, col, max_value = i, j, value

        return row, col

    # Returns the minimax value of the provided board, starting on 'player's turn
    def _dfs(self, board: List[List], player: str) -> int:
        winner = _check_winner(board)

        if winner:
            return 1 if winner == self.cpu else -1
        
        if _check_draw(board):
            return 0
        
        # CPU player's turn
        if player == self.cpu:
            max_value = float('-inf')

            for i in range(3):
                for j in range(3):
                    if not _empty_index(board, i, j):
                        continue

                    new_board = _copy_board(board)
                    new_board[i][j] = self.cpu
                    
                    max_value = max(max_value, self._dfs(new_board, _switch_player(self.cpu)))
            
            return max_value
        # Human player's turn
        else:
            min_value = float('inf')

            for i in range(3):
                for j in range(3):
                    if not _empty_index(board, i, j):
                        continue

                    new_board = _copy_board(board)
                    new_board[i][j] = self.human

                    min_value = min(min_value, self._dfs(new_board, _switch_player(self.human)))

            return min_value