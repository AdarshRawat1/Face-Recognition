import streamlit as st
import cv2 as cv
import numpy as np
import pandas as pd
from tempfile import NamedTemporaryFile
import os
import db
import image
import face_recognition as fr


# Assuming the functions save_image, delete_image, get_all_images, and compare_faces_in_directory are defined as provided
def attendence():
            st.title('Attendance System')
            uploaded_file = st.file_uploader("Choose a video file", type=['mp4', 'avi'])
            if uploaded_file is not None:
                tfile = NamedTemporaryFile(delete=False)
                tfile.write(uploaded_file.read())
                process_video(video_path=tfile.name)
                os.unlink(tfile.name)


def process_video(video_path=None):
        if video_path is None:
           raise ValueError("video_path must be provided")
        cap = cv.VideoCapture(video_path)

        frame_count = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
        fps = int(cap.get(cv.CAP_PROP_FPS))

        # Prepare a DataFrame to store attendance
        attendance_df = pd.DataFrame(columns=['User_ID', 'Attendance'])

        # Process each frame
        for i in range(frame_count):
            ret, frame = cap.read()
            if not ret:
                continue

            # Convert BGR to RGB for face_recognition
            rgb_frame = frame[:, :, ::-1]

            # Detect faces in the frame
            face_locations = fr.face_locations(rgb_frame)

            # For each face detected, save the cropped face as an image
            for top, right, bottom, left in face_locations:
                face_image = rgb_frame[top:bottom, left:right]
                unknown_user_dir = "./unknown_user/"
                unknown_user_name = f"unknown_{i}.jpg"
                image.save_image(face_image, unknown_user_dir, unknown_user_name)

                # Compare the saved face with known faces
                is_match, user_id = image.compare_faces_in_directory("./known_user/", unknown_user_dir)

                if is_match:
                    # Mark the user as present
                    attendance_df.loc[len(attendance_df)] = [user_id, 'Present']

                # Delete the temporary image
                image.delete_image(os.path.join(unknown_user_dir, unknown_user_name + ".jpg"))

        all_users = db.get_all_user_ids()  
        for user_id in all_users:
            if user_id not in attendance_df['User_ID'].values:
                attendance_df.loc[len(attendance_df)] = [user_id, 'Absent']

        # Save the attendance to a CSV file
        attendance_df.to_csv('attendance.csv', index=False)

        return attendance_df