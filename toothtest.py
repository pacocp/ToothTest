#!/usr/bin/env python3
# -*- coding:utf-8 -*-

#----------------------------------------------------------------------
# Francisco Carrillo Pérez <carrilloperezfrancisco@gmail.com>
# https://github.com/pacocp
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# You are going to be able to see the images of the different tooth and
# answer YES or NO depends on your evaluation of their similarity, and use
# an scale
#----------------------------------------------------------------------

from sys import argv
from sys import platform as _platform
import subprocess
import os
import errno
from tkinter import filedialog
from tkinter import *
from glob import glob
import random

class MainWindow():

    #----------------

    def __init__(self, main,description,number_of_observer,v,number_of_samples,shuffle,path):


        #Initialize attributes
        self.v = v
        self.matrix = []
        for i in range(0,number_of_samples):
            self.matrix.append([99,99,99])
        self.f = open("ObserversEvaluations/observer"+str(number_of_observer)+".txt",'w+')
        self.f.write(description)
        self.f.write("\n\n")
        self.f.write("\nThe order of the results is as follows: Perceptibility Acceptability Scale\n\n")
        self.number_of_observer = str(number_of_observer)
        screen_width = main.winfo_screenwidth()
        screen_height = main.winfo_screenheight()


        #Fullscreen
        main.attributes("-fullscreen", True)

        # canvas for image
        self.canvas = Canvas(main, width=screen_width, height=screen_height)
        self.canvas.grid(row=screen_height, column=screen_width)
        self.state = False
        # images
        self.shuffle = shuffle
        self.number_of_samples = number_of_samples
        self.path = path
        self.my_images = []
        images_list = sorted(glob(path+'/*.png'))
        images_list = Tcl().call('lsort', '-dict', images_list)
        
        if shuffle:
            self.list_numbers = list(range(0, number_of_samples))
            random.seed(50)
            self.list_numbers = random.sample(self.list_numbers, len(self.list_numbers))
            images = [images_list[i] for i in self.list_numbers]
            #images = images_list[self.list_numbers]
        else:
            images = images_list
        for img in images:
            self.my_images.append(PhotoImage(file = img))

        self.my_image_number = 0

        #This is going to be used to show the images that have been showed
        self.vector_of_shown_images = []
        for i in range(0,number_of_samples):
            self.vector_of_shown_images.append(0)


        # set first image on canvas
        """ You can change the place of the images giving
        different values to the screen_width and screen_height """
        #self.image_on_canvas = self.canvas.create_image((screen_width/2)-100, screen_height/2, anchor = NW, image = self.my_images[self.my_image_number])
        canvas = Canvas(root, width = 250, height = 250, bg='black')

        #canvas.pack()

        img = PhotoImage(file = r'assets/tooth1.png')
        img2 = PhotoImage(file = r'assets/tooth2.png')
        root.img = img
        root.img2 = img2
        canvas.create_rectangle(0, 0, 250/2, 250/2, fill='#fb0', outline='#fb0')
        canvas.create_rectangle(250/2,0, 250, 250/2, fill='#fc0', outline='#fc0')
        canvas.create_image((250/2)-100,40, anchor=NW, image=img)
        canvas.create_image((250/2),40, anchor=NW, image=img2)

        canvas.place(x=(screen_width/2)-100,y=screen_height/2)

        #self.image_on_canvas = self.canvas.create_image((screen_width/2)-100, screen_height/2, anchor = NW, image = self.my_images[self.my_image_number])
        self.texto = self.canvas.create_text(80,50,font=("Purisa", 16),text = "Sample 1")

         # button to close
        self.button_close = Button(main, text="Close", command=self.closeButton)
        #self.button.grid(row=0, column=0)
        self.button_close.place(x=0,y=0)

        # button to change to next image
        self.button_nextimage = Button(main, text="Next Sample", command=self.nextButton)
        """ You can change the place of the button giving
        different values to the screen_width and screen_height """
        #self.button.grid(row=4, column=10,columnspan=2, rowspan=2)
        self.button_nextimage.place(x=screen_width/2,y=0)

        # button to change to previous image
        self.button_previous = Button(main, text="Previous Sample", command=self.previousButton)
        #self.button.grid(row=4, column=11)
        """ You can change the place of the button giving
        different values to the screen_width and screen_height """
        self.button_previous.place(x=(screen_width/2)-150,y=0)


        ###################################################################
        #
        # PERCEPTIBILITY
        #
        ###################################################################

        """ You can change the place of the text giving
        different values yo the screen_width and screen_height """
        self.percep = self.canvas.create_text((screen_width/2)+300,60,font=("Purisa", 16),text = "Perceptibility")


        # button to say yes
        self.button_yes_p = Button(main, text="YES", command=self.yesButton_P)
        #self.button.grid(row=1, column=10,columnspan=2, rowspan=2)
        """ You can change the place of the button giving
        different values yo the screen_width and screen_height """
        self.button_yes_p.place(x=(screen_width/2)+450,y=55)

        # button to say no
        self.button_no_p = Button(main, text="NO", command=self.noButton_P)
        #self.button.grid(row=1, column=11,columnspan=2, rowspan=2)
        """ You can change the place of the button giving
        different values yo the screen_width and screen_height """
        self.button_no_p.place(x=(screen_width/2)+550,y=55)

        ###################################################################
        #
        # Acceptability
        #
        ###################################################################

        """ You can change the place of the text giving
        different values yo the screen_width and screen_height """
        self.percep = self.canvas.create_text((screen_width/2)+300,115,font=("Purisa", 16),text = "Acceptability")


        # button to say yes
        self.button_yes_ac = Button(main, text="YES", command=self.yesButton_AC)
        #self.button.grid(row=1, column=10,columnspan=2, rowspan=2)
        """ You can change the place of the button giving
        different values yo the screen_width and screen_height """
        self.button_yes_ac.place(x=(screen_width/2)+450,y=100)

        # button to say no
        self.button_no_ac = Button(main, text="NO", command=self.noButton_AC)
        #self.button.grid(row=1, column=11,columnspan=2, rowspan=2)
        """ You can change the place of the button giving
        different values yo the screen_width and screen_height """
        self.button_no_ac.place(x=(screen_width/2)+550,y=100)

        ###################################################################
        #
        # Scale
        #
        ###################################################################
        """ You can change the place of the text giving
        different values yo the screen_width and screen_height """
        self.percep = self.canvas.create_text((screen_width/2)+300,170,font=("Purisa", 16),text = "Scale")

        """ You can change the place of the buttons giving
        different values yo the screen_width and screen_height """
        # button scale 0
        self.button_scale_0 = Button(main, text="0", command=self.scale_0)
        self.button_scale_0.place(x=(screen_width/2)+450,y=150)

        # button scale 1
        self.button_scale_1 = Button(main, text="1", command=self.scale_1)
        self.button_scale_1.place(x=(screen_width/2)+500,y=150)

        # button scale 2
        self.button_scale_2 = Button(main, text="2", command=self.scale_2)
        self.button_scale_2.place(x=(screen_width/2)+550,y=150)

        # button scale 3
        self.button_scale_3 = Button(main, text="3", command=self.scale_3)
        self.button_scale_3.place(x=(screen_width/2)+600,y=150)

        # button scale 4
        self.button_scale_4 = Button(main, text="4", command=self.scale_4)
        self.button_scale_4.place(x=(screen_width/2)+650,y=150)

        # button scale 5
        self.button_scale_5 = Button(main, text="5", command=self.scale_5)
        self.button_scale_5.place(x=(screen_width/2)+700,y=150)



    #----------------
    # BUTTONS
    #----------------
    """Implementation of the next button to change the sample image"""
    def nextButton(self):
        #This is going to be used for debugging
        if self.matrix[self.my_image_number][0] == 99:
            app = Tk()
            app.title("Please select perceptibility")
            app.geometry("500x300+200+200")
            label = Label(app, text="Please select perceptibility before you can continue", height=100, width=100)
            label.pack()
            app.mainloop()
        elif self.matrix[self.my_image_number][1] == 99:
            app = Tk()
            app.title("Please select acceptability")
            app.geometry("500x300+200+200")
            label = Label(app, text="Please select acceptability before you can continue", height=100, width=100)
            label.pack()
            app.mainloop()
        elif self.matrix[self.my_image_number][2] == 99:
            app = Tk()
            app.title("Please select scale")
            app.geometry("500x300+200+200")
            label = Label(app, text="Please select an scale before you can continue", height=100, width=100)
            label.pack()
            app.mainloop()

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
            if self.my_image_number == len(self.my_images)+1:
                self.my_image_number = 0
            if self.vector_of_shown_images[self.my_image_number] == 1:
                self.canvas.itemconfigure(self.texto, text="Sample "+str(self.my_image_number+1),fill='green')
            else:
                self.canvas.itemconfigure(self.texto,text="Sample "+str(self.my_image_number+1),fill='black')
            # change image
            self.canvas.itemconfig(self.image_on_canvas, image = self.my_images[self.my_image_number])


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
            self.my_image_number = len(self.my_images)

        if self.vector_of_shown_images[self.my_image_number] == 1:
            self.canvas.itemconfigure(self.texto,text="Sample "+str(self.my_image_number+1),fill='green')
        else:
            self.canvas.itemconfigure(self.texto,text='Sample '+str(self.my_image_number+1),fill='black')

        # change image
        self.canvas.itemconfig(self.image_on_canvas, image = self.my_images[self.my_image_number])

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
        
        for i in range(0,len(self.matrix)):
            self.f.write(str(self.matrix[i][0])+" "+str(self.matrix[i][1])+" "+str(self.matrix[i][2])+"\n")
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
class almacen():
    def __init__ (self):
        self.entry = Tk()
        self.label1 = Label(self.entry, text="Patient name")
        self.E1 = Entry(self.entry, bd =5)
        self.label1.pack()
        self.E1.pack()
        self.shuffle = BooleanVar()
        self.shu_check = Checkbutton(self.entry, text='Random order of images',variable=self.shuffle, 
                                     onvalue=True, offvalue=False)
        self.shu_check.pack()
        self.label2 = Label(self.entry, text="Folder containing the images")
        self.folder_name = StringVar()
        self.folder_name.set('')
        self.text_folder = Label(self.entry, textvariable=self.folder_name)
        self.select_folder = Button(self.entry, text ="Select folder", command = self.selectFolder)
        self.label2.pack()
        self.select_folder.pack()
        self.text_folder.pack()
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
    def getFolder(self):
        return self.folder_selected
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

v = almacen()
b = observers_window(observers_names)
v.main()
b.main()
path = v.getFolder()
number_of_samples = len(glob(path+'/*.png'))
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
MainWindow(root,description,number_of_observer,v,number_of_samples,shuffle,path)
b.quit()
root.mainloop()
