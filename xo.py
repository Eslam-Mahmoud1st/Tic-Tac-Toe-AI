import tkinter as tk
from tkinter import messagebox
import math
import random

class XOGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("XO Game - AI Agent")
        self.window.configure(bg='#0b0b12')
        
        self.board = [' '] * 9
        self.player = 'X'
        self.ai = 'O'
        self.buttons = []
        self.game_over = False
        
        self.difficulty = tk.StringVar(value="Hard")
        
        self.create_gui()
    
    def create_gui(self):
        # Title
        title = tk.Label(
            self.window, 
            text="🎮 XO Game with AI Agent",
            font=('Segoe UI', 18, 'bold'),
            bg='#0b0b12',
            fg='#f5c16c'
        )
        title.pack(pady=10)
        
        # Players info
        info = tk.Label(
            self.window,
            text="Player (X)  vs  AI (O)",
            font=('Segoe UI', 12),
            bg='#0b0b12',
            fg='#c7c7d1'
        )
        info.pack(pady=5)
        
        # Difficulty
        diff_frame = tk.Frame(self.window, bg='#0b0b12')
        diff_frame.pack(pady=5)
        
        tk.Label(
            diff_frame,
            text="Difficulty:",
            font=('Segoe UI', 12),
            bg='#0b0b12',
            fg='#f5c16c'
        ).pack(side=tk.LEFT, padx=5)
        
        modes = [("Easy", "Easy"), ("Medium", "Medium"), ("Hard", "Hard")]
        for text, mode in modes:
            tk.Radiobutton(
                diff_frame,
                text=text,
                variable=self.difficulty,
                value=mode,
                bg='#0b0b12',
                fg='#f5c16c',
                selectcolor='#0b0b12',
                activebackground='#0b0b12',
                activeforeground='#ffae00'
            ).pack(side=tk.LEFT, padx=6)
        
        # Board
        board_frame = tk.Frame(self.window, bg='#0b0b12')
        board_frame.pack(pady=10)
        
        for i in range(9):
            btn = tk.Button(
                board_frame,
                text='',
                font=('Segoe UI', 22, 'bold'),
                width=4,
                height=2,
                bg='#1a1a2e',
                fg='#ffffff',
                activebackground='#2a2a44',
                activeforeground='#ffffff',
                relief='flat',
                command=lambda idx=i: self.player_move(idx)
            )
            btn.grid(row=i//3, column=i%3, padx=3, pady=3)
            self.buttons.append(btn)
        
        # Reset
        reset_btn = tk.Button(
            self.window,
            text="🔄 New Game",
            font=('Segoe UI', 11, 'bold'),
            bg='#f5c16c',
            fg='#0b0b12',
            activebackground='#ffae00',
            relief='flat',
            padx=14,
            pady=6,
            command=self.reset_game
        )
        reset_btn.pack(pady=10)
    
    def check_winner(self, board, player):
        win_patterns = [
            [0,1,2],[3,4,5],[6,7,8],
            [0,3,6],[1,4,7],[2,5,8],
            [0,4,8],[2,4,6]
        ]
        return any(all(board[i] == player for i in p) for p in win_patterns)
    
    def is_board_full(self, board):
        return ' ' not in board
    
    def get_empty_cells(self, board):
        return [i for i in range(9) if board[i] == ' ']
    
    def minimax(self, board, depth, is_maximizing):
        if self.check_winner(board, self.ai):
            return 10 - depth
        if self.check_winner(board, self.player):
            return depth - 10
        if self.is_board_full(board):
            return 0
        
        if is_maximizing:
            best = -math.inf
            for cell in self.get_empty_cells(board):
                board[cell] = self.ai
                best = max(best, self.minimax(board, depth + 1, False))
                board[cell] = ' '
            return best
        else:
            best = math.inf
            for cell in self.get_empty_cells(board):
                board[cell] = self.player
                best = min(best, self.minimax(board, depth + 1, True))
                board[cell] = ' '
            return best
    
    def get_best_move(self):
        if self.difficulty.get() == "Easy":
            return random.choice(self.get_empty_cells(self.board))
        elif self.difficulty.get() == "Medium":
            for cell in self.get_empty_cells(self.board):
                self.board[cell] = self.ai
                if self.check_winner(self.board, self.ai):
                    self.board[cell] = ' '
                    return cell
                self.board[cell] = ' '
            for cell in self.get_empty_cells(self.board):
                self.board[cell] = self.player
                if self.check_winner(self.board, self.player):
                    self.board[cell] = ' '
                    return cell
                self.board[cell] = ' '
            return random.choice(self.get_empty_cells(self.board))
        else:
            best_score = -math.inf
            best_move = None
            for cell in self.get_empty_cells(self.board):
                self.board[cell] = self.ai
                score = self.minimax(self.board, 0, False)
                self.board[cell] = ' '
                if score > best_score:
                    best_score = score
                    best_move = cell
            return best_move
    
    def update_button(self, index, player):
        color = '#ff3b3b' if player == 'X' else '#00e5ff'
        self.buttons[index].config(
            text=player,
            fg=color,
            disabledforeground=color,
            state='disabled'
        )
    
    def player_move(self, index):
        if self.game_over or self.board[index] != ' ':
            return
        
        self.board[index] = self.player
        self.update_button(index, self.player)
        
        if self.check_winner(self.board, self.player):
            self.game_over = True
            messagebox.showinfo("Game Result", "🎉 You Win!")
            return
        
        if self.is_board_full(self.board):
            self.game_over = True
            messagebox.showinfo("Game Result", "⚖️ Draw!")
            return
        
        self.window.after(400, self.ai_move)
    
    def ai_move(self):
        if self.game_over:
            return
        
        move = self.get_best_move()
        self.board[move] = self.ai
        self.update_button(move, self.ai)
        
        if self.check_winner(self.board, self.ai):
            self.game_over = True
            messagebox.showinfo("Game Result", "🤖 AI Wins!")
            return
        
        if self.is_board_full(self.board):
            self.game_over = True
            messagebox.showinfo("Game Result", "⚖️ Draw!")
            return
    
    def reset_game(self):
        self.board = [' '] * 9
        self.game_over = False
        for btn in self.buttons:
            btn.config(text='', state='normal', fg='#ffffff')
    
    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    XOGame().run()
