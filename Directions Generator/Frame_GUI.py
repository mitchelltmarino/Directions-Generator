'''
Name: Mitchell Marino
Date: 2018-02-20
Program: Frame_GUI.py
Description: Builds all the interfaces for the Directions generator application.
             Provides functionality allowing the user to search for the shortest path
             between two points. It also has a very detailed help screen and description
             about myself! :D
'''

#Imports
import threading
import tkinter as tk
from tkinter.font import Font
import Image_Processing as Image
import Functionality as pathfinder

class Interface_Frame(tk.Frame):

    def __init__(self, container, frame_type):
        '''Construct the frame, establish global variables.'''
        #Call constructor of inherited class.
        tk.Frame.__init__(self, master=container,padx=10,pady=10,relief="groove", bg="#194570")
        #Adjust type of frame so the Interface_Frame knows what type of Frame it is.
        self.frame_type = frame_type
        #Last searchest to prevent user from searching same thing repetitively.
        self.last_start = ""
        self.last_dest = ""
        #Fonts to be used for the Frame's widgets.
        self.main_bold_font = Font(family="Helvetica",size=25,weight="bold")
        self.alt_bold_font = Font(family="Helvetica",size=15,weight="bold")
        self.alt_norm_font = Font(family="Helvetica",size=15,weight="normal")
        #Split Main Frame into two Subframes; Left side and Right side.
        #Left Side
        if self.frame_type != "Help":
            #Note: Help frame does not require a left frame; will only use the right frame.
            left_side = tk.Frame(self,padx=5,pady=5,relief="groove", bg="#194570")  
            left_side.pack(anchor="nw", expand=False, fill="y",side="left")   
            left_side.grid_columnconfigure(0, weight=1)
        #Right Side
        right_side = tk.Frame(self,padx=5,pady=5,relief="groove", bg="#194570")
        right_side.pack(anchor="nw", expand=True, fill="both",side="right")
        right_side.grid_columnconfigure(0, weight=1)
        #Determine how to build the frame depending whether it is a help frame or not.
        if self.frame_type != "Help":
            #Help frame does not have a left frame.
            self.build_left(left_side) #Build left frame.
        self.build_right(right_side)   #Build right frame.

    def build_left(self, left_side):
        '''Build left side of frames'''
        left_side.grid_rowconfigure(7, weight=1)
        #search_label.
        search_label = tk.Label(left_side, text=self.frame_type+" Generator", font=self.main_bold_font, bg="#194570", fg="white")
        search_label.grid(row=0, column=0, rowspan=1, columnspan=2, sticky="nwse")
        #start_address_label.
        start_address_label = tk.Label(left_side, text="Start Address", font=self.alt_norm_font, bg="#194570", fg="white", pady=10)
        start_address_label.grid(row=1, column=0, rowspan=1, columnspan=2, sticky="nwse")
        #start_address_frame and start_address_field.
        start_address_frame = tk.Frame(left_side, padx=5, pady=5, relief="ridge", bg="#194570")
        start_address_frame.grid(row=2, column=0, rowspan=1, columnspan=2, sticky="nwse")
        start_address_frame.grid_columnconfigure(0, weight=1)
        start_address_frame.grid_rowconfigure(0, weight=1)
        self.start_address_field = tk.Entry(start_address_frame, font=self.alt_norm_font, relief="ridge")
        self.start_address_field.grid_configure(row=0, column=0, rowspan=1, columnspan=1, sticky="nwse")
        #dest_address_label.
        dest_address_label = tk.Label(left_side, text="Destination Address", font=self.alt_norm_font, bg="#194570", fg="white", pady=10)
        dest_address_label.grid(row=3, column=0, rowspan=1, columnspan=2, sticky="nwse")
        #dest_address_frame and dest_address_field.
        dest_address_frame = tk.Frame(left_side, padx=5, pady=5, relief="ridge", bg="#194570")
        dest_address_frame.grid(row=4, column=0, rowspan=1, columnspan=2, sticky="nwse")
        dest_address_frame.grid_columnconfigure(0, weight=1)
        dest_address_frame.grid_rowconfigure(0, weight=1)
        self.dest_address_field = tk.Entry(dest_address_frame, font=self.alt_norm_font, relief="ridge")
        self.dest_address_field.grid(row=0, column=0, rowspan=1, columnspan=2, sticky="nwse")
        #search_button.
        self.search_button = tk.Button(left_side, text="Get Directions", font=self.alt_bold_font, command=self.search_pressed)
        self.search_button.grid(row=5, column=0, rowspan=1, columnspan=2, sticky="nwse", pady=(5,0))
        #pad_label. (Padding between button and log textfield.)
        pad_label = tk.Label(left_side, text="", font=self.alt_norm_font, bg="#194570", fg="white")
        pad_label.grid(row=6, column=0, rowspan=1, columnspan=2, sticky="nwse")
        #log_textfield.
        result_lb_frame = tk.Frame(left_side, padx=5, pady=5, relief="ridge", bg="#194570")
        self.log_textfield = tk.Text(result_lb_frame, font=self.alt_norm_font, height=1, width=1, wrap=tk.WORD)
        self.log_textfield.grid(row=0, column=0, rowspan=1, columnspan=1, sticky="nswe")
        #Text for the log on the left side.
        logtext = ("To get started, enter an address into the start address field and an address into the destination address field, then press "
                    '''the "Get Directions" button!'''
                    "\n\nBe descriptive with addresses!"
                    "\nFor example:\n15 streetname, Toronto, Ontario"
                    "\n\nThat way, the application has a better chance of"
                    "correctly understanding the input you are giving it, and "
                    "it also successfully prevents misinterpretations."
                    "\n\nPlease also note that Open Street Map (OSM) is a free, open source database that anyone can use and thus it can be quite slow at times!"
                    "Bear with it and have some patience!"
                    "\n\nThank you for trying out my program, I hope you enjoy it!\n -Mitchell Marino")
        self.log_textfield.insert("end", logtext)
        result_lb_frame.grid(row=7, column=0, rowspan=1, columnspan=2, sticky="nwse")
        result_lb_frame.grid_rowconfigure(0, weight=1)
        result_lb_frame.grid_columnconfigure(0, weight=1)
        #start_address_scrollbar.
        start_address_scrollbar = tk.Scrollbar(start_address_frame, orient="horizontal")
        start_address_scrollbar.grid(row=1, column=0, rowspan=1, columnspan=1, sticky="nswe")
        self.start_address_field.configure(xscrollcommand=start_address_scrollbar.set)
        start_address_scrollbar.configure(command=self.start_address_field.xview)
        #dest_address_scrollbar.
        dest_address_scrollbar = tk.Scrollbar(dest_address_frame, orient="horizontal")
        dest_address_scrollbar.grid(row=1, column=0, rowspan=1, columnspan=1, sticky="nswe")
        self.dest_address_field.configure(xscrollcommand=dest_address_scrollbar.set)
        dest_address_scrollbar.configure(command=self.dest_address_field.xview)
        #log_y_scrollbar.
        log_y_scrollbar = tk.Scrollbar(result_lb_frame)
        log_y_scrollbar.grid(row=0, column=1, rowspan=2, columnspan=1, sticky="nswe")
        self.log_textfield.configure(yscrollcommand=log_y_scrollbar.set)
        log_y_scrollbar.configure(command=self.log_textfield.yview)

    def build_right(self, right_side):
        '''Build right side of frames.'''
        right_side.grid_rowconfigure(1, weight=1)
        #top_description_field frame.
        top_df_frame = tk.Frame(right_side, padx=0, pady=0, relief="groove", bg="#194570") 
        top_df_frame.grid(row=0, column=0, rowspan=2, columnspan=1, sticky="nwse")
        top_df_frame.grid_columnconfigure(0, weight=1)
        top_df_frame.grid_rowconfigure(0, weight=1)
        #top_description_field.
        self.top_description_field = tk.Text(top_df_frame, font=self.alt_norm_font, width=10, height=1, relief="groove", wrap=tk.WORD)
        self.top_description_field.grid(row=0, column=0, rowspan=1, columnspan=1, sticky="nwse")
        #top_y_scrollbar.
        top_y_scrollbar = tk.Scrollbar(top_df_frame)
        top_y_scrollbar.grid(row=0, column=1, rowspan=1, columnspan=1, sticky="nswe")
        self.top_description_field.configure(yscrollcommand=top_y_scrollbar.set)
        top_y_scrollbar.configure(command=self.top_description_field.yview)
        #btm and top fonts.
        self.top_description_field.tag_configure("subtitle", font=("Verdana", 15, "bold"))
        #Set up image if it is help.
        if self.frame_type == "Help":
            #bottom_description_field frame.
            btm_df_frame = tk.Frame(right_side, padx=0, pady=0, relief="groove", bg="#194570") 
            btm_df_frame.grid(row=1, column=0, rowspan=1, columnspan=2, sticky="nwse")
            btm_df_frame.grid_columnconfigure(0, weight=1)
            btm_df_frame.grid_rowconfigure(0, weight=1)
            #btm_description_field.
            self.btm_description_field = tk.Text(btm_df_frame, font=self.alt_norm_font, width=1, height=1, relief="groove", wrap=tk.WORD)
            self.btm_description_field.grid(row=0, column=0, rowspan=1, columnspan=1, sticky="nwse")
            self.btm_description_field.grid_columnconfigure(0, weight=1)
            self.btm_description_field.grid_rowconfigure(0, weight=1)
            #btm_y_scrollbar
            btm_y_scrollbar = tk.Scrollbar(btm_df_frame)
            btm_y_scrollbar.grid(row=0, column=1, rowspan=1, columnspan=1, sticky="nswe")
            self.btm_description_field.configure(yscrollcommand=btm_y_scrollbar.set)
            btm_y_scrollbar.configure(command=self.btm_description_field.yview)
            self.btm_description_field.tag_configure("maintitle", font=("Verdana", 20, "bold"))
            self.btm_description_field.tag_configure("subtitle", font=("Verdana", 16, "bold"))
            self.help_update()
            self.btm_description_field.config(state="disabled")
            #displayed_image.
            self.displayed_image = tk.Canvas(right_side, relief="groove", width=400, height=400, bg="white")
            self.displayed_image.grid(row=0, column=1, rowspan=1, columnspan=1, sticky="nwse")
            #display profile image.
            self.img = Image.generate_profile_image()
            self.displayed_image.create_image(0, 0, image=self.img, anchor="nw")
        #Disable description texts.
        self.top_description_field.config(state="disabled")
    
    def help_update(self):
        '''
        Update the help frame.
        '''  
        #Posting to text.
        #name
        self.top_description_field.insert("end", "About The Author:\n", "subtitle")
        self.top_description_field.insert("end", "Mitchell Timothy Marino", "maintitle")
        #date_of_birth
        self.top_description_field.insert("end", "\n\n")
        self.top_description_field.insert("end", "About Mitchell\n", "subtitle")
        about_mitchell = ("Mitchell has had a deep interest in technology ever since he was young."
                    " He aspires to some day lead a meaningful career in the field of technology and"
                    " develop himself as a person along the way.")
        self.top_description_field.insert("end", about_mitchell)
        #date of birth
        self.top_description_field.insert("end", "\n\n")
        self.top_description_field.insert("end", "Date of Birth\n", "subtitle")
        self.top_description_field.insert("end", "February 28th, 1997")
        #home town
        self.top_description_field.insert("end", "\n\n")
        self.top_description_field.insert("end", "Home Town\n", "subtitle")
        self.top_description_field.insert("end", "Markham, Ontario")
        #school
        self.top_description_field.insert("end", "\n\n")
        self.top_description_field.insert("end", "School\n", "subtitle")
        self.top_description_field.insert("end", "Wilfrid Laurier University")
        #program
        self.top_description_field.insert("end", "\n\n")
        self.top_description_field.insert("end", "Program\n", "subtitle")
        self.top_description_field.insert("end", "Honours Computer Science, BSc")
        #how to use
        self.btm_description_field.insert("end", "How To Use The Program\n", "subtitle")
        #String which describes how to use the program!
        how_to_use = ("On the text field under the search bars on the directions pane, there is generic"
                      " instructions on how to use the program. Here are some more detailed ones!:\n\n"
                      "In order to search for shortest path directions, type the start address in the"
                      " start address search field, and type the destination address in the destination"
                      ''' address search field. Then, to start your search press the "Get Directions" button!\n\n'''
                      "Make sure that you are descriptive in your search, otherise the program may not understand"
                      " the address you are searching for correctly. There may be misinterpretation, or the address"
                      " may not be able to be found.\n\n"
                      "For example:\n"
                      '''"15 streetname road, Toronto, Ontario" is a solid entry for an address.\n\n''')
        #Update field with instructions.
        self.btm_description_field.insert("end", how_to_use)
        #how it works
        self.btm_description_field.insert("end", "How The Program Works\n", "subtitle")
        functionality = ("The program pulls data from the Open Street Map (OSM) database using the OSMNX API."
                         " First, A bounding box is calculated in relation to the latitude / longitude coordinates of the two addresses."
                         " Then, This data is pulled from the database using the bounding box as a parameter for which region to collect information from."
                         " Note that the bounding box calculated includes both the start and destination addresses in its area,"
                         " along with a 1km buffer radius around both endpoints.\n\n"
                         "The data that is collected from the database is then parsed and placed into my own implementation of a Graph."
                         " In this graph, vertices are intersections and edges are streets.\n\n"
                         "A depth first search is then performed on the graph, to determine if the destination address is reachable by means of driving from the starting address."
                         " If the depth first search determines that the destination address cannot be reached, then the user will be informed.\n\n"
                         "Here is an example of addresses that can not be reached by one another:\n"
                         "Address1 --> 23 Garden Rd, Parson's Pond, Newfoundland\n"
                         "Address2 --> 22 Avenue Jacques Cartier, Blanc-Sablon, Quebec\n\n"
                         "If you enter the above addresses as your locations in the program, the program will tell you that there is no path between them."
                         " The reason that these two addresses are not connected because they are separated by a body of water"
                         " (the Gulf of St. Lawrence) in Eastern Canada. They are on different masses of land.\n\n"
                         "I chose DFS as I thought it would be more efficient than a BFS implementation. This is due to the nature"
                         " of the bounding box of which the intersections are pulled from; the destination node is very likely to be"
                         " deep in the graph, since the destination and start nodes are on opposite sides of the bounding box.\n\n"
                         "If a path exists between the two addresses in the path, then Djikstra's algorithm is used to determine the"
                         " absolute shortest route between them. After this, various algorithms determine street directions, distances, and turn directions"
                         " These pieces of information are placed into dynamically generated sentences to provide instructions that are different"
                         " every time, so they do not feel artificial or repetitive in nature!")
        self.btm_description_field.insert("end", functionality)

    def display_route(self, start_address, dest_address, itinerary):
        '''
        Displays the route instructions on the GUI textfield.
        '''
        self.top_description_field.config(state="normal")
        self.top_description_field.delete(1.0, "end")
        self.top_description_field.insert("end", "Directions from\n")
        self.top_description_field.insert("end",  start_address, "subtitle")
        self.top_description_field.insert("end", "\nto\n")
        self.top_description_field.insert("end",  dest_address, "subtitle")
        for step in itinerary:
            self.top_description_field.insert("end", "\n\n"+step)
        self.top_description_field.config(state="disabled")

    def display_string(self, string):
        '''
        Displays a string on the GUI textfield.
        '''
        self.top_description_field.config(state="normal")
        self.top_description_field.delete(1.0, "end")
        self.top_description_field.insert("end", string)
        self.top_description_field.config(state="disabled")
    
    def display_err(self, err_string):
        '''
        Displays an error string on the GUI textfield.
        '''
        self.top_description_field.config(state="normal")
        self.top_description_field.delete(1.0, "end")
        self.top_description_field.insert("end", "Error:\n", "subtitle")
        self.top_description_field.insert("end", err_string)
        self.top_description_field.config(state="disabled")

    def main_process(self, start_address, dest_address):
        '''
        The main process of the entire application. 
        Runs as a threaded process and calculates the shortest path between start_address and dest_address.
        ----------------------------------------------------------------------------------------------------------
        If the calculation is unsuccessful for some reason, an error will be printed to the GUI explaining why.
        If the calculation is successful, a dynamic array of directions will be printed to the GUI.
        '''
        err1 = False    #True if start address fails to be resolved.
        err2 = False    #True if destination address fails to be resolved.
        try:
            full_start_address = pathfinder.resolve_address(start_address)  #Attempt to resolve start address.
        except AttributeError:
            err1 = True
        try:
            full_dest_address = pathfinder.resolve_address(dest_address)    #Attempt to resolve destination address.
        except AttributeError:
            err2 = True

        #Error messages based on whether addresses could be resolved or not.
        if err1 == True and err2 == True:
            self.display_err("Start address and destination address could not be resolved! Ensure spelling is correct, or be more descriptive.")
        elif err1 == True:
            self.display_err("Start address could not be resolved! Ensure spelling is correct, or be more descriptive.")
        elif err2 == True:
            self.display_err("Destination address could not be resolved! Ensure spelling is correct, or be more descriptive.")

        #
        if full_start_address == full_dest_address:
            self.display_err("Start address and destination address are the same!")

        #If no error, attempt to generate directions.
        else:
            self.display_string('''Please wait..\nFetching information from database and then calculating shortest path and directions.
                                \nPlease note that the OSM (Open Street Map) database is open source and thus can be quite slow.''')
            itinerary = pathfinder.generate_route(start_address, dest_address)
            if itinerary != "Disconnected":
                #If successful, display the route. (The start and end addresses are connected by a path)
                self.display_route(full_start_address, full_dest_address, itinerary)
            else:
                #If unsuccessful, display error. (The start and end addresses are not connected by a path)
                self.display_err("Unfortunately, according to my algorithms, there is no path that can be driven between your starting point and destination point!")
            
        #When thread is completed its operation, enable the search button once again.
        self.search_button.config(state="normal")

    def search_pressed(self):
        #Disable the search button.
        self.search_button.config(state="disabled")
        #Get start and destination addresses.
        start_address = self.start_address_field.get()
        dest_address = self.dest_address_field.get()
        #If search is not equal to the user's prior search..
        if self.last_start != start_address and self.last_dest != dest_address:
            #Run main process in a thread, passing start and destination parameters
            #Main process:
            #   - re-enables search button after directions are generated.
            #   - generates errors or a successful calculation and prints either to the screen.
            self.last_start = start_address
            self.last_dest = dest_address
            workthread = threading.Thread(target=self.main_process, args=(start_address, dest_address))
            workthread.start()
        else:
            self.search_button.config(state="normal")
        
