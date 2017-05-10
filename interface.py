## Stanford ME310 - Product interface

## Import Libraries and functions from other .py files
import Tkinter as tk # For the actual interface widows display
import RPi.GPIO as GPIO # for Raspberry pi pins control
import time     #for serial comm
import serial   #for serial comm
from SimpleCV import Color,Camera,Display   #for barcode scanner

import sys
from Tkinter import * # different functions used different notations... for that import again
from pygame import * # for graphic processing (images in label)

from PIL import ImageTk, Image # for graphic processing (images in label)

LARGE_FONT = ("Verdana",15) # Define for display on window
buttonColorNumpad = '#39dddb'

######################################===================Main container for interface===================#############################################

class SPAInterface(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self) #Main container frame for the windows

        # Formats the way the interface window is displayed ...       
##        self.attributes('-zoomed', True) # Makes the window maximized
        self.attributes('-fullscreen', True) # Makes the window fullscreen
        
        container.pack(side="top", fill="both", expand = True) #put the container on screen

#       Configure the placement of the window
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

#       Add the names of each page in the (...) below for it to be displayed
        for F in (StartPage, PageOne, OTP,Instruction2,Instruction3,Barcode,Instruction4,Instruction5,Instruction6,Barcode_type):  ### Add names of pages here to navigate
            # Configure each window
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew") 

        self.show_frame(StartPage) #shows the StartPage frame

    def show_frame(self, cont):
        # defines the show_frame function used above
        
        frame = self.frames[cont]
        frame.tkraise()

######################################==================Each window separately====================#############################################
################# each window that you want should be defined as a separate class ################
        
class StartPage(tk.Frame):
    # This page is displayed when the program first starts
    
    def __init__(self, parent, controller):
        # define what is present on this page
        
        tk.Frame.__init__(self, parent) #Main frame on the page
        self.configure(background='white') # add backgrond page to this page specifically
        # Now define frames along side the main frame to divide the screen into sections for placing the attributes
        
        #Sub frame along side main frame F0 
        F0=tk.Frame(self,parent)
        F0.pack(side = 'right')
        
        #Sub frame along side main frame F1
        F1 = tk.Frame(self,parent)
        F1.pack(side = 'bottom')
        
        # place objects/attributes in the desired frames

        #Labels
        label = tk.Label(self, text="Welcome",font=14, bg='white')
        label.pack(pady=10, padx=10)

        label2 = tk.Label(self, text="I will guide you through the SPA delivery system",font=14, bg='white')
        label2.pack(pady=10, padx=10)

        label3 = tk.Label(self, text="First, you need to confirm your identity. ",font=LARGE_FONT, bg='white')
        label3.pack(pady=10, padx=10)
        
        label4 = tk.Label(self, text = 'Please start by verifying your secure access code.',font=LARGE_FONT,bg='white')
        label4.pack()
        
        #Buttons
        #(command=lambda:controller.show_frame(PageOne)) takes the window to PageOne when the button is pressed
        button2 = tk.Button(self, text="Verify", command=lambda:controller.show_frame(OTP),padx=50,pady=20, bd=8,fg='white',bg='black', font=30)
        button2.pack()

        button3 = tk.Button(F1, text="Exit", command=lambda:app.destroy(),padx=5,pady=1, bd=4,fg='white',bg='black', font=30)
        button3.pack(side='left')

###############---------------------------#####################

