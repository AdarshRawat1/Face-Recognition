import cv2
import numpy as np
import face_recognition
import image
from datetime import datetime
import csv 
from db import Database

unknown_user_dir = "./unknown_user/"
unknown_user_name = "unknown_user"
db = Database()
students = db.get_all_user_ids()

# Video capture from webcam
video_capture = cv2.VideoCapture(0)
user_detail_list=[]
face_names=[]
s=True
now = datetime.now()
current_date = now.strftime("%Y-%m-%d")

# CSV file 

f = open(current_date+'.csv', 'w+', newline='')
lnwrite = csv.writer(f)

# Reading video input from webcam
while True:
        ret,frame = video_capture.read()
        if not ret:
            print("Failed to grab frame")
            continue
        small_frame= cv2.resize(frame, (0, 0) ,fx=0.25, fy=0.25)
        rgb_small_frame= small_frame[ : , : ,:: -1]
        if s:
                userid=""
                is_match, user_id = image.compare_faces_in_directory("./known_user/", unknown_user_dir) 
                if is_match:
                    face_names.append(user_id)
                    user_detail = db.get_user_detail(user_id)
                    user_detail_list.write(user_detail.__dict__)
                    userid=user_detail.id
                
                if userid in face_names:
                    if userid in students:
                        students.remove(userid)
                        print ("Attendance marked for user id: ", userid)
                        current_time = now.strftime("%H:%M:%S")
                        lnwrite.writerow(user_detail_list,current_time)
        # Display the results
        cv2.imshow('Attendence Capture', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

video_capture.release()
cv2.destroyAllWindows()
f.close()



