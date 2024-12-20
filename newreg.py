import tkinter as tk
from tkinter import font
from tkinter import *
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd
import cv2
import os
import csv
import numpy as np
from PIL import Image,ImageTk

############## New Reg #####################

def New_Reg():
    wi = tk.Tk()
   
    wi.geometry("1920x1080")
    wi.resizable(True, False)
    wi.title("Attendance System")
    wi.configure(background="#fbb040")
    
    
   

    def assure_path_exists(path):
        dir = os.path.dirname(path)
        if not os.path.exists(dir):
            os.makedirs(dir)

    def check_haarcascadefile():
        exists = os.path.isfile("haarcascade_frontalface_default.xml")
        if exists:
            pass
        else:
            mess._show(title='Some file missing', message='Please contact us for help')
            wi.destroy()

    def TrainImages():
        check_haarcascadefile()
        assure_path_exists("TrainingImageLabel/")
        recognizer = cv2.face_LBPHFaceRecognizer.create()
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        faces, ID = getImagesAndLabels("TrainingImage")
        try:
            recognizer.train(faces, np.array(ID))#no of entery
        except:
            mess._show(title='No Registrations', message='Please Register someone first!!!')
            return
        recognizer.save("TrainingImageLabel\Trainner.yml")#image save with the id & name in trainner.yml
        res = "Profile Saved Successfully"
        message.configure(text=res)
        message.configure(text='Total Registrations till now  : ' + str(ID[0]))#no of entery display
        

    def getImagesAndLabels(path):
        # get the path of all the files in the folder
        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
        # create empth face list
        faces = []
        # create empty ID list
        Ids = []
        # now looping through all the image paths and loading the Ids and the images
        for imagePath in imagePaths:
            # loading the image and converting it to gray scale
            pilImage = Image.open(imagePath).convert('L')
            # Now we are converting the PIL image into numpy array
            imageNp = np.array(pilImage, 'uint8')
            # getting the Id from the image
            ID = int(os.path.split(imagePath)[-1].split(".")[1])
            # extract the face from the training image sample
            faces.append(imageNp)
            Ids.append(ID)
        return faces, Ids

    def check_haarcascadefile():
        exists = os.path.isfile("haarcascade_frontalface_default.xml")
        if exists:
            pass
        else:
            mess._show(title='Some file missing', message='Please contact us for help')
            wi.destroy()

    def TakeImages():
        check_haarcascadefile()
        columns = ['SERIAL NO.', '', 'ID', '', 'NAME', '', 'Branch', '', 'Semester']
        assure_path_exists("StudentDetails/")
        assure_path_exists("TrainingImage/")
        serial = 0
        exists = os.path.isfile("StudentDetails\StudentDetails.csv")
        if exists:
            with open("StudentDetails\StudentDetails.csv", 'r') as csvFile1:
                reader1 = csv.reader(csvFile1)
                for l in reader1:
                    serial = serial + 1
            serial = (serial // 2)
            csvFile1.close()
        else:
            with open("StudentDetails\StudentDetails.csv", 'a+') as csvFile1:
                writer = csv.writer(csvFile1)
                writer.writerow(columns)
                serial = 1
            csvFile1.close()
        Id = (txt.get())
        name = (txt2.get())
        branch = (txt3.get())
        sem = (txt4.get())
        if ((name.isalpha()) or (' ' in name)):
            cam = cv2.VideoCapture(0)
            harcascadePath = "haarcascade_frontalface_default.xml"
            detector = cv2.CascadeClassifier(harcascadePath)
            sampleNum = 0
            while (True):
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 5)
                    # incrementing sample number
                    sampleNum = sampleNum + 1
                    # saving the captured face in the dataset folder TrainingImage
                    cv2.imwrite("TrainingImage\ " + name + "." + str(serial) + "." + Id + '.' + str(sampleNum) + ".jpg",
                                gray[y:y + h, x:x + w])
                    # display the frame
                    cv2.imshow('Taking Images', img)
                # wait for 100 miliseconds
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
                # break if the sample number is morethan 100
                elif sampleNum > 100:
                    break
            cam.release()
            cv2.destroyAllWindows()
            res = "Images Taken for ID : " + Id
            row = [serial, '', Id, '', name, '', branch, '', sem]
            with open('StudentDetails\StudentDetails.csv', 'a+') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(row)
            csvFile.close()
            message.configure(text=res)
        else:
            if (name.isalpha() == False):
                res = "Enter Correct name"
                message.configure(text=res)

    def re():
        txt.delete(0, END)
        txt2.delete(0, END)
        txt3.delete(0, END)
        txt4.delete(0, END)
   

 
    frame2 = tk.Frame(wi,width=10,height=1080, bg="yellow") # bg="#11FFEE"
    frame2.place(anchor="c",relx=0.51, rely=0.56, relwidth=0.35, relheight=0.85)
   
    message3 = tk.Label(wi, text="Welcome to BIT Patna ", fg="white", bg="black", width=70, height=1, font=('Georgia', 29, ' italic '))
    message3.place(y=10)

    message3 = tk.Label(wi, text="For New Registration Pls Fill the Form ", fg="white", bg="black", width=70, height=1, font=('Georgia', 29, ' italic '))
    message3.place(y=50)

    head2 = tk.Label(frame2, text="For New Registrations", width=38, height=1, fg="white", bg="black", font=('comic', 17, ' bold '))
    head2.grid(row=0, column=0)

    takeImg = tk.Button(frame2, text="Upload your Image", command=TakeImages, fg="white", bg="black", width=36, height=1, activebackground="white", font=('comic', 15, ' bold '))
    takeImg.place(x=40, y=400)

    trainImg = tk.Button(frame2, text="Save Profile", command=TrainImages, fg="white", bg="black", width=36, height=1, activebackground="white", font=('comic', 15, 'bold '))
    trainImg.place(x=40, y=500)

    quitWindow = tk.Button(frame2, text="Quit", command=wi.destroy, fg="white", bg="black", width=36, height=1, activebackground="white", font=('comic', 15, ' bold '))
    quitWindow.place(x=40, y=600)

    resest = tk.Button(frame2, text="Reset", command=re, fg="white", bg="black", width=36, height=1, activebackground="white", font=('comic', 15, ' bold '))
    resest.place(x=40, y=550)

