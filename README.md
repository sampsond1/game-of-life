# Conway's Game of Life
This is a project I did for my Data Structures class my sophomore year of college. The assignment was to spend 8 hours coding a project of our choice, and I chose to implement Conway's Game of Life in the terminal. I designed my own `TorusGrid` and `GameGrid` data structures to store the grid and used the Blessed python library for terminal manipulation.

## Features
- Conway's Game of Life: an oldie but goodie
- A seemingly infinite wraparound grid
- Four premade starting states, and will read custom ones from .txt

## Skills Used
- Object Oriented Programming
- Data Structures
- Read/Write Files
- Blessed Python Library
- Git and GitHub

## Instructions
Run main.py with the first argument being a text file with a starting state:
`python3 main.py starting-state.txt`
The starting state is a text file with the first line being two integers, rows and columns, and the rest being a grid of 0s and 1s, where 1s will start alive.

To control game while active:
- z: Slow down
- x: Speed up
- Arrow keys: Move focus
- q: Quit

## Credits
[Blessed Python Library](https://blessed.readthedocs.io/)\
ASCII art by [Patorjk](patorjk.com/software/taag)