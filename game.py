from typing import List, Optional, Tuple

# Returns the letter of the non-specified player
def switch_player(player: str) -> str:
    return 'X' if player == 'O' else 'O'

class Game:

    def __init__(self, human: str):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.human = human
        self.cpu = switch_player(human)
        self.turn = 'X'

    # Game loop
    # Returns the winner's corresponding letter, or None if there was a draw
    def play(self) -> Optional[str]:
        while True:
            self.take_turn()

            winner = self.check_winner(self.board)

            if winner:
                self.print_board()
                return winner
            
            if self.check_draw(self.board):
                return None

    # Prompts the appropriate player to take their turn and updates the board accordingly
    def take_turn(self):
        self.print_board()

        if self.turn == self.human:
            input_num, row, col = 0, 0, 0
            
            while input_num < 11 or input_num > 33 or not self.empty_index(self.board, row, col):
                user_input = input("Your turn (<row><col>, 11-33): ")

                if not user_input.isdigit():
                    continue
                
                input_num = int(user_input)
                row = (input_num // 10) - 1
                col = (input_num % 10) - 1

            self.board[row][col] = self.human

            self.turn = self.cpu 
        else:
            print("CPU's turn.")

            row, col = self.minimax()
            self.board[row][col] = self.cpu

            self.turn = self.human
        
        print("\n=================================\n")

    # Returns whether the specified spot in the board is empty or not
    def empty_index(self, board: List[List], row: int, col: int) -> bool:
        return board[row][col] == ' '

    # Returns a copy of the given board
    def copy_board(self, board: List[List]) -> List[List]:
        return [[x for x in row] for row in board]

    # Returns the optimal move (row, col)
    def minimax(self) -> Tuple[int, int]:
        row, col, max_value = 0, 0, float('-inf')

        for i in range(3):
            for j in range(3):
                if not self.empty_index(self.board, i, j):
                    continue

                new_board = self.copy_board(self.board)
                new_board[i][j] = self.cpu

                value = self.dfs(new_board, self.human)
                
                if value > max_value:
                    row, col, max_value = i, j, value

        return row, col

    # Returns the minimax value of the provided board, starting on 'player's turn
    def dfs(self, board: List[List], player: str) -> int:
        winner = self.check_winner(board)

        if winner:
            return 1 if winner == self.cpu else -1
        
        if self.check_draw(board):
            return 0
        
        # CPU player's turn
        if player == self.cpu:
            max_value = float('-inf')

            for i in range(3):
                for j in range(3):
                    if not self.empty_index(board, i, j):
                        continue

                    new_board = self.copy_board(board)
                    new_board[i][j] = self.cpu
                    
                    max_value = max(max_value, self.dfs(new_board, switch_player(self.cpu)))
            
            return max_value
        # Human player's turn
        else:
            min_value = float('inf')

            for i in range(3):
                for j in range(3):
                    if not self.empty_index(board, i, j):
                        continue

                    new_board = self.copy_board(board)
                    new_board[i][j] = self.human

                    min_value = min(min_value, self.dfs(new_board, switch_player(self.human)))

            return min_value

    # Returns the winner's letter, or None if there is no winner
    def check_winner(self, board: List[List]) -> Optional[str]:
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
    def check_draw(self, board: List[List]) -> bool:
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    return False

        return True

    # Prints the game board
    def print_board(self):
        for i in range(3):
            for j in range(3):
                print(self.board[i][j], end=("\n" if j == 2 else " | "))

            print("" if i == 2 else "---------")