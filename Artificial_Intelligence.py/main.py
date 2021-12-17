from tkinter import Tk
from Gui import Gui
from Maze import Maze
from Frontier import Frontier


def Main():
    speed = int(1000 * 0.05)
    size = 15
    root = Tk()
    gui = Gui(root=root, size=size)
    maze = Maze(size)
    maze.isInitialized = False
    root.after(speed, lambda: searching(gui, root, maze, speed))
    root.after(speed, lambda: printMazeSolution(gui, root, speed))
    root.bind("<Key>", lambda event: restart(event, gui, maze))
    root.mainloop()


def printMazeSolution(gui, root, speed):
    root.after(speed, lambda: printMazeSolution(gui, root, speed))
    color = ""
    if gui.state == "searching":
        color = "yellow"
    elif gui.state == "done":
        color = "#999AED"
    if not type(gui.solution) == type(""):
        for case in gui.explored:
            gui.w.create_rectangle(gui.x_marge + (case[0] - 1) * gui.square_side,
                                   gui.y_marge + (case[1] - 1) * gui.square_side,
                                   gui.x_marge + case[0] * gui.square_side,
                                   gui.y_marge + case[1] * gui.square_side,
                                   fill=color)
    if gui.state == "done":
        for case in gui.solution:
            gui.w.create_rectangle(gui.x_marge + (case[0] - 1) * gui.square_side,
                                   gui.y_marge + (case[1] - 1) * gui.square_side,
                                   gui.x_marge + case[0] * gui.square_side,
                                   gui.y_marge + case[1] * gui.square_side,
                                   fill="blue")


def searching(gui, root, maze, speed):
    root.after(speed, lambda: searching(gui, root, maze, speed))
    if gui.state == "searching":
        if not maze.isInitialized:
            frontier = Frontier()
            maze.init(gui.initial_pos, gui.goal_pos, gui.walls_pos, frontier)
            maze.isInitialized = True
        parameters = maze.solve()
        gui.state = parameters[0]
        gui.explored = parameters[1]
        gui.solution = parameters[2]


def restart(event, gui, maze):
    if event.char == "r":
        gui.restart()
        maze.restart()


if __name__ == '__main__':
    Main()
