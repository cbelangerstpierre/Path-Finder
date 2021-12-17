from tkinter import Canvas, Label, Button, CENTER


class Gui:
    def __init__(self, root, size):
        self.root = root
        self.state = "nothing"
        self.initial_pos = []
        self.goal_pos = []
        self.walls_pos = []
        self.root.title("Artificial Intelligence")
        self.root.resizable(False, False)
        self.root.geometry("650x650")
        self.root["bg"] = "#999AED"
        self.screen_side = 650
        self.x_marge = 100
        self.y_marge = 55
        self.size = size
        self.square_side = (self.screen_side - 2 * self.x_marge) / self.size
        self.solution = []
        self.explored = []

        # Create the board
        self.w = Canvas(self.root, width=self.screen_side, height=self.screen_side)

        self.fillW()
        self.message, self.start_button, \
            self.goal_button, self.wall_button,\
            self.wall_remover_button, self.finish_button = self.TitlesAndButtons()

    def restart(self):
        self.fillW()
        self.state = "nothing"
        self.initial_pos = []
        self.goal_pos = []
        self.walls_pos = []
        self.start_button["state"] = "normal"
        self.goal_button["state"] = "normal"
        self.wall_button["state"] = "normal"
        self.finish_button["state"] = "normal"
        self.wall_remover_button["state"] = "normal"
        self.message["text"] = ""
        self.solution = []
        self.explored = []

    def cursorGridPos(self, x, y):
        for i in range(1, self.size + 1):
            for j in range(1, self.size + 1):
                if self.isBetween(x, self.x_marge + self.square_side * (i - 1), self.x_marge + self.square_side * i) \
                        and self.isBetween(y, self.y_marge + self.square_side * (j - 1),
                                           self.y_marge + self.square_side * j):
                    return [i, j]

    @staticmethod
    def isBetween(a, b, c):
        if (b <= a <= c) or (c <= a <= b):
            return True
        else:
            return False

    def clickedOnGrid(self, event):
        if self.isBetween(event.x, self.x_marge, self.x_marge + self.size * self.square_side) \
                and self.isBetween(event.y, self.y_marge, self.y_marge + self.size * self.square_side):
            pos = self.cursorGridPos(event.x, event.y)
            if self.state == "start":
                if not self.initial_pos == []:
                    self.w.create_rectangle(self.x_marge + (self.initial_pos[0] - 1) * self.square_side,
                                            self.y_marge + (self.initial_pos[1] - 1) * self.square_side,
                                            self.x_marge + self.initial_pos[0] * self.square_side,
                                            self.y_marge + self.initial_pos[1] * self.square_side,
                                            fill="#999AED")
                self.w.create_rectangle(self.x_marge + (pos[0] - 1) * self.square_side,
                                        self.y_marge + (pos[1] - 1) * self.square_side,
                                        self.x_marge + pos[0] * self.square_side,
                                        self.y_marge + pos[1] * self.square_side,
                                        fill="green")
                self.initial_pos = pos
                if pos in self.walls_pos:
                    self.walls_pos.remove(pos)
            elif self.state == "goal":
                if not self.goal_pos == []:
                    self.w.create_rectangle(self.x_marge + (self.goal_pos[0] - 1) * self.square_side,
                                            self.y_marge + (self.goal_pos[1] - 1) * self.square_side,
                                            self.x_marge + self.goal_pos[0] * self.square_side,
                                            self.y_marge + self.goal_pos[1] * self.square_side,
                                            fill="#999AED")
                    self.goal_pos = pos
                self.w.create_rectangle(self.x_marge + (pos[0] - 1) * self.square_side,
                                        self.y_marge + (pos[1] - 1) * self.square_side,
                                        self.x_marge + pos[0] * self.square_side,
                                        self.y_marge + pos[1] * self.square_side,
                                        fill="red")
                self.goal_pos = pos
                if pos in self.walls_pos:
                    self.walls_pos.remove(pos)
            elif self.state == "wall":
                if not pos == self.initial_pos and not pos == self.goal_pos:
                    pos_is_a_wall = False
                    for wall in self.walls_pos:
                        if wall[0] == pos[0] and wall[1] == pos[1]:
                            pos_is_a_wall = True
                    if not pos_is_a_wall:
                        self.w.create_rectangle(self.x_marge + (pos[0] - 1) * self.square_side,
                                                self.y_marge + (pos[1] - 1) * self.square_side,
                                                self.x_marge + pos[0] * self.square_side,
                                                self.y_marge + pos[1] * self.square_side,
                                                fill="black")
                        self.walls_pos.append([pos[0], pos[1]])

            elif self.state == "wall remover":
                for wall in self.walls_pos:
                    if wall[0] == pos[0] and wall[1] == pos[1]:
                        self.w.create_rectangle(self.x_marge + (pos[0] - 1) * self.square_side,
                                                self.y_marge + (pos[1] - 1) * self.square_side,
                                                self.x_marge + pos[0] * self.square_side,
                                                self.y_marge + pos[1] * self.square_side,
                                                fill="#999AED")
                        self.walls_pos.remove(pos)

    def stateChanger(self, new_state):
        self.message["text"] = ""
        self.state = new_state

    def noPlacement(self):
        if not self.goal_pos == [] and not self.initial_pos == []:
            self.start_button["state"] = "disabled"
            self.goal_button["state"] = "disabled"
            self.wall_button["state"] = "disabled"
            self.finish_button["state"] = "disabled"
            self.wall_remover_button["state"] = "disabled"
            self.state = "searching"
        else:
            self.message["text"] = "You need to set the start and the goal."

    def fillW(self):
        self.w.create_rectangle(0, 0, 650, 650, fill="#999AED", outline="#999AED")
        for i in range(self.size + 1):
            self.w.create_line(i * self.square_side + self.x_marge, self.y_marge, i * self.square_side + self.x_marge,
                               self.y_marge + self.size * self.square_side)
            self.w.create_line(self.x_marge, i * self.square_side + self.y_marge,
                               self.x_marge + self.size * self.square_side,
                               i * self.square_side + self.y_marge)
        self.w.bind("<B1-Motion>", self.clickedOnGrid)
        self.w.bind("<Button-1>", self.clickedOnGrid)
        self.w.pack()

    def TitlesAndButtons(self):

        # Create title and buttons
        message = Label(self.root, text="", bg="#999AED", font=('Helvetica bold', 15))
        restart_message = Label(self.root, text="'R' to restart", bg="#999AED", font=('Helvetica bold', 12))
        headline = Label(self.root, text="Path Finder", bg="#999AED", font=('Helvetica bold', 25))
        start_button = Button(self.root, text="Place the start", bg="green", fg="white", width=12,
                              command=lambda: self.stateChanger("start"))
        goal_button = Button(self.root, text="Place the goal", bg="red", fg="white", width=12,
                             command=lambda: self.stateChanger("goal"))
        wall_button = Button(self.root, text="Place walls", bg="black", fg="white", width=12,
                             command=lambda: self.stateChanger("wall"))
        wall_remover_button = Button(self.root, text="Remove walls", bg="white", fg="black", width=12,
                                     command=lambda: self.stateChanger("wall remover"))
        finish_button = Button(self.root, text="Placement finished", bg="blue", fg="white", width=30,
                               command=self.noPlacement)

        # Place title and buttons
        message.place(relx=0.5, rely=0.81, anchor=CENTER)
        restart_message.place(relx=0.1, rely=0.96, anchor=CENTER)
        headline.place(relx=0.5, rely=0.04, anchor=CENTER)
        start_button.place(relx=0.12, rely=0.87, anchor=CENTER)
        goal_button.place(relx=0.88, rely=0.87, anchor=CENTER)
        wall_button.place(relx=0.37, rely=0.87, anchor=CENTER)
        wall_remover_button.place(relx=0.62, rely=0.87, anchor=CENTER)
        finish_button.place(relx=0.5, rely=0.96, anchor=CENTER)

        return message, start_button, goal_button, wall_button, wall_remover_button, finish_button
