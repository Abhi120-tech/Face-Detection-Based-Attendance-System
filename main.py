######################### IMPORTING ##############################
import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter import *
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd
import cv2
import os
import csv
import numpy as np
from PIL import Image,ImageTk
import pandas as pd
import datetime
import time
from newreg import*


######################### Functions ###################################

def tick():
    time_string = time.strftime('%H:%M:%S')
    clock.config(text=time_string)
    clock.after(200,tick)




def check_haarcascadefile():
    exists = os.path.isfile("haarcascade_frontalface_default.xml")
    if exists:
        pass
    else:
        mess._show(title='Some file missing', message='Please contact us for help')
        window.destroy()


def assure_path_exists(path):
  dir = os.path.dirname(path)
  if not os.path.exists(dir):
    os.makedirs(dir)

def TrackImages():
    check_haarcascadefile()
    assure_path_exists("Attendance/")
    assure_path_exists("StudentDetails/")
    for k in tv.get_children(): #For Tree view
        tv.delete(k)
    msg = ''
    i = 0
    j = 0
    recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
    exists3 = os.path.isfile("TrainingImageLabel\Trainner.yml")
    if exists3:
        recognizer.read("TrainingImageLabel\Trainner.yml")
    else:
        mess._show(title='Data Missing', message='Please click on Save Profile to reset data!!')
        return
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath);

    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', '', 'Name', '', 'Date', '', 'Time']
    exists1 = os.path.isfile("StudentDetails\StudentDetails.csv")
    if exists1:
        df = pd.read_csv("StudentDetails\StudentDetails.csv")
    else:
        mess._show(title='Details Missing', message='No Students details are inserted yet, please regester!')
        cam.release()
        cv2.destroyAllWindows()
        window.destroy()
    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 5)
            serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
            if (conf < 50):
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa = df.loc[df['SERIAL NO.'] == serial]['NAME'].values
                ID = df.loc[df['SERIAL NO.'] == serial]['ID'].values
               
                ID = str(ID)
                ID = ID[1:-1]
                bb = str(aa)
                bb = bb[2:-2]
               
                
                attendance = [str(ID), '', bb, '', str(date), '', str(timeStamp)]

            else:
                Id = 'Unknown'
                bb = str(Id)
                
           
        
            #cv2.putText(im, str(ID), (260, 150), font, 1, (0, 255, 0), 4)
            cv2.putText(im, str(bb), (260, 335), font, 1, (0, 255, 0), 4)
            

        cv2.imshow('Taking Attendance', im)
        if (cv2.waitKey(1) == ord('q')):
            mess.showinfo("T","ThankYou")
            break
        

    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    exists = os.path.isfile("Attendance\Attendance_" + date + ".csv")
    if exists:
        with open("Attendance\Attendance_" + date + ".csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(attendance)
        csvFile1.close()
    else:
        with open("Attendance\Attendance_" + date + ".csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(col_names)
            writer.writerow(attendance)
        csvFile1.close()
    with open("Attendance\Attendance_" + date + ".csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for lines in reader1:
            i = i + 1
            if (i > 1):
                if (i % 2 != 0):
                    iidd = str(lines[0]) + '   '
                    tv.insert('', 0, text=iidd, values=(str(lines[2]), str(lines[4]), str(lines[6])))
    csvFile1.close()
    cam.release()
    cv2.destroyAllWindows()
    
global key
key = ''

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
day,month,year=date.split("-")

mont={'01':'January',
      '02':'February',
      '03':'March',
      '04':'April',
      '05':'May',
      '06':'June',
      '07':'July',
      '08':'August',
      '09':'September',
      '10':'October',
      '11':'November',
      '12':'December'
      }

###################### GUI FRONT-END ###################

window = tk.Tk()
window.geometry("1920x1020")
window.resizable(True,False)
window.title("Attendance System")


gb = PhotoImage(file ="q.png")
label1 = ttk.Label(window,image = gb)

logo = PhotoImage(file ="logo.png")
label = ttk.Label(window,image = logo)

frame1 = tk.Frame(window, bg="yellow") # bg="#FFF019"
frame1.place(anchor="c",relx=0.51, rely=0.60, relwidth=0.40, relheight=0.75)

trackImg = tk.Button(frame1, text="Click Here to Make Your Attendance", command=TrackImages, fg="white", bg="black", width=35,
                     height=1, activebackground="white", font=('comic', 15, ' bold '))
trackImg.place(x=80, y=50)


label.pack(anchor="nw")

message3 = tk.Label(window, text="Welcome to BIT Patna " ,fg="white",bg="black" ,width=65 ,height=1,font=('Georgia', 29, ' italic '))
message3.place(x=100,y=10)
message3 = tk.Label(window, text="Face Recognition Based Attendance Monitoring System" ,fg="white",bg="black" ,width=65 ,height=1,font=('Georgia', 29, ' italic '))
message3.place(x=100,y=50)
label1.pack()


frame3 = tk.Frame(window, bg="black")
frame3.place(relx=0.40, rely=0.17, relwidth=0.45, relheight=0.04)

frame4 = tk.Frame(window, bg="black",)
frame4.place(relx=0.20, rely=0.17, relwidth=0.38, relheight=0.04)

datef = tk.Label(frame4, text ="     Date :- "+ day+"-"+mont[month]+"-"+year+"           Time :-", fg="white",bg="black",font=('comic', 22, ' bold '))
datef.pack(fill='both',expand=2)

clock = tk.Label(frame3,fg="white" ,width=70 ,height=1,bg="black",font=('comic', 22, ' bold '))
clock.pack(fill='both',expand=1)
tick()



head1 = tk.Label(frame1, text="For Already Registered",width=45  ,height=1, fg="white",bg="black" ,font=('comic', 17, ' bold ') )
head1.place(x=0,y=0)



lbl3 = tk.Label(frame1, text="Attendance Report",width=16  ,fg="black"  ,bg="#FFF019"  ,height=1 ,font=('comic', 17, ' bold '))
lbl3.place(x=170, y=105)

res=0
exists = os.path.isfile("StudentDetails\StudentDetails.csv")
if exists:
    with open("StudentDetails\StudentDetails.csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for l in reader1:
            res = res + 1
    res = (res // 2) - 1
    csvFile1.close()
else:
    res = 0

tv= ttk.Treeview(frame1,height =13,columns = ('name','date','time'))
tv.column('#0',width=82)
tv.column('name',width=130)
tv.column('date',width=133)
tv.column('time',width=133)
tv.grid(row=2,column=0,padx=(50,0),pady=(150,0),columnspan=4)
tv.heading('#0',text ='Roll')
tv.heading('name',text ='NAME')
tv.heading('date',text ='DATE')
tv.heading('time',text ='TIME')

###################### SCROLLBAR ################################

scroll=ttk.Scrollbar(frame1,orient='vertical',command=tv.yview)
scroll.grid(row=2,column=4,padx=(0,100),pady=(150,0),sticky='ns')
tv.configure(yscrollcommand=scroll.set)

###################### New Regestration ##################################

nn = tk.Button(frame1, text="New Registration", command= New_Reg,fg="white"  ,bg="black"  ,width=35 ,height=1, activebackground = "white" ,font=('comic', 15, ' bold '))
nn.place(x=70, y=450)

quitWindow = tk.Button(frame1, text="Quit", command=window.destroy  ,fg="white"  ,bg="black"  ,width=35 ,height=1, activebackground = "white" ,font=('comic', 15, ' bold '))
quitWindow.place(x=70, y=500)

#####################End New Reg#######################


######################Menu Bar############

def Dev():
     mess.showinfo("Developer","Akhil and its Team Members")

def Hel():
     mess.showinfo("Help","Contact on :-bca15027.20@bitmesra.ac.in ")
     


menubar = tk.Menu(window, relief='ridge')
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label='Developer',command=Dev)
filemenu.add_command(label='Help',command=Hel)
filemenu.add_command(label='Exit', command=window.destroy)
menubar.add_cascade(label='Menu', font=('comic', 29, ' bold '), menu=filemenu)

#################End########################

window.configure(menu=menubar)
window.mainloop()