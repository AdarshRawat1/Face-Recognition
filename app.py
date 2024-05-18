import streamlit as st
import face_recognition as fr
import register
import login

registerTab, loginTab = st.tabs(["Register", "Login"])



with registerTab:
    register.register()
with loginTab:
    login.login()