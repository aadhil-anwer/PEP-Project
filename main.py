import tkinter as tk
from tkinter import simpledialog, messagebox
import time

class NQueensSolver:
    def __init__(self, N, canvas, cell_size):
        self.N = N
        self.board = [[0 for _ in range(N)] for _ in range(N)]
        self.solutions = []
        self.canvas = canvas
        self.cell_size = cell_size
        self.placement_attempts = 0
        self.start_time = 0

    def is_safe(self, row, col):
        for i in range(col):
            if self.board[row][i] == 1:
                return False
        for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
            if self.board[i][j] == 1:
                return False
        for i, j in zip(range(row, self.N), range(col, -1, -1)):
            if self.board[i][j] == 1:
                return False
        return True

    def solve(self, col=0):
        if col >= self.N:
            solution_copy = [row[:] for row in self.board]
            self.solutions.append(solution_copy)
            self.visualize_solution()
            time.sleep(1)
            return False
        for row in range(self.N):
            if self.is_safe(row, col):
                self.board[row][col] = 1
                self.placement_attempts += 1
                self.visualize_board()
                time.sleep(0.01)
                if self.solve(col + 1):
                    return True
                self.board[row][col] = 0
                self.visualize_board()
                time.sleep(0.01)
        return False

    def visualize_board(self):
        self.canvas.delete("all")
        for row in range(self.N):
            for col in range(self.N):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                color = "white" if (row + col) % 2 == 0 else "gray"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)
                if self.board[row][col] == 1:
                    self.canvas.create_text(
                        (x1 + x2) // 2,
                        (y1 + y2) // 2,
                        text="♛",
                        font=("Arial", self.cell_size // 2),
                        fill="black"
                    )
        self.canvas.update()

    def visualize_solution(self):
        self.visualize_board()
        time.sleep(1)

    def get_solutions(self):
        return self.solutions

    def get_placement_attempts(self):
        return self.placement_attempts

    def start_timer(self):
        self.start_time = time.time()

    def get_elapsed_time(self):
        return time.time() - self.start_time

class NQueensVisualizer:
    def __init__(self, N, solutions, placement_attempts, elapsed_time):
        self.N = N
        self.solutions = solutions
        self.placement_attempts = placement_attempts
        self.elapsed_time = elapsed_time
        self.solution_idx = 0

        self.root = tk.Tk()
        self.root.title(f"All N-Queens Solutions for N = {N}")
        self.canvas_size = 500
        self.cell_size = self.canvas_size // N
        self.canvas = tk.Canvas(self.root, width=self.canvas_size, height=self.canvas_size)
        self.canvas.pack()

        self.label_info = tk.Label(self.root, text=f"Total Solutions: {len(self.solutions)} | "
                                                   f"Placements Attempted: {self.placement_attempts} | "
                                                   f"Time Taken: {self.elapsed_time:.2f} seconds")
        self.label_info.pack()

        self.prev_button = tk.Button(self.root, text="Previous", command=self.show_prev_solution)
        self.prev_button.pack(side=tk.LEFT, padx=10)

        self.next_button = tk.Button(self.root, text="Next", command=self.show_next_solution)
        self.next_button.pack(side=tk.RIGHT, padx=10)

        self.draw_solution(self.solution_idx)

    def draw_solution(self, solution_idx):
        self.canvas.delete("all")
        solution = self.solutions[solution_idx]
        for row in range(self.N):
            for col in range(self.N):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                color = "white" if (row + col) % 2 == 0 else "gray"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)
                if solution[row][col] == 1:
                    self.canvas.create_text(
                        (x1 + x2) // 2,
                        (y1 + y2) // 2,
                        text="♛",
                        font=("Arial", self.cell_size // 2),
                        fill="black"
                    )

    def show_next_solution(self):
        if self.solution_idx < len(self.solutions) - 1:
            self.solution_idx += 1
            self.draw_solution(self.solution_idx)

    def show_prev_solution(self):
        if self.solution_idx > 0:
            self.solution_idx -= 1
            self.draw_solution(self.solution_idx)

    def run(self):
        self.root.mainloop()

def main():
    root = tk.Tk()
    root.withdraw()
    N = simpledialog.askinteger("Input", "Enter the value of N for N-Queens:", minvalue=4)
    
    if N is None:
        return

    solver_window = tk.Toplevel()
    solver_window.title(f"Solving N-Queens for N = {N}")
    canvas_size = 500
    cell_size = canvas_size // N
    canvas = tk.Canvas(solver_window, width=canvas_size, height=canvas_size)
    canvas.pack()

    solver = NQueensSolver(N, canvas, cell_size)
    solver.start_timer()
    solver.solve()

    solutions = solver.get_solutions()
    placement_attempts = solver.get_placement_attempts()
    elapsed_time = solver.get_elapsed_time()
    solver_window.destroy()

    if solutions:
        visualizer = NQueensVisualizer(N, solutions, placement_attempts, elapsed_time)
        visualizer.run()
    else:
        messagebox.showerror("Error", f"No solution exists for N = {N}")

if __name__ == "__main__":
    main()
