import cv2
import numpy as np
import face_recognition
import os
import sys
from PIL import ImageGrab
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import inspect
import time
from itertools import count
from multiprocessing import Process
from tkinter import filedialog

path = 'student_photos'
images = []     # LIST CONTAINING ALL THE IMAGES
className = []    # LIST CONTAINING ALL THE CORRESPONDING CLASS Names
myList = os.listdir(path)
#print("Total Classes Detected:",len(myList))
for x,cl in enumerate(myList):
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        className.append(os.path.splitext(cl)[0])

def open_file():
    root.filename =  filedialog.askopenfilename(initialdir = "C:\\Users\\hilel\\PycharmProjects\\zoom_attandent",title = "Select file",filetypes = (("CSC files", "*.csv"),("all files","*.*")))

def zoom():
   messagebox.showinfo("Next Step", "Go To Zoom Call And Look At Students")

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
        print("trr")
    return encodeList

def markAttendance(name):
    with open('Attendance.csv','r+') as f:
        myDataList = f.readlines()
        print('aaa')
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
            label['text'] = nameList, 
        if name not in nameList:
            now = datetime.now()
            dt_string = now.strftime("%H:%M:%S")
            f.writelines(f'\n{name},{dt_string}')

encodeListKnown = findEncodings(images)

print("f")

def start():
    t_end = time.time() + 60 # sec
    while time.time() < t_end:
        img = ImageGrab.grab()
        img_np = np.array(img)
        imgS = cv2.resize(img_np, (0, 0), fx=0.25, fy=0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        print(t_end)
        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
        print('ddd')
        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            print(faceDis)
            print("ll")
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                name = className[matchIndex].upper()
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img_np, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img_np, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img_np, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)
                markAttendance(name)

#########################################  GUI #########################################

root = tk.Tk()
canvas = tk.Canvas(root, height=400, width=400)
canvas.pack()

background_image = tk.PhotoImage(file='MB.png')
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

frame = tk.Frame(root, bg='#331100', bd=5)
frame.place(relx=0.5, rely=0.1, relwidth=1, relheight=0.1, anchor='n')

button = tk.Button(frame, text="Excel", font=3, command=lambda: open_file())
button.place(relx=0.55, relheight=1, relwidth=0.45)

button = tk.Button(frame, text="Take Attendants", font=3, command=lambda: [zoom(), start()])
button.place(relx=0.01, relheight=1, relwidth=0.45)

lower_frame = tk.Frame(root, bg='#331100', bd=10)
lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor = 'n')

label = tk.Label(lower_frame, )
label.place(relwidth=1, relheight=1)

root.mainloop()

