import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe - Minimax AI")
        self.board = ['' for _ in range(9)]
        self.buttons = []
        self.current_turn = 'X'  # Human starts first (X)
        self.create_buttons()
        self.status_label = tk.Label(self.root, text="Your Turn (X)", font=('Arial', 20))
        self.status_label.grid(row=3, column=0, columnspan=3)
        self.score_x = 0  # Initialize score for X
        self.score_o = 0  # Initialize score for O
        self.create_scoreboard()
        self.game_mode = 'Single Player'  # Default game mode
        self.create_menu()

    def create_menu(self):
        """Create menu for game mode selection and other options."""
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        game_menu = tk.Menu(menu)
        menu.add_cascade(label="Game", menu=game_menu)
        game_menu.add_command(label="Single Player", command=self.set_single_player)
        game_menu.add_command(label="Multiplayer", command=self.set_multiplayer)
        game_menu.add_separator()
        game_menu.add_command(label="Restart", command=self.reset_game)
        game_menu.add_command(label="Exit", command=self.root.quit)

    def set_single_player(self):
        """Set game mode to Single Player."""
        self.game_mode = 'Single Player'
        self.reset_game()  # Reset game for new mode
        self.status_label.config(text="Your Turn (X)")

    def set_multiplayer(self):
        """Set game mode to Multiplayer."""
        self.game_mode = 'Multiplayer'
        self.reset_game()  # Reset game for new mode
        self.status_label.config(text="Your Turn (X)")

    def create_buttons(self):
        """Create the 3x3 grid of buttons."""
        for i in range(9):
            button = tk.Button(self.root, text='', font=('Arial', 40), width=5, height=2,
                               command=lambda i=i: self.on_button_click(i))
            button.grid(row=i // 3, column=i % 3)
            self.buttons.append(button)

    def create_scoreboard(self):
        """Create a scoreboard to track scores."""
        self.score_label = tk.Label(self.root, text=f"Score - X: {self.score_x} | O: {self.score_o}", font=('Arial', 20))
        self.score_label.grid(row=4, column=0, columnspan=3)

    def on_button_click(self, index):
        """Handle human player (X) move."""
        if self.board[index] == '' and (self.current_turn == 'X' or self.game_mode == 'Multiplayer'):
            self.board[index] = 'X'
            self.buttons[index].config(text='X', state=tk.DISABLED)
            if self.check_winner():
                return
            self.current_turn = 'O'
            self.status_label.config(text="AI's Turn (O)")
            if self.game_mode == 'Single Player':
                self.root.after(500, self.ai_move)
            else:
                self.status_label.config(text="Your Turn (O)")

    def ai_move(self):
        """AI (O) makes the move using Minimax algorithm."""
        best_move = self.minimax(self.board, True)[1]
        self.board[best_move] = 'O'
        self.buttons[best_move].config(text='O', state=tk.DISABLED)

        if self.check_winner():
            return

        self.current_turn = 'X'
        self.status_label.config(text="Your Turn (X)")

    def check_winner(self):
        """Check for a winner or a draw."""
        winner = None
        winning_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
            (0, 4, 8), (2, 4, 6)              # Diagonals
        ]

        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != '':
                winner = self.board[combo[0]]
                break

        if winner:
            self.update_score(winner)
            self.status_label.config(text=f"{winner} Wins!")
            messagebox.showinfo("Game Over", f"{winner} Wins!")
            self.reset_game()
            return True
        elif '' not in self.board:
            self.status_label.config(text="It's a Draw!")
            messagebox.showinfo("Game Over", "It's a Draw!")
            self.reset_game()
            return True
        return False

    def update_score(self, winner):
        """Update the score based on the winner."""
        if winner == 'X':
            self.score_x += 1
        elif winner == 'O':
            self.score_o += 1
        self.score_label.config(text=f"Score - X: {self.score_x} | O: {self.score_o}")

    def reset_game(self):
        """Reset the game to start a new round."""
        self.board = ['' for _ in range(9)]
        for button in self.buttons:
            button.config(text='', state=tk.NORMAL)
        self.current_turn = 'X'
        self.status_label.config(text="Your Turn (X)")

    def minimax(self, board, is_maximizing):
        """Minimax algorithm implementation."""
        winner = self.check_winner_in_board(board)
        if winner == 'O':
            return 1, -1  # AI wins
        elif winner == 'X':
            return -1, -1  # Human wins
        elif winner is None and '' not in board:
            return 0, -1  # Draw

        if is_maximizing:
            best_value = -float('inf')
            best_move = -1
            for i in range(9):
                if board[i] == '':
                    board[i] = 'O'  # AI move
                    value = self.minimax(board, False)[0]
                    board[i] = ''  # Undo move
                    if value > best_value:
                        best_value = value
                        best_move = i
            return best_value, best_move
        else:
            best_value = float('inf')
            best_move = -1
            for i in range(9):
                if board[i] == '':
                    board[i] = 'X'  # Human move
                    value = self.minimax(board, True)[0]
                    board[i] = ''  # Undo move
                    if value < best_value:
                        best_value = value
                        best_move = i
            return best_value, best_move

    def check_winner_in_board(self, board):
        """Check for a winner in the current board state."""
        winning_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
            (0, 4, 8), (2, 4, 6)              # Diagonals
        ]

        for combo in winning_combinations:
            if board[combo[0]] == board[combo[1]] == board[combo[2]] != '':
                return board[combo[0]]  # Return the winner ('X' or 'O')

        return None  # No winner

# Run the Tic-Tac-Toe game
root = tk.Tk()
game = TicTacToe(root)
root.mainloop()
