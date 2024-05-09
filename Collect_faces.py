import cv2
import pickle
import numpy as np
import os
#-----------------------------------------------------------------------------------------------------------------------#
#to create web camera
#create video capture object in order to capture the frame
video=cv2.VideoCapture(0)
detect_faces=cv2.CascadeClassifier('Data_haar/haarcascade_frontalface_default.xml') # to detect the face
faces_data=[]

person_name=input("Please enter your name: ")
i=0
while True:
    ok,frame=video.read() #ok indicates whether the frame was successfully read
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # conversion from BGR (color) to grayscale
    face=detect_faces.detectMultiScale(gray, 1.3 , 5)
    for(x,y,width_img,height_img)in face:
        crop_img=frame[y:y+height_img, x:x+height_img, :]
        resized_img=cv2.resize(crop_img,(50,50))
        if len(faces_data)<=100 and i%10==0:
           faces_data.append(resized_img)
        i=i+i
        cv2.putText(frame, str(len(faces_data)),(50,50),cv2.FONT_HERSHEY_DUPLEX, 1, (50,255,50),1)
        cv2.rectangle(frame,(x,y),(x+width_img,y+height_img),(50,255,50),1) #to display a rectangle around the detected face
    cv2.imshow("Nour_Ghsaier_Frame (Face Recognition Project)",frame) #to show the captured frame in a window
    k=cv2.waitKey(1) #keyword binding function (to break while loop)
    if k==ord('q') or len(faces_data)==100: # If 'q' is pressed, the loop breaks, terminating the program.
        break
video.release() #releases the video capture object, closing the connection to the camera
cv2.destroyAllWindows() #close all windows before exiting the program
#-----------------------------------------------------------------------------------------------------------------------#
#convert data into numpy array
faces_data=np.asarray(faces_data)
faces_data=faces_data.reshape(100, -1)
#----------------------------------------------------------------------
#store data in pickle file

#store names in pickle file
if 'person_names.pkl' not in os.listdir('Data_haar/'): #to check if the file exists or not
    #If it doesn't exist, it creates a list names containing person_name repeated 100 times and dumps it into the file.
    names=[person_name]*100
    with open ('Data_haar/person_names.pkl', 'wb') as f:
        pickle.dump(names,f)
#If the file already exists, it loads the existing data into the variable names, appends person_name to it 100 times, and then dumps the updated data back into the file.
else:
    with open('Data_haar/person_names.pkl', 'rb') as f:
              names=pickle.load(f)
    names=names+[person_name]*100
    with open('Data_haar/person_names.pkl', 'wb') as f:
            pickle.dump(names, f)

###############
#store faces in pickle file
if 'faces_data.pkl' not in os.listdir('.venv/Data_haar/'):
    with open ('Data_haar/faces_data.pkl', 'wb') as f:
        pickle.dump(faces_data,f)
else:
    with open('Data_haar/faces_data.pkl', 'rb') as f:
              face=pickle.load(f)
    face=np.append(face,faces_data, axis=0)
    with open('Data_haar/faces_data.pkl', 'wb') as f:
            pickle.dump(face, f)