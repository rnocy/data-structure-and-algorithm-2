import matplotlib.pyplot as mpl
import numpy as np
import pandas as pd
import networkx as nx
import random

DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]  #right, down, left, and up.
def read_maze(filename): #I have to make a different function to read the maze from a CSV file so I can put data frame seting for the CSV and all the values in CSV as well. Also use this to convert it to a matrix!
    df = pd.read_csv(filename, header=None, dtype=str, encoding="utf-8-sig")#utf-8-sig is used to handle the BOM (Byte Order Mark) if present in the CSV file.
    grid = df.values.tolist()
    start = (0, 9) #identifying the start positions in the maze
    end = (20, 11) #identifying the end positions in the maze
    return start, end, grid #returns the start position, end position, and the grid as a list of lists. This matrix representation of the maze will be used for further processing in the maze direction.
def which_method(start, end, grid):
    print("Hello!")
    print("How would you like to solve the maze?")
    print("Start position: " + str(start) + ", End position: " + str(end))
    for row in grid:
        print(" ".join(row)) #for each row in the grid, join the elements with a space and print it, for better visualization of the maze in the terminal.
    print("Please press 0 to select Back Tracking method, press 1 for Las Vegas.")
    userchoice = input()
    while userchoice not in ("0", "1"):
        print("Please only select 0 or 1.")
        userchoice = input()
    return "back_tracking" if userchoice == "0" else "las_vegas"
start, end, grid = read_maze("maze.csv")
def is_open(grid, cell, visited): #this function checks if a cell is a wall or not, if isOpen, it is not a wall and not visited yet. It takes the grid, the cell coordinates, and the set of visited cells as input.
    row, col = cell #define what is a cell, which is a tuple of (row, col) coordinates. 
    return (0 <= row < len(grid) and 0 <= col < len(grid[0]) #identify the bounds of the grid, length of the grid is the number of rows, and length of the first row is the number of columns
            and grid[row][col] != "0" #since 0 is a wall, we have to set a condition to check if the cell is not a wall, if it is not a wall, we can visit it.
            and cell not in visited) #if the cell has not been visited yet, we check if it is a wall or road, if road, we can visit it.
def backtracking(grid, position, end, visited, path): #find a path from the start position to the end position. Takes the grid, current position, end position, set of visited cells, and the path taken so far as input.
    visited.add(position) #add the current position to the set of visited cells, so we don't visit it again in this path.
    path.append(position) #add the current position to the path taken so far so we can keep track of the path we have taken to reach the end position.
    if position == end: #set the end condition for the algorithm, if the current position is the end position, we have found a path and return True.
        return True
    for direction in DIRECTIONS: #set directions to move in the maze in a loop.
        new_position = (position[0] + direction[0], position[1] + direction[1]) #new position is the current position plus the direction we are moving in, which is a tuple of (row, col) coordinates.
        if is_open(grid, new_position, visited): #check if the new position is open, if it is, we can move to it and continue the search.
            if backtracking(grid, new_position, end, visited, path): #if the recursive call to backtracking returns True, we have found a path.
                return True
    path.pop()#remove the current position from the path if it doesn't lead to a solution, so we can backtrack and try other paths.
    return False #return False if no path is found from the current position to the end position.
def las_vegas(grid, start, end, max_steps=200): #this function implements the Las Vegas algorithm to find a path from the start position to the end position in the maze, also set limit as 200 steps.
    position = start
    previous = None #set the previous position to None, since we haven't moved yet.
    path = [start] #set path to a list containing the start position, so we can keep track of the path we have taken.
    for step in range(1, max_steps + 1): #loop through the steps, all the way until you hit a wall or the end position, or until you hit the maximum number of steps which is 200.
        options = [] #make a list of options
        for direction in DIRECTIONS: #reuse directions from backtracking to identify new position cell.
            new_position = (position[0] + direction[0], position[1] + direction[1])
            if (0 <= new_position[0] < len(grid) #check for wall and road, if the new position cell is out of bounds or not.
                    and 0 <= new_position[1] < len(grid[0])  #check for bounds
                    and grid[new_position[0]][new_position[1]] != "0"): #check if this is a wall or not. If it is not a wall, it could be the next position
                options.append(new_position) #add new position coordination to the list of options we can take

        forward = [cell for cell in options if cell != previous] #make a new list called "forward" to hold all of the options. 
        if len(forward) > 0: #if forward is empty or not, if empty = cannot move forward, if not empty = can move ahead.
            options = forward  #set the amount of cells that is possible as options to be the forward list as well

        previous = position #set this to identify that now "previous" cell is recorded by the coordination of your "position". After moving forward, my current position is counted into "previous"
        position = random.choice(options) #take a random path and just see how it goes from there.
        path.append(position) #add the new position to the path list, so we can keep track of the 'visited' cells.

        if position == end: #found the exit
            return path, step

    return None, max_steps # end if reach 200 steps but still no exit

#Maze drawing section
def draw_maze(grid, start, end, path=None, title="Maze"): #make a function to draw the maze using matplotlib, which takes the grid, start position, end position, path and title taken as input.
    numbers = [[0 if cell == "0" else 1 for cell in row] for row in grid] #identify the grid to a matrix of 0s and 1s, where 0 is a wall and 1 is a road, so we can use it to draw the maze.
    fig, ax = mpl.subplots(figsize=(5, 5)) # set figure size is set to 5x5 inches but you can freely change it to any size you want.
    ax.imshow(numbers, cmap="gray") #set the colormap to gray, so walls are black and roads are white.

    if path:
        rows = [cell[0] for cell in path] #get the row coordinates of the path, which is a list of the first element of each cell in the path.
        cols = [cell[1] for cell in path] # get the column coordinates of the path, which is a list of the second element of each cell in the path.
        ax.plot(cols, rows, color="red", linewidth=2) #mark the path on the maze, with red color and linewidth of 2, so we can see the path clearly.

    ax.plot(start[1], start[0], "go", markersize=10, label="Entrance (E)") #mark the start position on the maze, with green color and markersize of 10, so we can see the start position clearly.
    ax.plot(end[1], end[0], "bs", markersize=10, label="Exit (O)") #mark the end position on the maze, with blue color and markersize of 10, so we can see the end position clearly.

    ax.set_title(title) #set the title of the maze, which method is used.
    mpl.show() #show the maze with the path taken, start position, and end position, so we can see the result of the maze solving algorithm.

#this section is for UX. It will be displayed to user.
start, end, grid = read_maze("Maze.csv") #load the file name to the read_maze function.
method = which_method(start, end, grid) #determine which method the user wants to use to solve the maze, either backtracking or Las Vegas.
if method == "back_tracking":
    print("Back tracking selected")
    path = []
    if backtracking(grid, start, end, set(), path): #call the backtracking function
            print(path) #print the path found by the backtracking algorithm, which is a list of coordinates of the path taken from start to end.
            draw_maze(grid, start, end, path, title="Backtracking Path") #set title for the maze figure if user select backtracking method.
    else:
            print("No path found")
else:
    print("Las Vegas selected")
    path, steps = las_vegas(grid, start, end)
    if path:
        print("Path found in", steps, "steps:")
        print(path)
        draw_maze(grid, start, end, path, title="Las Vegas solution")
    else:
        print("No path found after", steps, "steps.")
#for row in range(len(grid)): #this loop to define start and end positions based on the grid content, where 'E' is the start and 'O' is the end.
#        for col in range(len(grid[row])):
#            if grid[row][col] == 'E':
#                start = (row, col)
#            elif grid[row][col] == 'O':
#                end = (row, col)