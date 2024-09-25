import random
import matplotlib.pyplot as plt
import numpy as np
import csv

class MazeGenerator:
    def __init__(self, width: int = None, height: int = None, seed = None):
        """
        Initializes the maze generator.

        Parameters:
        - width (int, optional): The width of the maze (must be odd).
        - height (int, optional): The height of the maze (must be odd).
        - seed (int, optional): A seed value for the random number generator.
        """
        self.maze = None
        self.width = None
        self.height = None
        self.start_pos = None
        self.end_pos = None
        self.seed = seed

        if width is not None and height is not None:
            self.width = width if width % 2 == 1 else width + 1
            self.height = height if height % 2 == 1 else height + 1
            self.maze = [[1 for i in range(self.width)] for i in range(self.height)]

    def generate_maze(self, start_pos = None, end_pos = None, add_loops = False, loop_probability = 0.1, seed = None):
        """
        Generates the maze using the iterative backtracking algorithm.

        Parameters:
        - start_pos (tuple, optional): Custom starting position for the maze.
        - end_pos (tuple, optional): Custom ending position for the maze.
        """
        if self.width is None or self.height is None:
            raise ValueError("Maze dimensions are not set.")

        # Set the seed for reproducibility
        if seed is not None:
            random.seed(seed)
        elif self.seed is not None:
            random.seed(self.seed)
        
        self.start_pos = start_pos if start_pos else (0, 1)
        self.end_pos = end_pos if end_pos else (self.height - 1, self.width - 2)

        if not self._is_valid_position(self.start_pos) or not self._is_valid_position(self.end_pos):
            raise ValueError("Start or end position is invalid or outside the maze boundaries.")

        start_x = random.randrange(1, self.width, 2)
        start_y = random.randrange(1, self.height, 2)

        self._carve_path_iterative(start_x, start_y)
        self.maze[self.start_pos[0]][self.start_pos[1]] = 0
        self.maze[self.end_pos[0]][self.end_pos[1]] = 0

        if add_loops:
            self._add_loops(loop_probability)

    def _is_valid_position(self, pos):
        """
        Checks if a position is valid within the maze and not on a wall.

        Parameters:
        - pos (tuple): Position to validate as (row, column).
        Returns:
        - bool: True if the position is valid, False otherwise.
        """
        row, col = pos
        if 0 <= row < self.height and 0 <= col < self.width:
            return self.maze[row][col] == 1
        return False

    def _carve_path_iterative(self, x, y):
        stack = []
        stack.append((x, y))
        self.maze[y][x] = 0  # Mark the starting cell as a path

        while stack:
            x, y = stack[-1]

            # Randomly order directions: up, right, down, left
            directions = [(0, -2), (2, 0), (0, 2), (-2, 0)]
            random.shuffle(directions)

            found = False
            for dx, dy in directions:
                nx, ny = x + dx, y + dy

                if 1 <= nx < self.width - 1 and 1 <= ny < self.height - 1:
                    if self.maze[ny][nx] == 1:
                        # Carve a path between the current cell and the next cell
                        self.maze[y + dy // 2][x + dx // 2] = 0
                        self.maze[ny][nx] = 0
                        # Push the neighbor cell onto the stack
                        stack.append((nx, ny))
                        found = True
                        break

            if not found:
                # Backtrack to the previous cell
                stack.pop()
                
    def _add_loops(self, loop_probability):
        """
        Adds random loops to the maze by removing walls with a certain probability.

        Parameters:
        - loop_probability (float): The probability of adding a loop in the maze.
        """
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if self.maze[y][x] == 1:
                    neighbors = self._count_adjacent_paths(x, y)
                    if neighbors >= 2 and random.random() < loop_probability:
                        self.maze[y][x] = 0

    def _count_adjacent_paths(self, x, y):
        """
        Counts the number of path cells adjacent to a given wall cell.

        Parameters:
        - x (int): The x-coordinate of the cell.
        - y (int): The y-coordinate of the cell.

        Returns:
        - int: The number of adjacent path cells.
        """
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        count = 0
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height and self.maze[ny][nx] == 0:
                count += 1
        return count

    def set_maze(self, maze_array: list[int], start_pos: tuple = None, end_pos: tuple = None):
        """
        Sets the maze grid from a given array.

        Parameters:
        - maze_array (list of lists): The maze grid to set.
        """
        
        if not maze_array:
            raise ValueError("Provided maze array is empty.")

        self.maze = maze_array
        self.height = len(maze_array)
        self.width = len(maze_array[0])
        self.start_pos = start_pos
        self.end_pos = end_pos

    def visualize_maze(self, save_path=None):
        """
        Visualizes the maze using Matplotlib.

        Parameters:
        - save_path (str, optional): The file path to save the visualization image.
        """
        if self.maze is None:
            raise ValueError("Maze grid is not set.")

        maze_array = np.array(self.maze)
        cmap = plt.cm.binary

        fig, ax = plt.subplots(figsize=(10, 10))
        ax.imshow(maze_array, cmap=cmap, interpolation='none')

        if self.start_pos:
            ax.scatter(self.start_pos[1], self.start_pos[0], c='green', s=50, label='Start')
        if self.end_pos:
            ax.scatter(self.end_pos[1], self.end_pos[0], c='red', s=50, label='End')

        ax.axis('off')

        if self.start_pos or self.end_pos:
            ax.legend(loc='upper right')

        if save_path:
            plt.savefig(save_path, bbox_inches='tight', pad_inches=0)
            print(f"Maze visualization saved to {save_path}")

        plt.show()

    def save_maze_as_csv(self, file_path):
        """
        Saves the maze grid to a CSV file.

        Parameters:
        - file_path (str): The file path to save the maze data.
        """
        if self.maze is None:
            raise ValueError("Maze grid is not set.")

        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for row in self.maze:
                writer.writerow(row)
        print(f"Maze data saved to {file_path}")

    def load_maze_from_csv(self, file_path):
        """
        Loads the maze grid from a CSV file.

        Parameters:
        - file_path (str): The file path to load the maze data from.
        """
        with open(file_path, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            maze_array = []
            for row in reader:
                maze_array.append([int(cell) for cell in row])
        self.set_maze(maze_array)
        print(f"Maze data loaded from {file_path}")
