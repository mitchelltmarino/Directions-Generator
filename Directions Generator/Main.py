'''
Name: Mitchell Marino
Date: 2018-02-20
Program: Main.py
Description: The main program for the Directions Generator.
'''

#Imports
import tkinter as tk
import Frame_GUI as Frame

#Class for application GUI.
class Application_GUI(tk.Tk):
    '''
    Application GUI is the main window for the application.
    Frames are layered and brought forward depending on which interface the
    user intends to use.
    '''

    def __init__(self):
        '''Constructor for Applicaiton GUI; The main window for the application.'''
        tk.Tk.__init__(self)
        self.title("Mitchell Marino's Directions Generator")
        #Setting up menu.
        self.menubar = tk.Menu(self)
        self.menubar.add_command(label="Directions Browser", command=self.launch_directions_frame)
        self.menubar.add_command(label="Help", command=self.launch_help_frame)
        self.config(menu=self.menubar, bg="#194570")
        #Establishing minimum size for the application window.
        self.minsize(1200,650)
        #Create the main frame.
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(expand=True, fill="both")
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        #Custom frames to be put into main frame depending on interface selected.
        self.frames = {}
        #Movie Browser Frame.
        self.frames["Directions"] = Frame.Interface_Frame(self.main_frame, "Directions")
        self.frames["Directions"].grid(row=0, column=0, sticky="nsew")
        #Help Frame.
        self.frames["Help"] = Frame.Interface_Frame(self.main_frame, "Help")
        self.frames["Help"].grid(row=0, column=0, sticky="nsew")
        #Launch movie frame as the initial top level frame.
        self.launch_directions_frame()

    def launch_directions_frame(self):
        '''Brings direction frame to the top.'''
        frame = self.frames["Directions"]
        frame.tkraise()
    
    def launch_help_frame(self):
        '''Brings help frame to the top.'''
        frame = self.frames["Help"]
        frame.tkraise()

#Launch and start application.
window = Application_GUI()
window.mainloop()