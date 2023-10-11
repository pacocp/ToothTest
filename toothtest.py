#!/usr/bin/env python3
# -*- coding:utf-8 -*-

#----------------------------------------------------------------------
# Francisco Carrillo Pérez <franciscocp@ugr.es>
# https://github.com/pacocp
#----------------------------------------------------------------------

from sys import platform as _platform
import os
import errno
from tkinter import (Tk, Label, Entry, PhotoImage, Canvas, Tcl, NW, Button, RAISED,
                     SUNKEN, BooleanVar, StringVar, Checkbutton, END, BOTTOM, Toplevel,
                     filedialog, font)
from glob import glob
import random
from utils import read_file, RGBtoHEX, error_popup
import csv

class MainWindow():

    #----------------

    def __init__(self, main, options): 


        #Initialize attributes
        self.v = options['v']
        self.matrix = []
        for i in range(0,options['number_of_samples']):
            self.matrix.append([99,99,99])

        # check if the name already exists for that observer
        existing_obs = glob(f"ObserversEvaluations/{options['description']}*")
        if len(existing_obs) > 0:
            self.f = open(f"ObserversEvaluations/{options['description']}_{len(existing_obs)+1}.csv", "w+", newline='')
        else:
            self.f = open(f"ObserversEvaluations/{options['description']}.csv", "w+", newline='')    
        self.number_of_observer = str(options['number_of_observer'])
        self.screen_witdh = main.winfo_screenwidth()
        self.screen_height = main.winfo_screenheight()

        self.path = options['path']
        self.file = options['file']

        self.defaultfont = font.nametofont('TkDefaultFont')
        self.defaultfont.configure(family='Arial',
                                   size=10,
                                   weight=font.BOLD)
        # Fullscreen
        main.attributes("-fullscreen", True)

        self.shuffle = options['shuffle']
        self.number_of_samples = options['number_of_samples']
        if shuffle:
            self.list_numbers = list(range(0, self.number_of_samples))
            random.seed(50)
            random.shuffle(self.list_numbers)
        
        # This is going to be used to show the images that have been showed
        self.vector_of_shown_images = []
        for i in range(0,self.number_of_samples):
            self.vector_of_shown_images.append(0)
        
        if path != '':
            self.bool_img = True
            self.bool_colors = False
        elif file_name != '':
            self.bool_img = False
            self.bool_colors = True
        
        self.my_image_number = 0
        self.canvas = Canvas(main, width=self.screen_witdh, height=self.screen_height)
        self.canvas.grid(row=self.screen_height, column=self.screen_witdh)
        self.canvas.pack()
        if self.bool_img:
            # canvas for image
            
            self.state = False
            # images
            self.my_images = []
            images_list = sorted(glob(path+'/*.png'))
            images_list = Tcl().call('lsort', '-dict', images_list)
            
            if shuffle:
                images = [images_list[i] for i in self.list_numbers]
            else:
                images = images_list

            for img in images:
                self.my_images.append(PhotoImage(file = img))

            # set first image on canvas
            """ You can change the place of the images giving
            different values to the self.screen_witdh and self.screen_height """
            self.image_on_canvas = self.canvas.create_image((self.screen_witdh/2)-100, self.screen_height/2, anchor = NW, image = self.my_images[self.my_image_number])
        elif self.bool_colors:

            if self.shuffle:
                self.file = self.file[self.list_numbers,:]
            
            img = PhotoImage(file = r'assets/tooth1.png').subsample(2,2)
            img2 = PhotoImage(file = r'assets/tooth2.png').subsample(2,2)

            self.color_canvas = Canvas(main, width = img.width()+50, height = img.height()+50, bg=options['bg_tcolor'])
            width = img.width()+50
            height = img.height()+50
            #self.canvas.grid(row=250, column=250)
            self.color_canvas.pack()
            rgb1 = file.values[self.my_image_number, 0:3]
            rgb2 = file.values[self.my_image_number, 3:]
            hex1 = RGBtoHEX(rgb1[0], rgb1[1], rgb1[2])
            hex2 = RGBtoHEX(rgb2[0], rgb2[1], rgb2[2])

            main.img = img
            main.img2 = img2
            self.rec1 = self.color_canvas.create_rectangle(0, 0, int(height/2), int(height/2), fill=hex1, outline=hex1)
            self.rec2 = self.color_canvas.create_rectangle(int(width/2), 0, height, int(height/2), fill=hex2, outline=hex2)
            self.color_canvas.create_image(int(width/2)-50,20, anchor=NW, image=img)
            self.color_canvas.create_image(int(width/2),20, anchor=NW, image=img2)

            self.color_canvas.place(x=(self.screen_witdh/2)-100,y=self.screen_height/2)

        #self.image_on_canvas = self.canvas.create_image((self.screen_witdh/2)-100, self.screen_height/2, anchor = NW, image = self.my_images[self.my_image_number])
        self.texto = self.canvas.create_text(80,50,font=("Purisa", 16),text = "Sample 1")

         # button to close
        self.button_close = Button(main, text="Close", command=self.closeButton)
        #self.button.grid(row=0, column=0)
        self.button_close.place(x=0,y=0)

        # button to change to next image
        self.button_nextimage = Button(main, text="Next Sample", command=self.nextButton)
        """ You can change the place of the button giving
        different values to the self.screen_witdh and self.screen_height """
        #self.button.grid(row=4, column=10,columnspan=2, rowspan=2)
        self.button_nextimage.place(x=self.screen_witdh/2,y=0)

        # button to change to previous image
        self.button_previous = Button(main, text="Previous Sample", command=self.previousButton)
        #self.button.grid(row=4, column=11)
        """ You can change the place of the button giving
        different values to the self.screen_witdh and self.screen_height """
        self.button_previous.place(x=(self.screen_witdh/2)-150,y=0)


        ###################################################################
        #
        # PERCEPTIBILITY
        #
        ###################################################################

        """ You can change the place of the text giving
        different values yo the self.screen_witdh and self.screen_height """
        self.percep = self.canvas.create_text((self.screen_witdh/2)+300,60,font=("Purisa", 16),text = "Perceptibility")


        # button to say yes
        self.button_yes_p = Button(main, text="YES", command=self.yesButton_P)
        #self.button.grid(row=1, column=10,columnspan=2, rowspan=2)
        """ You can change the place of the button giving
        different values yo the self.screen_witdh and self.screen_height """
        self.button_yes_p.place(x=(self.screen_witdh/2)+450,y=55)

        # button to say no
        self.button_no_p = Button(main, text="NO", command=self.noButton_P)
        #self.button.grid(row=1, column=11,columnspan=2, rowspan=2)
        """ You can change the place of the button giving
        different values yo the self.screen_witdh and self.screen_height """
        self.button_no_p.place(x=(self.screen_witdh/2)+550,y=55)

        ###################################################################
        #
        # Acceptability
        #
        ###################################################################

        """ You can change the place of the text giving
        different values yo the self.screen_witdh and self.screen_height """
        self.percep = self.canvas.create_text((self.screen_witdh/2)+300,115,font=("Purisa", 16),text = "Acceptability")


        # button to say yes
        self.button_yes_ac = Button(main, text="YES", command=self.yesButton_AC)
        #self.button.grid(row=1, column=10,columnspan=2, rowspan=2)
        """ You can change the place of the button giving
        different values yo the self.screen_witdh and self.screen_height """
        self.button_yes_ac.place(x=(self.screen_witdh/2)+450,y=100)

        # button to say no
        self.button_no_ac = Button(main, text="NO", command=self.noButton_AC)
        #self.button.grid(row=1, column=11,columnspan=2, rowspan=2)
        """ You can change the place of the button giving
        different values yo the self.screen_witdh and self.screen_height """
        self.button_no_ac.place(x=(self.screen_witdh/2)+550,y=100)

        ###################################################################
        #
        # Scale
        #
        ###################################################################
        """ You can change the place of the text giving
        different values yo the self.screen_witdh and self.screen_height """
        self.percep = self.canvas.create_text((self.screen_witdh/2)+300,170,font=("Purisa", 16),text = "Scale")

        """ You can change the place of the buttons giving
        different values yo the self.screen_witdh and self.screen_height """
        # button scale 0
        self.button_scale_0 = Button(main, text="0", command=self.scale_0)
        self.button_scale_0.place(x=(self.screen_witdh/2)+450,y=150)

        # button scale 1
        self.button_scale_1 = Button(main, text="1", command=self.scale_1)
        self.button_scale_1.place(x=(self.screen_witdh/2)+500,y=150)

        # button scale 2
        self.button_scale_2 = Button(main, text="2", command=self.scale_2)
        self.button_scale_2.place(x=(self.screen_witdh/2)+550,y=150)

        # button scale 3
        self.button_scale_3 = Button(main, text="3", command=self.scale_3)
        self.button_scale_3.place(x=(self.screen_witdh/2)+600,y=150)

        # button scale 4
        self.button_scale_4 = Button(main, text="4", command=self.scale_4)
        self.button_scale_4.place(x=(self.screen_witdh/2)+650,y=150)

        # button scale 5
        self.button_scale_5 = Button(main, text="5", command=self.scale_5)
        self.button_scale_5.place(x=(self.screen_witdh/2)+700,y=150)



    #----------------
    # BUTTONS
    #----------------
    """Implementation of the next button to change the sample image"""
    def nextButton(self):
        #This is going to be used for debugging
        if self.matrix[self.my_image_number][0] == 99:
            error_popup("Please select perceptibility", "Please select perceptibility before you can continue")
        elif self.matrix[self.my_image_number][1] == 99:
            error_popup("Please select acceptability", "Please select acceptability before you can continue")
        elif self.matrix[self.my_image_number][2] == 99:
            error_popup("Please select scale", "Please select an scale before you can continue")
        else:
            #Raise buttons
            self.button_no_p.config(relief=RAISED)
            self.button_yes_p.config(relief=RAISED)
            self.button_no_ac.config(relief=RAISED)
            self.button_yes_ac.config(relief=RAISED)
            self.button_scale_1.config(relief=RAISED)
            self.button_scale_2.config(relief=RAISED)
            self.button_scale_3.config(relief=RAISED)
            self.button_scale_4.config(relief=RAISED)
            self.button_scale_5.config(relief=RAISED)
            self.button_scale_0.config(relief=RAISED)

            self.vector_of_shown_images[self.my_image_number] = 1
            self.my_image_number = self.my_image_number + 1
            # return to first image
            if self.my_image_number == self.number_of_samples:
                self.my_image_number = 0
            if self.vector_of_shown_images[self.my_image_number] == 1:
                self.canvas.itemconfigure(self.texto, text="Sample "+str(self.my_image_number+1),fill='green')
            else:
                self.canvas.itemconfigure(self.texto,text="Sample "+str(self.my_image_number+1),fill='black')
            
            # change image
            if self.bool_img:
                self.canvas.itemconfig(self.image_on_canvas, image = self.my_images[self.my_image_number])
            elif self.bool_colors:

                rgb1 = self.file[self.my_image_number, 0:3]
                rgb2 = self.file[self.my_image_number, 3:]
                hex1 = RGBtoHEX(rgb1[0], rgb1[1], rgb1[2])
                hex2 = RGBtoHEX(rgb2[0], rgb2[1], rgb2[2])
                self.color_canvas.itemconfig(self.rec1, fill=hex1, outline=hex1)
                self.color_canvas.itemconfig(self.rec2, fill=hex2, outline=hex2)
                
    """Implementation of the previuos button to change the sample image"""
    def previousButton(self):
        #Raise buttons
        self.button_no_p.config(relief=RAISED)
        self.button_yes_p.config(relief=RAISED)
        self.button_no_ac.config(relief=RAISED)
        self.button_yes_ac.config(relief=RAISED)
        self.button_scale_1.config(relief=RAISED)
        self.button_scale_2.config(relief=RAISED)
        self.button_scale_3.config(relief=RAISED)
        self.button_scale_4.config(relief=RAISED)
        self.button_scale_5.config(relief=RAISED)
        self.button_scale_0.config(relief=RAISED)
        self.vector_of_shown_images[self.my_image_number] = 1


        # next image
        #if self.my_image_number != 0:
        self.my_image_number -= 1
        
        # return to last image image
        if self.my_image_number < 0:
            self.my_image_number = self.number_of_samples

        if self.vector_of_shown_images[self.my_image_number] == 1:
            self.canvas.itemconfigure(self.texto,text="Sample "+str(self.my_image_number+1),fill='green')
        else:
            self.canvas.itemconfigure(self.texto,text='Sample '+str(self.my_image_number+1),fill='black')

        # change image
        # change image
            if self.bool_img:
                self.canvas.itemconfig(self.image_on_canvas, image = self.my_images[self.my_image_number])
            elif self.bool_colors:
                rgb1 = self.file[self.my_image_number, 0:3]
                rgb2 = self.file[self.my_image_number, 3:]
                hex1 = RGBtoHEX(rgb1[0], rgb1[1], rgb1[2])
                hex2 = RGBtoHEX(rgb2[0], rgb2[1], rgb2[2])
                self.color_canvas.itemconfig(self.rec1, fill=hex1, outline=hex1)
                self.color_canvas.itemconfig(self.rec2, fill=hex2, outline=hex2)

        # sunken the buttons previously selected
        # perceptibility
        if self.matrix[self.my_image_number][0] == 1:
            self.button_yes_p.config(relief=SUNKEN)
        elif self.matrix[self.my_image_number][0] == 0:
            self.button_no_p.config(relief=SUNKEN)
        
        # acceptability
        if self.matrix[self.my_image_number][1] == 1:
            self.button_yes_ac.config(relief=SUNKEN)
        elif self.matrix[self.my_image_number][1] == 0:
            self.button_no_ac.config(relief=SUNKEN)
        
        # scale
        if self.matrix[self.my_image_number][2] == 0:
            self.button_scale_0.config(relief=SUNKEN)
        elif self.matrix[self.my_image_number][2] == 1:
            self.button_scale_1.config(relief=SUNKEN)
        elif self.matrix[self.my_image_number][2] == 2:
            self.button_scale_2.config(relief=SUNKEN)
        elif self.matrix[self.my_image_number][2] == 3:
            self.button_scale_3.config(relief=SUNKEN)
        elif self.matrix[self.my_image_number][2] == 4:
            self.button_scale_4.config(relief=SUNKEN)
        elif self.matrix[self.my_image_number][2] == 5:
            self.button_scale_5.config(relief=SUNKEN)
    
     ###################################################################
     #
     # PERCEPTIBILITY
     #
     ###################################################################

    def yesButton_P(self):
        #write YES and number of the sample number
        self.matrix[self.my_image_number][0] = 1
        self.button_no_p.config(relief=RAISED)
        self.button_yes_p.config(relief=SUNKEN)
        self.button_yes_ac.config(relief=RAISED)
        self.button_scale_0.config(relief=RAISED)
        self.button_scale_0['state'] = 'disabled'

    def noButton_P(self):
        self.matrix[self.my_image_number][0] = 0
        self.matrix[self.my_image_number][1] = 1
        self.matrix[self.my_image_number][2] = 0
        self.button_scale_0['state'] = 'active'
        self.button_yes_p.config(relief=RAISED)
        self.button_no_p.config(relief=SUNKEN)
        self.button_yes_ac.config(relief=SUNKEN)
        self.button_scale_0.config(relief=SUNKEN)
        

       ###################################################################
     #
     # ACCEPTABILITY
     #
     ###################################################################

    def yesButton_AC(self):
        #write 1 in the acceptability field
        self.matrix[self.my_image_number][1] = 1
        self.button_no_ac.config(relief=RAISED)
        self.button_yes_ac.config(relief=SUNKEN)

    def noButton_AC(self):
        #write 0 in the acceptability field
        self.matrix[self.my_image_number][1] = 0
        self.button_yes_ac.config(relief=RAISED)
        self.button_no_ac.config(relief=SUNKEN)

    def closeButton(self):
        #Close button
        """Writes the results in a file"""
        # if there is a shuffle, reorder the samples for the files
        if self.shuffle:
            self.matrix = [self.matrix[i] for i in self.list_numbers]
        
        csv_writer = csv.writer(self.f)
        csv_writer.writerow(['Perceptibility', 'Acceptability', 'Scale'])

        for row in self.matrix:
            csv_writer.writerow(row)

        self.f.close()
        self.v.quit()

    def toggle_fullscreen(self, main):
        self.state = not self.state  # Just toggling the boolean
        main.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self,main):
        self.state = False
        main.attributes("-fullscreen", False)
        return "break"

    ########################################
    #
    # THIS ARE GOING TO BE THE SCALE BUTTONS
    #
    ########################################

    """Function for 0 scale button"""
    def scale_0(self):
        self.matrix[self.my_image_number][2] = 0
        self.button_scale_1.config(relief=RAISED)
        self.button_scale_2.config(relief=RAISED)
        self.button_scale_3.config(relief=RAISED)
        self.button_scale_4.config(relief=RAISED)
        self.button_scale_5.config(relief=RAISED)
        self.button_scale_0.config(relief=SUNKEN)

    """Function for 1 scale"""
    def scale_1(self):
        self.matrix[self.my_image_number][2] = 1
        self.button_scale_0.config(relief=RAISED)
        self.button_scale_2.config(relief=RAISED)
        self.button_scale_3.config(relief=RAISED)
        self.button_scale_4.config(relief=RAISED)
        self.button_scale_5.config(relief=RAISED)
        self.button_scale_1.config(relief=SUNKEN)

    """Function for 2 scale"""
    def scale_2(self):
        self.matrix[self.my_image_number][2] = 2
        self.button_scale_1.config(relief=RAISED)
        self.button_scale_0.config(relief=RAISED)
        self.button_scale_3.config(relief=RAISED)
        self.button_scale_4.config(relief=RAISED)
        self.button_scale_5.config(relief=RAISED)
        self.button_scale_2.config(relief=SUNKEN)

    """Function for 3 scale"""
    def scale_3(self):
        self.matrix[self.my_image_number][2] = 3
        self.button_scale_1.config(relief=RAISED)
        self.button_scale_2.config(relief=RAISED)
        self.button_scale_0.config(relief=RAISED)
        self.button_scale_4.config(relief=RAISED)
        self.button_scale_5.config(relief=RAISED)
        self.button_scale_3.config(relief=SUNKEN)

    """Function for 4 scale"""
    def scale_4(self):
        self.matrix[self.my_image_number][2] = 4
        self.button_scale_1.config(relief=RAISED)
        self.button_scale_2.config(relief=RAISED)
        self.button_scale_3.config(relief=RAISED)
        self.button_scale_0.config(relief=RAISED)
        self.button_scale_5.config(relief=RAISED)
        self.button_scale_4.config(relief=SUNKEN)

    """Function for 5 scale"""
    def scale_5(self):
        self.matrix[self.my_image_number][2] = 5
        self.button_scale_1.config(relief=RAISED)
        self.button_scale_2.config(relief=RAISED)
        self.button_scale_3.config(relief=RAISED)
        self.button_scale_4.config(relief=RAISED)
        self.button_scale_0.config(relief=RAISED)
        self.button_scale_5.config(relief=SUNKEN)

