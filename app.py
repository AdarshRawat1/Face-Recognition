import streamlit as st
import face_recognition as fr
import register
import login
import attendance

registerTab, loginTab, attendanceTab= st.tabs(["Register", "Login","Attendance"])


with registerTab:
    register.register()
with loginTab:
    login.login()
with attendanceTab:
    attendance.attendence()