####################All Entery###########3
    lbl = tk.Label(frame2, text="Enter Roll No", width=20, height=1, fg="white", bg="black", font=('comic', 17, ' bold '))
    lbl.place(x=110, y=50)

    txt = tk.Entry(frame2, width=32, fg="black", font=('comic', 15, ' bold '))
    txt.place(x=70, y=90)

    lbl2 = tk.Label(frame2, text="Enter Name", width=20, fg="white", bg="black", font=('comic', 17, ' bold '))
    lbl2.place(x=110, y=130)

    txt2 = tk.Entry(frame2, width=32, fg="black", font=('comic', 15, ' bold '))
    txt2.place(x=70, y=173)

    lbl5 = tk.Label(frame2, text="Enter Branch", width=20, fg="white", bg="black", font=('comic', 17, ' bold '))
    lbl5.place(x=110, y=215)

    txt3 = tk.Entry(frame2, width=32, fg="black", font=('comic', 15, ' bold '))
    txt3.place(x=70, y=260)

    lbl6 = tk.Label(frame2, text="Enter Semeseter", width=20, fg="white", bg="black", font=('comic', 17, ' bold '))
    lbl6.place(x=110, y=300)

    txt4 = tk.Entry(frame2, width=32, fg="black", font=('comic', 15, ' bold '))
    txt4.place(x=70, y=344)

    message = tk.Label(frame2, text="", bg="#c79cff", fg="black", width=39, height=1, activebackground="#3ffc00",font=('comic', 16, ' bold '))
    message.place(x=7, y=450)
   
    wi.mainloop()
#New_Reg()