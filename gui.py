#!/bin/python3

import tkinter as tk
from tkinter import messagebox
from game_engine import Board, ChosenField, InvalidSize, victory_for, check_move



class GraphicalBoard(Board, tk.Canvas):
    """ kwargs: size"""
    def __init__(self, root, *args, **kwargs):
        if kwargs['mode'] == 'NEW':
            self.size = kwargs['size']
            self.grid_length = 100
            try :
                tk.Canvas.__init__(self,root, height=self.size*self.grid_length, width=self.size*self.grid_length)
                Board.__init__(self,size = self.size)
            except InvalidSize:
                raise InvalidSize
            self.turn = kwargs['turn']
            self.moves = 0
            self.draw_board()
            self.bind('<Button-1>',self.draw_moves)


    def draw_board(self, mode='NEW'):
        x = 0
        y = self.grid_length
        for i in range(self.size - 1):      # Drawing horizontal lines
            self.create_line(x,y, x + self.size*self.grid_length, y, width=4)
            y += self.grid_length

        x = self.grid_length
        y = 0
        for i in range(self.size -1):
            self.create_line(x, y, x, y + self.size*self.grid_length, width=4)
            x += self.grid_length

    def initialize_board(self):
        self.fields_coords = dict()  # this dictionary will associate field numbers with the upper-left and bottom-right coordinates of the field
        self.fields = dict()
        f = 1   # field number
        x = 0
        y = 0
        for j in range(self.size):
            row = list()
            for i in range(self.size):
                row.append(f)
                coords = (x, y, x+self.grid_length, y+self.grid_length)
                self.fields_coords[f] = coords
                self.fields[f] = (j,i)
                x += self.grid_length
                f += 1
            self.rows.append(row) # rows has been inherited from Board
            x = 0
            y += self.grid_length

    def draw_moves(self,event):
        x = event.x
        y = event.y
        field_number = None
        for i in range(1, self.size**2 + 1):  #this range include the field numbers in self.fields dictionary.
            x1, y1, x2, y2 = self.fields_coords[i]
            if (x1 <= x <= x2) and (y1 <= y <= y2): # Check if the mouse was in the range of any of the fields
                field_number = i
                break
        if field_number != None:
            try:
                if self.moves == self.size**2:
                    messagebox.showinfo('','Nobody won')
                    self.unbind('<Button-1>')
                    return
                self.enter_move(field_number, self.turn) # inhereted from board
                if self.turn: # O turn
                    self.draw_O(field_number)
                    if victory_for(self,True):
                        messagebox.showinfo('','O won')
                        self.unbind('<Button-1>')
                        return
                    self.turn = not self.turn
                    self.moves += 1
                else:  # X turn
                    self.draw_X(field_number)
                    if victory_for(self,False):
                        messagebox.showinfo('','X won')
                        self.unbind('<Button-1>')
                        return
                    self.turn = not self.turn
                    self.moves += 1


            except ChosenField:
                pass

    def draw_X(self, field_number):
        x1, y1, x2, y2 = self.fields_coords[field_number]
        self.create_line(x1,y1,x2,y2, fill='red', width=4)
        self.create_line(x2,y1,x1,y2, fill='red', width=4)

    def draw_O(self, field_number):
        x1, y1, x2, y2 = self.fields_coords[field_number]
        self.create_oval(x1,y1,x2,y2, outline='green', width=4)



class Game(tk.Tk):
    def __init__(self):
        super().__init__()
        self.resizable(False,False)
        self.title('Tic-Tac-Toe')
        self.tk.call('wm','iconphoto', self._w, tk.PhotoImage(file="806131.png"))
        self.saved_games = list()

        self.frame = tk.Frame(self)
        self.start = tk.Button(self.frame,text='start new game', width=40, height = 2, command=self.new_game)
        self.cont = tk.Button(self.frame, text='continue', width=40, height=2, command=self.resume_game, state=tk.DISABLED)
        self.exit = tk.Button(self.frame, text='quit', width=40, height=2, command=self.quit)

        self.turn = tk.IntVar()
        self.turn.set(1)
        self.x_turn = tk.Radiobutton(self.frame, text='x turn', variable=self.turn, value=0)
        self.o_turn = tk.Radiobutton(self.frame, text='o turn', variable=self.turn, value=1)

        self.var = tk.StringVar()
        self.entry = tk.Entry(self.frame, textvariable=self.var, width=10)

        self.label = tk.Label(self.frame, text='size: ')

        self.start.grid(row=1, column=2)
        self.cont.grid(row=2, column=2)
        self.exit.grid(row=3, column=2)

        self.x_turn.grid(row=1, column=3)
        self.o_turn.grid(row=2, column=3)

        self.label.grid(row=1, column=0)
        self.entry.grid(row=1,column=1)
        self.frame.pack()
        self.mainloop()

    def new_game(self):
        try:
            self.size = self.var.get()
            self.board = GraphicalBoard(self, size=int(self.size), mode='NEW', turn=bool(self.turn.get()))
        except Exception as e:
             print(e)
             self.entry.delete(0,last=tk.END)
             messagebox.showerror('','Invalid size')
             return

        self.frame.pack_forget()
        self.create_menu1()
        self.board.pack()

    def create_menu1(self):
        self.main_menu = tk.Menu(self, tearoff=0)
        self.config(menu=self.main_menu)
        self.main_menu.add_command(label='main menu' ,command=self.sure1, hidemargin=True)
        self.main_menu.add_command(label='pause', command=self.pause, hidemargin=True)
        self.main_menu.add_command(label='save and exit', command=self.save_and_exit)

    def create_menu2(self):
        self.main_menu2 = tk.Menu(self, tearoff=0) # used while not in a game
        self.config(menu=self.main_menu2)
        self.main_menu2.add_command(label='main menu', command=self.sure2)


    def sure1(self): # used while in a game
        ans = messagebox.askyesno('','Do you want to save the game first?')
        if ans:
            self.save_and_exit()
        else:
            self.board.destroy()
            self.frame.pack()

    def sure2(self):  # used otherwise
        self.frame2.pack_forget()
        self.frame.pack()
        self.main_menu2.destroy()

    def pause(self):
        messagebox.showinfo('','Continue?')


    def save_and_exit(self):
        if self.board not in self.saved_games:
            self.saved_games.append(self.board)
        self.main_menu.destroy()
        self.board.pack_forget()
        if len(self.saved_games) != 0:
            self.cont.config(state=tk.NORMAL)
        self.frame.pack()

    def resume_game(self):
        self.create_menu2()
        self.frame.pack_forget()
        self.frame2 = tk.Frame(self)   # this frame contains all widgets that allow the user to choose from the saved games
        self.label2 = tk.Label(self.frame2, text='choose a saved game')
        self.label2.grid(row = 0, column=0)
        for i in range(len(self.saved_games)):
            button = tk.Button(self.frame2, text='game # {0}'.format(i), command=lambda: self._retrieve_game(i))
            button.grid(row=i, column=1)
        self.frame2.pack()

    def _retrieve_game(self, index):
        self.frame2.pack_forget()
        self.create_menu1()
        self.saved_games[index].pack()

    def quit(self):
        ans = messagebox.askyesno('','Are you sure you want to quit the game?')
        if ans:
            self.destroy()
        else:
            pass


Game()