class PageOne(tk.Frame):
    # Sample page to start another page (not used in the program) 

    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent) #Main frame on the page

        #Labels
        label = tk.Label(self, text="Page One",font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        #Buttons
        button1 = tk.Button(self, text="Visit Start Page", command=lambda:controller.show_frame(StartPage))
        button1.pack()

###############---------------------------#####################

class OTP(tk.Frame):
    # OTP/ID number verification page
    
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent) #Main frame on the page
        self.configure(background='white') # Configure background color of the main frame
        
        # Frame for Lable and text box
        F0 = tk.Frame(self,parent)
        F0.configure(background='white')
        F0.pack(side='top')
        # Frame for numpad
        F = tk.Frame(self,parent)
        F.configure(background='white')
        F.pack(side='top')
        # frame for numbers 1 2 3
        f1 = tk.Frame(F,parent)
        f1.pack(side='top')
        # frame for numbers 4 5 6
        f2 = tk.Frame(F,parent)
        f2.pack(side='top')
        # frame for numbers 7 8 9
        f3 = tk.Frame(F,parent)
        f3.pack(side='top')
        # frame for numbers 0
        f4 = tk.Frame(F,parent)
        f4.pack(side='top')
        # frame for numbers Clear and Submit
        f5 = tk.Frame(F,parent)
        f5.pack(side='top')
        # frame for numbers Go back
        f6 = tk.Frame(F,parent)
        f6.pack(side='top')

        f7 = tk.Frame(F,parent)
        f7.pack(side='top')

        # Proceed variable
        self.matchID=False
        

        ### now defining the functions for each button and assisting operations ###
        
        def btnClick(numbers):
            # function for each button on the numpad being pressed
            self.operator = self.operator+str(numbers) # Add the pressed number to existing input
            num1.set(self.operator) # display the present total input in the text box

        def submit():
            # Function for submitting the ID  for verification

            # check if the entered input matches the required ID
            if self.operator == '24':
                controller.show_frame(Instruction3) #Proceed to further instructions
            else:
                controller.show_frame(Instruction2) #Proceed to further instructions
                
            self.operator='' # Clean the memory of the numpad textbox
            num1.set(self.operator) #Set the textbox to blank again

        def clear():
            # backspace function
            self.operator=self.operator[0:-1] # Remove the last entered digit
            num1.set(self.operator) #set the display to new value

                       
        num1 = tk.StringVar() # A String Variable used to display thhe text in the text box on the window

        self.operator=''  # The variable that stores the entered input for numpad while operation

        #Instrunction Label
        label = tk.Label(F0, text="Plese enter your secure access code here and press 'SUBMIT' to verify",font=LARGE_FONT,bg='white')
        label.pack(pady=10, padx=10)

        #Home Button
        buttonback = tk.Button(f6, text="Home", command=lambda:controller.show_frame(StartPage), padx=20,pady=10, bd=8,fg='white',bg='black', font=30)
        buttonback.pack(side='left')

        #Textbox
        txtDisplay = tk.Entry(F0, textvariable = num1,bd=10, insertwidth=1, font=120)
        txtDisplay.pack(side='top',ipady=15,ipadx=5)

        ### Numpad Buttons ###

        # First row
        button1 = tk.Button(f1, text="1", command=lambda:btnClick(1), padx=25,pady=4, bd=8,fg='black',bg=buttonColorNumpad, font=30)
        button1.pack(side='left')

        button2 = tk.Button(f1, text="2", command=lambda:btnClick(2), padx=25,pady=4, bd=8,fg='black',bg=buttonColorNumpad, font=30)
        button2.pack(side='left')

        button3 = tk.Button(f1, text="3", command=lambda:btnClick(3), padx=25,pady=4, bd=8,fg='black',bg=buttonColorNumpad, font=30)
        button3.pack(side='left')

        # Second row 
        button4 = tk.Button(f2, text="4", command=lambda:btnClick(4), padx=25,pady=4, bd=8,fg='black',bg=buttonColorNumpad, font=30)
        button4.pack(side='left')

        button5 = tk.Button(f2, text="5", command=lambda:btnClick(5), padx=25,pady=4, bd=8,fg='black',bg=buttonColorNumpad, font=30)
        button5.pack(side='left')

        button6 = tk.Button(f2, text="6", command=lambda:btnClick(6), padx=25,pady=4, bd=8,fg='black',bg=buttonColorNumpad, font=30)
        button6.pack(side='left')

        # Third row
        button7 = tk.Button(f3, text="7", command=lambda:btnClick(7), padx=25,pady=4, bd=8,fg='black',bg=buttonColorNumpad, font=30)
        button7.pack(side='left')

        button8 = tk.Button(f3, text="8", command=lambda:btnClick(8), padx=25,pady=4, bd=8,fg='black',bg=buttonColorNumpad, font=30)
        button8.pack(side='left')

        button9 = tk.Button(f3, text="9", command=lambda:btnClick(9), padx=25,pady=4, bd=8,fg='black',bg=buttonColorNumpad, font=30)
        button9.pack(side='left')

        # Fourth row
        button0 = tk.Button(f4, text="0", command=lambda:btnClick(0), padx=25,pady=4, bd=8,fg='black',bg=buttonColorNumpad, font=30)
        button0.pack(side='left')

        # Fifth row
        buttonClear = tk.Button(f5, text="Clear", command=clear, padx=25,pady=4, bd=8,fg='black',bg='red', font=30)
        buttonClear.pack(side='left')

        buttonSubmit = tk.Button(f5, text="SUBMIT", command=submit,bg='green', padx=25,pady=4, bd=8,fg='black', font=30)
        buttonSubmit.pack(side='left')


