import tkinter as tk
from tkinter import messagebox
import random

# Sudoku solver function using Backtracking
def is_valid(board, row, col, num):
    """Check if placing 'num' at board[row][col] is valid."""
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False

    start_row, start_col = (row // 3) * 3, (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False

    return True

def find_empty_cell(board):
    """Find an empty cell in the Sudoku grid."""
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return row, col
    return None

def solve_sudoku(board):
    """Solve the Sudoku using Backtracking."""
    empty_cell = find_empty_cell(board)
    if not empty_cell:
        return True  # No empty cell means solved

    row, col = empty_cell
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num

            if solve_sudoku(board):
                return True

            board[row][col] = 0  # Backtrack

    return False

# Random Sudoku Generator
def generate_full_sudoku():
    """Generate a fully solved random Sudoku board using a randomized approach."""
    board = [[0] * 9 for _ in range(9)]
    
    def fill_diagonal_boxes():
        """Fill the 3x3 diagonal boxes with random numbers to increase randomness."""
        for i in range(0, 9, 3):
            numbers = random.sample(range(1, 10), 9)  # Shuffle numbers 1-9
            k = 0
            for row in range(i, i + 3):
                for col in range(i, i + 3):
                    board[row][col] = numbers[k]
                    k += 1

    fill_diagonal_boxes()  # Start with randomized diagonal blocks
    solve_sudoku(board)  # Solve the board to get a full Sudoku

    return board

def remove_numbers(board, difficulty=40):
    """Remove numbers from a solved board to create a puzzle with unique solutions."""
    puzzle = [row[:] for row in board]  # Copy the board
    removed_positions = set()
    
    while len(removed_positions) < difficulty:
        row, col = random.randint(0, 8), random.randint(0, 8)
        if (row, col) not in removed_positions:
            puzzle[row][col] = 0
            removed_positions.add((row, col))
    
    return puzzle

# GUI Implementation using Tkinter
class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.create_grid()

    def create_grid(self):
        """Create 9x9 Sudoku Grid using Entry widgets."""
        for row in range(9):
            for col in range(9):
                entry = tk.Entry(self.root, width=3, font=('Arial', 16), justify="center", borderwidth=2)
                entry.grid(row=row, column=col, padx=2, pady=2)
                self.entries[row][col] = entry

        # Buttons for Solve, Clear, and Generate Puzzle
        solve_button = tk.Button(self.root, text="Solve", command=self.solve)
        solve_button.grid(row=9, column=2, columnspan=2, pady=10)

        clear_button = tk.Button(self.root, text="Clear", command=self.clear_grid)
        clear_button.grid(row=9, column=4, columnspan=2, pady=10)

        generate_button = tk.Button(self.root, text="Generate Puzzle", command=self.generate_puzzle)
        generate_button.grid(row=9, column=6, columnspan=3, pady=10)

    def get_board(self):
        """Retrieve the Sudoku board from user input."""
        board = []
        for row in range(9):
            board.append([])
            for col in range(9):
                value = self.entries[row][col].get()
                board[row].append(int(value) if value.isdigit() else 0)
        return board

    def fill_grid(self, board):
        """Fill the GUI grid with the Sudoku board."""
        for row in range(9):
            for col in range(9):
                self.entries[row][col].delete(0, tk.END)
                if board[row][col] != 0:
                    self.entries[row][col].insert(0, str(board[row][col]))

    def solve(self):
        """Solve the Sudoku puzzle and display the solution."""
        board = self.get_board()
        if solve_sudoku(board):
            self.fill_grid(board)
        else:
            messagebox.showerror("Error", "No solution exists!")

    def clear_grid(self):
        """Clear all entries in the grid."""
        for row in range(9):
            for col in range(9):
                self.entries[row][col].delete(0, tk.END)

    def generate_puzzle(self):
        """Generate a new Sudoku puzzle."""
        full_board = generate_full_sudoku()
        puzzle = remove_numbers(full_board, difficulty=40)  # Remove numbers to create puzzle
        self.fill_grid(puzzle)

# Run the GUI application
if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()
