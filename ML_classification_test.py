from sklearn.neighbors import KNeighborsClassifier
import cv2
import pickle
import numpy as np
import os
import csv
import time
from datetime import datetime
from win32com.client import Dispatch

def speak(str1):
    speak=Dispatch(("SAPI.SpVoice"))
    speak.Speak(str1)

video=cv2.VideoCapture(0)
detect_faces=cv2.CascadeClassifier('Data_haar/haarcascade_frontalface_default.xml') # to detect the face
with open('Data_haar/person_names.pkl', 'rb') as f:
    Labels = pickle.load(f)

with open('Data_haar/faces_data.pkl', 'rb') as f:
    Faces=pickle.load(f)

knn=KNeighborsClassifier(n_neighbors=5)
knn.fit(Faces, Labels)
img_background=cv2.imread("background.jpg")

column_name=['Name','Time']

while True:
    ok,frame=video.read() #ok indicates whether the frame was successfully read
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # conversion from BGR (color) to grayscale
    face=detect_faces.detectMultiScale(gray, 1.3 , 5)
    for(x,y,width_img,height_img)in face:
        crop_img=frame[y:y+height_img, x:x+height_img, :]
        resized_img=cv2.resize(crop_img,(50,50)).flatten().reshape(1,-1)
        output=knn.predict(resized_img)

        t=time.time()
        date=datetime.fromtimestamp(t).strftime("%d-%m-%Y")
        timestamp=datetime.fromtimestamp(t).strftime("%H-%M-%S")

        exist=os.path.isfile("Attendance_file/Attendance_"+date+".csv")

        cv2.putText(frame, str(output[0]),(x,y-15),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
        cv2.rectangle(frame,(x,y),(x+width_img,y+height_img),(50,255,50),1) #to display a rectangle around the detected face

        attendance=[str(output[0]), str(timestamp)]

    img_background[162:162+480,55:55+640]=frame
    cv2.imshow("Nour_Ghsaier_Frame (Face Recognition Project)",img_background) #to show the captured frame in a window
    k=cv2.waitKey(1) #keyword binding function (to break while loop)

    if k==ord('o'):
        speak("Attendance Taken..")
        time.sleep(5)
        if exist:
            with open("Attendance_file/Attendance_" + date + ".csv", "+a") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(attendance)
            csvfile.close()
        else:
            with open("Attendance_file/Attendance_"+date+".csv","+a") as csvfile:
                writer=csv.writer(csvfile)
                writer.writerow(column_name)
                writer.writerow(attendance)
            csvfile.close()


    if k==ord('q') : # If 'q' is pressed, the loop breaks, terminating the program.
        break
video.release() #releases the video capture object, closing the connection to the camera
cv2.destroyAllWindows() #close all windows before exiting the program