###############---------------------------#####################
        
class Instruction2(tk.Frame):
    # Instructions if the the OTP/ID is wrong

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) # Main Frame on the page
        self.configure(background='white') # Add background to main frame

        #Message
        label = tk.Label(self, text="The Identification you entered does not match the record.",bg='white',font=17)
        label.pack(pady=10, padx=10)

        #Image on the screen
        self.photo = tk.PhotoImage(file="sorry.png") #load image
        label1=tk.Label(self,text='Sorry',borderwidth=0) # label to display the image
        label1.configure(image=self.photo) #assign the image to the label
        label1.pack(side='top') #display the label on screen

        
        #Buttons
        button1 = tk.Button(self, text="Home", command=lambda:controller.show_frame(StartPage),bd=8,padx=40,pady=30,bg='black',fg='white',font=30)
        button1.pack(side='left')

        button2 = tk.Button(self, text="Try Again", command=lambda:controller.show_frame(OTP),bd=8, padx=40,pady=30, bg='black',fg='white',font=30)
        button2.pack(side='right')

###############---------------------------#####################

class Instruction3(tk.Frame):
    # Instructions if the OTP/ID is correct

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) # Main frame on the page
        self.configure(background='white') # add backgroound color

        #Message
        label = tk.Label(self, text="Your identification matched",bg='white',font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        label2 = tk.Label(self, text=" Now please scan the barcode on your package with the camera in the figure",font=20,bg='white')
        label2.pack()

        #Image of camera
        Img_in = Image.open('camera.png') # load image
        Img = Img_in.resize((200,200),Image.ANTIALIAS) #shrink image to fit raspberry pi screen size
        self.photo = ImageTk.PhotoImage(Img) 

        label1=tk.Label(self,text='camera',)
        label1.configure(image=self.photo)
        label1.pack(side='top')

        #Buttons
            #Home button
        button3 = tk.Button(self, text="Home", command=lambda:controller.show_frame(StartPage),bd=8,padx=40,pady=30,bg='black',fg='white',font=30)
        button3.pack(side='left')

            # Scan barcode button
        button2 = tk.Button(self, text="Scan", command=lambda:controller.show_frame(Barcode),bd=8, padx=40,pady=30, bg='black',fg='white',font=30)
        button2.pack(side='right')

            #Type barcode button
        button1 = tk.Button(self, text="Type", command=lambda:controller.show_frame(Barcode_type),bd=8,padx=40,pady=30,bg='black',fg='white',font=30)
        button1.pack(side='left')

###############---------------------------#####################

class Barcode(tk.Frame):
    # Page to scan the barcode

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) #Main frame
        self.configure(background='white')

        # sub frame along main frame F1
        F1=tk.Frame(self,parent)
        F1.pack(side='right')

        #Message
        label = tk.Label(self, text="Scan the barcode at the camera",font=LARGE_FONT,bg='white')
        label.pack(pady=10, padx=10)

        #Label to display the video wile scanning
        self.labeli = tk.Label(self,text ='Press SCAN to start scanning',font=20,bg='white')
        self.labeli.pack()

        # flag variable
        self.flag = True
        
        def scanBarcode():
            # function to scan the barcode
            try:
                #Try if the following is possible, if error, move to except
                global job1 # global variable job1 that keeps track of the scanning function being called

                # Get all the stored barcodes
                In_Barcodes=get_Barcodes()
                if not In_Barcodes:
                    # if the stored barcodes are zero, return
                    return "error",4021

                # Else, start the scanning process
                
                cam = Camera()  #starts the camera (camera uses SimpleCV functions)
    ##            display = Display() # used to creat a display for the camera
                if(self.flag):
                    img = cam.getImage()		#gets image from the camera
                    IMG = ImageTk.PhotoImage(img.getPIL()) #Manipulate the image to make it possible to put in label
                    
                    if self.labeli is None:
                        # if this label is not initialized, then initialize it
                        self.labeli = tk.Label(image = IMG,bg='blue')
                        self.labeli.image=IMG
                        self.labeli.pack()
                        app.update_idletasks()
                    else:
                        # put the camera camputred image into the label
                        self.labeli.configure(image=IMG)
                        self.labeli.image=IMG
                        self.labeli.pack()
                        app.update_idletasks()

                        
                    barcode = img.findBarcode() #finds barcode data from image
                    print(barcode) # print the barcode in the console/IDE fro your verification (gives None if no barcode)
                    
                    if(barcode is not None): 	#if there is some data processed (None => no data/barcode)
                        barcode = barcode[0]    #take the barcode value
                        result = str(barcode.data) #convert it into string
                        print (result)  # print barcode value in IDE/console
                        
                        In_Barcodes=get_Barcodes() # retrive the stored barcodes
                        if result in In_Barcodes:  #compare barcode with library
                                                    ##delete barcode in the library (Not implemented here)             
                            print "barcode matched"
                    
                            onClose() # Stop the camera process
                            controller.show_frame(Instruction4) # Move to further instructions
                            
                            return 'success',2021
                        else:
                            print('barcode not matched') 
                            onClose() # Stop the camera process
                            controller.show_frame(Instruction6) # Move to further instructions
                            return
                        
                        barcode = [] 			#reset barcode data to empty set
    ##                img.save(display) 			#shows the image on the screen (used with displa enabled)
                    job1 = app.after(1, scanBarcode) #sets the global job1 variable to act 1 milisecond after the mainloop of the SPAInterface is executed
                return 'success',2022
            except:
                # If there was an error in the above execution 
                print('Error int scan barcode') 

        def get_Barcodes():
            # getting the stored barcodes from a predefined storage file
            f=open('Input_barcodes.txt') #Open the file
            barcodes=[]
            for line in f:
                barcodes=str.split(line)
            f.close()
            return barcodes

        def remove_Barcode(value):
            #remove the used barcodes from the storage file
            Barcodes=get_Barcodes()
            if value in Barcodes:
                f=open('Input_barcodes.txt','w')
                Barcodes.remove(value)
                for val in Barcodes:
                    f.write(val+'\t')
                f.close()   
                return 'success',2051
            else:
                return 'error',4051

        def onClose():
            #Stopping the scan function
            self.Flag = False
            try:
                global job1
                app.after_cancel(job1) #cancle the job1 = stop scanning
                self.labeli.configure(image='') # set the image on the video lable to blank
            except:
                print('Error in OnClose')

        def onHome():
            # returing to home screen 
            try:
                self.Flag = False
                global job1
                app.after_cancel(job1) #cancel the job1 = stop scanning
                self.labeli.configure(image='') # set the image on the video lable to blank
                controller.show_frame(StartPage) #move to start page
            except:
                print('In Home')
                controller.show_frame(StartPage) #move to start page
                    

        #Buttons

                #Scan Button
        button1 = tk.Button(F1, text="SCAN", command=scanBarcode,bd=8,padx=40,pady=30,bg='black',fg='white',font=30)
        button1.pack()
        
                # Stop Button
        button2 = tk.Button(F1, text="Stop", command=onClose,bd=8, padx=40,pady=30, bg='black',fg='white',font=30)
        button2.pack(side='top')

                # Home Button
        button2 = tk.Button(F1, text="Home", command=onHome,bd=8, padx=40,pady=30, bg='black',fg='white',font=30)
        button2.pack(side='top')


