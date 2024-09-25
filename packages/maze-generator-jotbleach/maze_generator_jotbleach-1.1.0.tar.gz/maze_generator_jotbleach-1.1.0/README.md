# Maze Generator

![Maze Visualization](https://img.shields.io/badge/maze-generator-blue) ![Python](https://img.shields.io/badge/python-3.6%2B-brightgreen)

Maze Generator is a Python library for generating, visualizing, and saving maze structures. It allows you to create random mazes, visualize them using `matplotlib`, and save/load them in various formats including CSV and text files. This library is ideal for educational purposes, game development, or just for fun!

## Features

- **Maze Generation**: Generate mazes of any size with random paths using the iterative backtracking algorithm.
- **Visualization**: Visualize mazes using `matplotlib` with start and end points highlighted.
- **File Handling**: Save and load mazes in CSV or text formats.

## Installation

You can install the library via `pip`:

```bash
pip install pip install maze-generator-jotbleach==1.1.0
```

## Usage

### 1. Creating and Generating a Maze

```python
from maze_generator_jotbleach import MazeGenerator

# Create a MazeGenerator object with specified dimensions
maze = MazeGenerator(width=21, height=21, seed=42)

# Generate the maze
maze.generate_maze()

# Retrieve the maze as a grid (2D list)
maze_grid = maze.get_maze()
```

### 2. Visualizing the Maze

```python
# Visualize the generated maze
maze.visualize_maze()

# Save the visualization as an image
maze.visualize_maze(save_path='maze.png')
```

### 3. Saving and Loading the Maze

#### Save as CSV

```python
# Save the maze grid to a CSV file
maze.save_maze_as_csv('maze.csv')
```

#### Load from CSV

```python
# Load a maze grid from a CSV file
maze.load_maze_from_csv('maze.csv')
```

### 4. Customizing the Maze

You can also manually set a maze using a 2D list and visualize it.

```python
custom_maze = [
    [1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1]
]

maze.set_maze(custom_maze)
maze.visualize_maze()
```

## API Reference

### `class MazeGenerator(width=None, height=None, seed=None)`

#### Parameters:
- `width` (int, optional): The width of the maze (must be an odd number).
- `height` (int, optional): The height of the maze (must be an odd number).
- `seed` (int, optional): Seed value for the random number generator to ensure reproducibility.

#### Methods:

- `generate_maze()`: Generates a new maze.
- `set_maze(maze_array)`: Sets the maze grid from a given 2D list.
- `get_start_end_positions()`: Returns the start and end positions of the maze.
- `visualize_maze(save_path=None)`: Visualizes the maze using `matplotlib`.
- `save_maze_as_csv(file_path)`: Saves the maze grid to a CSV file.
- `load_maze_from_csv(file_path)`: Loads the maze grid from a CSV file.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss your ideas.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Matplotlib](https://matplotlib.org/) for visualization.
- [NumPy](https://numpy.org/) for efficient array handling.
