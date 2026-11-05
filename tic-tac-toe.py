import tkinter as tk #GUI standard library.
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self, master):
        self.master = master
        master.title("Tic Tac Toe game")

        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'  # Human player starts
        self.buttons = [[None for _ in range(3)] for _ in range(3)]

         # Initialize scores
        self.x_score = 0
        self.o_score = 0
        self.score_label = tk.Label(master, text=f"Human(X): {self.x_score}  AI(O): {self.o_score}", font=("Sans serif", 20),fg="blue")
        self.score_label.grid(row=4, column=0, columnspan=3)  # Places the label below the game board.

        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(master, text=" ", font=("Helvetica", 36, "bold"),
                                             width=7, height=2, bg="black", relief=tk.GROOVE,
                                             command=lambda row=i, col=j: self.on_click(row, col))
                self.buttons[i][j].grid(row=i, column=j)

    def on_click(self, row, col):
        if self.board[row][col] == ' ':
            self.human_move(row, col)

    def human_move(self, row, col):
        self.board[row][col] = self.current_player
        self.buttons[row][col].config(text=self.current_player, state="disabled")

        if self.check_win(self.current_player):
            messagebox.showinfo("Game Over", f"{self.current_player} wins!!")
            # Update scores
            if self.current_player == 'X':
                self.x_score += 1
            else:
                self.o_score += 1
            self.update_score_label()  # Update the score label
            self.reset_board()
        elif self.check_draw():
            messagebox.showinfo("Game Over", "It's a draw!!")
            self.reset_board()
        else:
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            if self.current_player == 'O':  # AI's turn
                self.ai_move()

    def ai_move(self):
        # Find the best move using Minimax algorithm
        best_score = -float('inf')
        best_move = None
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    self.board[i][j] = 'O'
                    score = self.minimax(self.board, 0, False)
                    self.board[i][j] = ' '
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        self.human_move(best_move[0], best_move[1])

    def minimax(self, board, depth, is_maximizing):
        if self.check_win('O'):
            return 1
        if self.check_win('X'):
            return -1
        if self.check_draw():
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == ' ':
                        board[i][j] = 'O'
                        score = self.minimax(board, depth + 1, False)
                        board[i][j] = ' '
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == ' ':
                        board[i][j] = 'X'
                        score = self.minimax(board, depth + 1, True)
                        board[i][j] = ' '
                        best_score = min(score, best_score)
            return best_score

    def check_win(self, player):
        # Check rows, columns, and diagonals
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)) or \
               all(self.board[j][i] == player for j in range(3)):
                return True
        if (self.board[0][0] == player and self.board[1][1] == player and self.board[2][2] == player) or \
           (self.board[0][2] == player and self.board[1][1] == player and self.board[2][0] == player):
            return True
        return False

    def check_draw(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    return False
        return True
    
    def update_score_label(self):
        # Update the score label with the current scores
        self.score_label.config(text=f"Human(X): {self.x_score}  AI(O): {self.o_score}", font=("Sans serif", 20),fg="blue")


    def reset_board(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=" ", state="normal")
                self.board[i][j] = ' '
        self.current_player = 'X'  # Human starts again.

root = tk.Tk()
game = TicTacToe(root)
root.mainloop()