###############---------------------------#####################

class Instruction4(tk.Frame):

    def __init__(self, parent, controller):
        # instructions if barcode matches
        
        tk.Frame.__init__(self, parent) # Main frame
        self.configure(background='white')

        #Message
        label = tk.Label(self, text="Great! All your credentials matched.",bg='white',font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        label2 = tk.Label(self, text=" Sure you want to unlock the door?",font=20,bg='white')
        label2.pack()

        #Image
        Img_in = Image.open('thumbsup.png')
        Img = Img_in.resize((200,200),Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(Img)
        
        label1=tk.Label(self,text='great',borderwidth=0)
        label1.configure(image=self.photo)
        label1.pack(side='top')

        #Buttons
                #Yes
        button1 = tk.Button(self, text="Yes, let me in please", command=lambda:controller.show_frame(Instruction5),bd=8,padx=40,pady=30,bg='black',fg='white',font=30)
        button1.pack(side='right')

                #No
        button2 = tk.Button(self, text="No, I don't want to enter, Cancel it please", command=lambda:controller.show_frame(StartPage),bd=8, padx=40,pady=30, bg='black',fg='white',font=30)
        button2.pack(side='left')

###############---------------------------#####################
        
class Instruction5(tk.Frame):
    # Instructions if you unlock the door lock

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) # Main frame
        self.configure(background='white')

        #Labels
        label = tk.Label(self, text='you are in the house',font=LARGE_FONT,bg='white')
        label.pack(pady=10, padx=10)

        #Buttons
        button1 = tk.Button(self, text="Home", command=lambda:controller.show_frame(StartPage),bd=8,padx=40,pady=30,bg='black',fg='white',font=30)
        button1.pack(side='left')

###############---------------------------#####################

class Instruction6(tk.Frame):
    # Insatructions if the barcode is not verified

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) #Main frame
        self.configure(background='white')

        #Message
        label = tk.Label(self, text="Sorry, your package barcode does not match the designated one",bg='white',font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        label2 = tk.Label(self, text=" Would you like to try again with another package? ",font=20,bg='white')
        label2.pack()

        #Image
        self.photo = tk.PhotoImage(file="sorry.png")
        label1=tk.Label(self,text='Sorry',borderwidth=0)
        label1.configure(image=self.photo)
        label1.pack(side='top')

        #Buttons
                #Home
        button1 = tk.Button(self, text="Home", command=lambda:controller.show_frame(StartPage),bd=8,padx=40,pady=30,bg='black',fg='white',font=30)
        button1.pack(side='left')

                #Try again
        button2 = tk.Button(self, text="Try Again", command=lambda:controller.show_frame(Instruction3),bd=8, padx=40,pady=30, bg='black',fg='white',font=30)
        button2.pack(side='right')

###############---------------------------#####################

class Barcode_type(tk.Frame):
    # Manually type the barcode

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) #Main frame
        self.configure(background='white')
        
        # Frame for Lable and text box
        F0 = tk.Frame(self,parent)
        F0.configure(background='white')
        F0.pack(side='top')
        # Frame for numpad
        F = tk.Frame(self,parent)
        F.configure(background='white')
        F.pack(side='top')
        # frame for numbers 1234567890
        f1 = tk.Frame(F,parent)
        f1.pack(side='top')
        # frame for numbers qwertyuiop
        f2 = tk.Frame(F,parent)
        f2.pack(side='top')
        # frame for numbers asdfghjkl
        f3 = tk.Frame(F,parent)
        f3.pack(side='top')
        # frame for numbers zxcvbnm
        f4 = tk.Frame(F,parent)
        f4.pack(side='top')
        # frame for numbers Clear and Submit
        f5 = tk.Frame(F,parent)
        f5.pack(side='top')
        # frame for numbers Go back
        f6 = tk.Frame(F,parent)
        f6.pack(side='top')

        f7 = tk.Frame(F,parent)
        f7.pack(side='top')

        # Proceed variable
        self.matchID=False
        

        
        def btnClick(param):
        
            self.operator = self.operator+str(param)
            num1.set(self.operator)