##############################################################3

""" This is going to be used to show the first window, where you can introduce
the description of the observer"""
class optionsSelector():
    def __init__ (self):
        self.entry = Tk()
        self.label1 = Label(self.entry, text="Patient name")
        self.E1 = Entry(self.entry, bd =5)
        self.label1.pack()
        self.E1.pack()

        # Random order of images colors
        self.shuffle = BooleanVar()
        self.shu_check = Checkbutton(self.entry, text='Random order of images/colors',variable=self.shuffle, 
                                     onvalue=True, offvalue=False)
        self.shu_check.pack()

        # Selecting the folder 
        self.folder_selected = ''
        self.label2 = Label(self.entry, text="Folder containing the images")
        self.folder_name = StringVar()
        self.folder_name.set('')
        self.text_folder = Label(self.entry, textvariable=self.folder_name)
        self.select_folder = Button(self.entry, text ="Select folder", command = self.selectFolder)
        self.label2.pack()
        self.select_folder.pack()
        self.text_folder.pack()

        # Selecting the color file
        self.file_selected = ''
        self.color_label = Label(self.entry, text='Select color file (.csv or .xlsx)')
        self.color_file = StringVar()
        self.color_file.set('')
        self.color_text = Label(self.entry, textvariable=self.color_file)
        self.select_color_file = Button(self.entry, text ="Select file", command = self.selectFile)
        self.color_label.pack()
        self.select_color_file.pack()
        self.color_text.pack()
        
        # Other stuff
        self.description = ""
        self.number_of_samples = ""
        self.submit = Button(self.entry, text ="Submit", command = self.getOptions)
        self.submit.pack(side=BOTTOM)

    def getOptions(self):
        self.description = self.E1.get()
        self.entry.quit()
    def main(self):
        self.entry.mainloop()
    def getDescription(self):
        return self.description
    def getNumberOfSamples(self):
        return int(self.number_of_samples)
    def selectFolder(self):
        self.folder_selected = filedialog.askdirectory()
        self.folder_name.set(self.folder_selected)
        self.entry.update_idletasks()
    def selectFile(self):
        self.file_selected = filedialog.askopenfilename()
        self.color_file.set(self.file_selected)
        self.entry.update_idletasks()
        # if the file has been selected you must select
        # the background color for the teeth
        self.bg_tlabel = Label(self.entry, text="RGB for teeth background (e.g. 255,255,255)")
        self.bg_tcolor_entry = Entry(self.entry, bd =5)
        self.bg_tlabel.pack()
        self.bg_tcolor_entry.insert(END, "255,255,255")
        self.bg_tcolor_entry.pack()
    def getBGTColor(self):
        return self.bg_tcolor_entry.get()
    def getFolder(self):
        return self.folder_selected
    def getFile(self):
        return self.file_selected
    def getShuffle(self):
        return self.shuffle.get()
    def quit(self):
        self.entry.destroy()


