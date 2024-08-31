import tkinter as tk
from tkinter import messagebox
import random
import time

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        
        # Initialize 9x9 grids for the entries and a boolean grid for prefilled values
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.prefilled = [[False for _ in range(9)] for _ in range(9)]
        
        # Create the Sudoku grid and buttons
        self.create_grid()
        self.create_buttons()

    def create_grid(self):
        # Create a frame to hold the Sudoku grid
        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.pack(expand=True)
        
        # Create a 9x9 grid with 3x3 sub-grids, each having a border
        for i in range(3):
            for j in range(3):
                frame = tk.Frame(self.grid_frame, highlightbackground="black", highlightcolor="black", highlightthickness=2)
                frame.grid(row=i*3, column=j*3, rowspan=3, columnspan=3, padx=1, pady=1, sticky='nsew')
                
                # Create individual entry widgets for each cell in the grid
                for k in range(3):
                    for l in range(3):
                        entry = tk.Entry(frame, width=3, font=('Arial', 18), justify='center', highlightthickness=0)
                        entry.grid(row=k, column=l, padx=1, pady=1)
                        self.entries[i*3 + k][j*3 + l] = entry
        
        # Configure the grid to expand properly within the frame
        for i in range(9):
            self.grid_frame.rowconfigure(i, weight=1)
            self.grid_frame.columnconfigure(i, weight=1)

    def create_buttons(self):
        # Create a frame to hold the buttons at the bottom of the window
        button_frame = tk.Frame(self.root)
        button_frame.pack(fill='x')

        # Create and place buttons for different functionalities
        new_board_button = tk.Button(button_frame, text="New Board", command=self.new_board)
        new_board_button.pack(side='left', expand=True, fill='x')
        
        solve_button = tk.Button(button_frame, text="Solve", command=self.solve)
        solve_button.pack(side='left', expand=True, fill='x')

        submit_button = tk.Button(button_frame, text="Submit", command=self.submit)
        submit_button.pack(side='left', expand=True, fill='x')
        
        reset_button = tk.Button(button_frame, text="Reset", command=self.reset)
        reset_button.pack(side='left', expand=True, fill='x')

    def get_grid(self):
        # Retrieve the current state of the Sudoku grid from the entries
        grid = []
        for i in range(9):
            row = []
            for j in range(9):
                val = self.entries[i][j].get()
                if val == '':
                    row.append(0)  # Empty cells are represented by 0
                else:
                    row.append(int(val))  # Convert entry text to integer
            grid.append(row)
        return grid

    def set_grid(self, grid):
        # Set the Sudoku grid values into the entries and apply background colors
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)
                if grid[i][j] != 0:
                    self.entries[i][j].insert(0, grid[i][j])
                    if self.prefilled[i][j]:
                        self.entries[i][j].config(bg="lightblue")  # Prefilled cells
                    else:
                        self.entries[i][j].config(bg="lightgreen")  # Solved cells
                else:
                    self.entries[i][j].config(bg="white")  # Empty cells

    def update_entry(self, row, col, value, is_backtracking=False):
        # Update a specific entry in the grid and visualize backtracking
        self.entries[row][col].delete(0, tk.END)
        if value != 0:
            self.entries[row][col].insert(0, value)
            if is_backtracking:
                self.entries[row][col].config(bg="lightgreen")
        else:
            if not self.prefilled[row][col]:
                self.entries[row][col].config(bg="white")
        self.root.update_idletasks()
        if is_backtracking:
            time.sleep(0.05)  # Delay to visualize the backtracking process

    def solve(self):
        # Get the current grid and attempt to solve it
        grid = self.get_grid()
        if self.solve_sudoku(grid):
            self.set_grid(grid)  # Update the GUI with the solved grid
        else:
            messagebox.showinfo("Sudoku Solver", "No solution exists")  # Notify if no solution

    def solve_sudoku(self, grid):
        # Recursive backtracking algorithm to solve the Sudoku
        empty = self.find_empty_location(grid)
        if not empty:
            return True  # Base case: If no empty location, puzzle is solved
        row, col = empty

        for num in range(1, 10):
            if self.is_safe(grid, row, col, num):
                grid[row][col] = num
                self.update_entry(row, col, num, is_backtracking=True)  # Visualize the step
                if self.solve_sudoku(grid):
                    return True  # Recursive call if the grid is solvable
                grid[row][col] = 0
                self.update_entry(row, col, 0, is_backtracking=True)  # Undo the step (backtrack)
        return False  # Trigger backtracking

    def find_empty_location(self, grid):
        # Find an empty location in the grid (marked with 0)
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    return (i, j)
        return None

    def is_safe(self, grid, row, col, num):
        # Check if it's safe to place a number in the given row, column, and 3x3 box
        return (self.not_in_row(grid, row, num) and
                self.not_in_col(grid, col, num) and
                self.not_in_box(grid, row - row % 3, col - col % 3, num))

    def not_in_row(self, grid, row, num):
        # Check if the number is not in the given row
        return num not in grid[row]

    def not_in_col(self, grid, col, num):
        # Check if the number is not in the given column
        return num not in [grid[row][col] for row in range(9)]

    def not_in_box(self, grid, box_start_row, box_start_col, num):
        # Check if the number is not in the 3x3 box
        for i in range(3):
            for j in range(3):
                if grid[i + box_start_row][j + box_start_col] == num:
                    return False
        return True

    def submit(self):
        # Check the current grid against Sudoku rules and provide feedback
        grid = self.get_grid()
        if self.check_solution(grid):
            messagebox.showinfo("Sudoku Solver", "Congratulations, you won!")
        else:
            messagebox.showinfo("Sudoku Solver", "There are some mistakes")

    def check_solution(self, grid):
        # Check if the filled grid is a valid solution
        for i in range(9):
            for j in range(9):
                num = grid[i][j]
                grid[i][j] = 0  # Temporarily clear the cell to check
                if not self.is_safe(grid, i, j, num):
                    return False  # Return False if any rule is violated
                grid[i][j] = num
        return True

    def reset(self):
        # Reset the grid and clear all entries
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)
                self.entries[i][j].config(bg="white")
                self.prefilled[i][j] = False

    def new_board(self):
        # Create a new Sudoku board with a given number of prefilled values
        self.reset()  # Clear the current grid
        grid = [[0 for _ in range(9)] for _ in range(9)]
        self.generate_board(grid, 20)  # Adjust the number of initial values here

    def generate_board(self, grid, initial_values):
        # Generate a random Sudoku board with a specific number of prefilled values
        count = 0
        while count < initial_values:
            row, col = random.randint(0, 8), random.randint(0, 8)
            if grid[row][col] == 0:
                num = random.randint(1, 9)
                if self.is_safe(grid, row, col, num):
                    grid[row][col] = num
                    self.prefilled[row][col] = True  # Mark as prefilled
                    count += 1
        self.set_grid(grid)  # Update the GUI with the generated board

if __name__ == "__main__":
    root = tk.Tk()
    gui = SudokuGUI(root)
    root.mainloop()