##            print(self.operator)

        def submit():
##            print('final = ',self.operator)
            In_Barcodes = get_Barcodes()
            if self.operator in In_Barcodes: # verify if the barcode is in the stored file
                controller.show_frame(Instruction4) # Proceed to further instructions
            else:
                controller.show_frame(Instruction6) # Procedd to instructions
            self.operator='' #reset operator
            num1.set(self.operator) #reset display

        def clear():
            #backspace function
            self.operator=self.operator[0:-1]
            num1.set(self.operator)

        def get_Barcodes():
            f=open('Input_barcodes.txt')
            barcodes=[]
            for line in f:
                barcodes=str.split(line)
            f.close()
            return barcodes

                       
        num1 = tk.StringVar() # A String Variable used to display thhe text in the text box on the window

        self.operator=''  # The variable that stores the entered input for numpad while operation

        #Message
        label = tk.Label(F0, text="Plese enter the Barcode number here and press 'SUBMIT' to verify",font=LARGE_FONT,bg='white')
        label.pack(pady=10, padx=10)

        # Home button
        buttonback = tk.Button(f6, text="Home", command=lambda:controller.show_frame(StartPage), padx=20,pady=10, bd=8,fg='white',bg='black', font=30)
        buttonback.pack(side='left')

        #text box
        txtDisplay = tk.Entry(F0, textvariable = num1,bd=10, insertwidth=1, font=120)
        txtDisplay.pack(side='top',ipady=15,ipadx=5)

        ### Keyboard ###

        #1234567890 Buttons
        button1 = tk.Button(f1, text="1", command=lambda:btnClick(1), padx=25,pady=4, bd=8,fg='black',bg=buttonColorNumpad, font=30)
        button1.pack(side='left')

        button2 = tk.Button(f1, text="2", command=lambda:btnClick(2), padx=25,pady=4, bd=8,fg='black',bg=buttonColorNumpad, font=30)
        button2.pack(side='left')

        button3 = tk.Button(f1, text="3", command=lambda:btnClick(3), padx=25,pady=4, bd=8,fg='black',bg=buttonColorNumpad, font=30)
        button3.pack(side='left')

        button4 = tk.Button(f1, text="4", command=lambda:btnClick(4), padx=25,pady=4, bd=8,fg='black',bg=buttonColorNumpad, font=30)
        button4.pack(side='left')

        button5 = tk.Button(f1, text="5", command=lambda:btnClick(5), padx=25,pady=4, bd=8,fg='black',bg=buttonColorNumpad, font=30)
        button5.pack(side='left')

        button6 = tk.Button(f1, text="6", command=lambda:btnClick(6), padx=25,pady=4, bd=8,fg='black',bg=buttonColorNumpad, font=30)
        button6.pack(side='left')

        button7 = tk.Button(f1, text="7", command=lambda:btnClick(7), padx=25,pady=4, bd=8,fg='black',bg=buttonColorNumpad, font=30)
        button7.pack(side='left')

        button8 = tk.Button(f1, text="8", command=lambda:btnClick(8), padx=25,pady=4, bd=8,fg='black',bg=buttonColorNumpad, font=30)
        button8.pack(side='left')

        button9 = tk.Button(f1, text="9", command=lambda:btnClick(9), padx=25,pady=4, bd=8,fg='black',bg=buttonColorNumpad, font=30)
        button9.pack(side='left')

        button0 = tk.Button(f1, text="0", command=lambda:btnClick(0), padx=25,pady=4, bd=8,fg='black',bg=buttonColorNumpad, font=30)
        button0.pack(side='left')

        #qwertyuiop Buttons
        buttonQ = tk.Button(f2, text="Q", command=lambda:btnClick('Q'), padx=25,pady=4, bd=8,fg='black',bg=buttonColorNumpad, font=30)
        buttonQ.pack(side='left')

        buttonW = tk.Button(f2, text="W", command=lambda:btnClick('W'), padx=25,pady=4, bd=8,fg='black',bg=buttonColorNumpad, font=30)
        buttonW.pack(side='left')

        buttonE = tk.Button(f2, text="E", command=lambda:btnClick('E'), padx=25,pady=4, bd=8,fg='black',bg=buttonColorNumpad, font=30)
        buttonE.pack(side='left')

        buttonR = tk.Button(f2, text="R", command=lambda:btnClick('R'), padx=25,pady=4, bd=8,fg='black',bg=buttonColorNumpad, font=30)
        buttonR.pack(side='left')

        buttonT = tk.Button(f2, text="T", command=lambda:btnClick('T'), padx=25,pady=4, bd=8,fg='black',bg=buttonColorNumpad, font=30)
        buttonT.pack(side='left')

        buttonY = tk.Button(f2, text="Y", command=lambda:btnClick('Y'), padx=25,pady=4, bd=8,fg='black',bg=buttonColorNumpad, font=30)
        buttonY.pack(side='left')

        buttonU = tk.Button(f2, text="U", command=lambda:btnClick('U'), padx=25,pady=4, bd=8,fg='black',bg=buttonColorNumpad, font=30)
        buttonU.pack(side='left')

        buttonI = tk.Button(f2, text="I", command=lambda:btnClick('I'), padx=25,pady=4, bd=8,fg='black',bg=buttonColorNumpad, font=30)
        buttonI.pack(side='left')

        buttonO = tk.Button(f2, text="O", command=lambda:btnClick('O'), padx=25,pady=4, bd=8,fg='black',bg=buttonColorNumpad, font=30)
        buttonO.pack(side='left')

        buttonP = tk.Button(f2, text="P", command=lambda:btnClick('P'), padx=25,pady=4, bd=8,fg='black',bg=buttonColorNumpad, font=30)
        buttonP.pack(side='left')

        #asdfghjkl Buttons
        buttonA = tk.Button(f3, text="A", command=lambda:btnClick('A'), padx=25,pady=4, bd=8,fg='black',bg=buttonColorNumpad, font=30)
        buttonA.pack(side='left')

        buttonS = tk.Button(f3, text="S", command=lambda:btnClick('S'), padx=25,pady=4, bd=8,fg='black',bg=buttonColorNumpad, font=30)
        buttonS.pack(side='left')

        buttonD = tk.Button(f3, text="D", command=lambda:btnClick('D'), padx=25,pady=4, bd=8,fg='black',bg=buttonColorNumpad, font=30)
        buttonD.pack(side='left')

        buttonF = tk.Button(f3, text="F", command=lambda:btnClick('F'), padx=25,pady=4, bd=8,fg='black',bg=buttonColorNumpad, font=30)
        buttonF.pack(side='left')

        buttonG = tk.Button(f3, text="G", command=lambda:btnClick('G'), padx=25,pady=4, bd=8,fg='black',bg=buttonColorNumpad, font=30)
        buttonG.pack(side='left')

        buttonH = tk.Button(f3, text="H", command=lambda:btnClick('H'), padx=25,pady=4, bd=8,fg='black',bg=buttonColorNumpad, font=30)
        buttonH.pack(side='left')

        buttonJ = tk.Button(f3, text="J", command=lambda:btnClick('J'), padx=25,pady=4, bd=8,fg='black',bg=buttonColorNumpad, font=30)
        buttonJ.pack(side='left')

        buttonK = tk.Button(f3, text="K", command=lambda:btnClick('K'), padx=25,pady=4, bd=8,fg='black',bg=buttonColorNumpad, font=30)
        buttonK.pack(side='left')

        buttonL = tk.Button(f3, text="L", command=lambda:btnClick('L'), padx=25,pady=4, bd=8,fg='black',bg=buttonColorNumpad, font=30)
        buttonL.pack(side='left')

        #zxcvbnm Buttons
        buttonZ = tk.Button(f4, text="Z", command=lambda:btnClick('Z'), padx=25,pady=4, bd=8,fg='black',bg=buttonColorNumpad, font=30)
        buttonZ.pack(side='left')

        buttonX = tk.Button(f4, text="X", command=lambda:btnClick('X'), padx=25,pady=4, bd=8,fg='black',bg=buttonColorNumpad, font=30)
        buttonX.pack(side='left')

        buttonC = tk.Button(f4, text="C", command=lambda:btnClick('C'), padx=25,pady=4, bd=8,fg='black',bg=buttonColorNumpad, font=30)
        buttonC.pack(side='left')

        buttonV = tk.Button(f4, text="V", command=lambda:btnClick('V'), padx=25,pady=4, bd=8,fg='black',bg=buttonColorNumpad, font=30)
        buttonV.pack(side='left')

        buttonB = tk.Button(f4, text="B", command=lambda:btnClick('B'), padx=25,pady=4, bd=8,fg='black',bg=buttonColorNumpad, font=30)
        buttonB.pack(side='left')

        buttonN = tk.Button(f4, text="N", command=lambda:btnClick('N'), padx=25,pady=4, bd=8,fg='black',bg=buttonColorNumpad, font=30)
        buttonN.pack(side='left')

        buttonM = tk.Button(f4, text="M", command=lambda:btnClick('M'), padx=25,pady=4, bd=8,fg='black',bg=buttonColorNumpad, font=30)
        buttonM.pack(side='left') 

        
        # Clear and Submit Buttons
        buttonClear = tk.Button(f5, text="Clear", command=clear, padx=25,pady=10, bd=8,fg='black',bg='red', font=30)
        buttonClear.pack(side='left')

        buttonEnter = tk.Button(f5, text="SUBMIT", command=submit,bg='green', padx=25,pady=10, bd=8,fg='black', font=30)
        buttonEnter.pack(side='left')

######################################===================Run the Interface===================#############################################
        
app = SPAInterface()
app.mainloop()