##########################################################

"""This is going to show the observers who already have made the test"""

class observers_window():
    def __init__(self,observers_names):
        self.window = Tk()
        self.label1 = Label(self.window, text="Observers Names")
        self.label1.pack()
        for name in observers_names:
        	self.label = Label(self.window, text=name)
        	self.label.pack()
    def main(self):
    	self.window.mainloop()
    def quit(self):
    	self.window.destroy()

##########################################################


""" MAIN PROGRAM """
try:
    os.makedirs("ObserversEvaluations")
except OSError as exception:
    if exception.errno != errno.EEXIST:
        raise
try:
    open("observers.txt")
except:
    open("observers.txt", "w")

with open("observers.txt") as f:
	observers_names = []
	for line in f:
		observers_names.append(line)

v = optionsSelector()
b = observers_window(observers_names)
v.main()
b.main()
path = v.getFolder()
file_name = v.getFile()
if path != '':
    number_of_samples = len(glob(path+'/*.png'))
    values = None
    bg_tcolor=None
elif file_name != '':
    file = read_file(file_name)
    number_of_samples = file.values.shape[0]
    bg_tcolor = v.getBGTColor().split(',')
    bg_tcolor = RGBtoHEX(int(bg_tcolor[0]), int(bg_tcolor[1]), int(bg_tcolor[2]))
    values = file.values
else:
    error_popup('Path or File Error', 'You must select a path with images or a valid color file (.csv or .xlsx)')

description = v.getDescription()
shuffle = v.getShuffle()
number_of_observer = 0

"""This is going to check the number of files in the Observers Evaluation folder
so it can select the number of the next observer"""
while os.path.exists("ObserversEvaluations/observer"+str(number_of_observer)+".txt"):
    number_of_observer = number_of_observer + 1
with open("observers.txt", "a") as observers:
    observers.write(description+"\n")

root = Toplevel()
options = {
    'description': description,
    'number_of_observer': number_of_observer,
    'v': v,
    'number_of_samples': number_of_samples,
    'shuffle': shuffle,
    'path': path,
    'file': values,
    'bg_tcolor': bg_tcolor
}
MainWindow(root,options)
b.quit()
root.mainloop()
