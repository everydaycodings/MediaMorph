import streamlit as st
from helper import TextToImage

st.title("Welcome To MediaMorph")


choice = st.selectbox("Which function do you want to choose: ", options=["Text To Image", "Image To Text"])

if choice == "Text To Image":
    file_upload = st.file_uploader("Choose a txt File: ", type=["txt"])
elif choice == "Image To Text":
    file_upload = st.file_uploader("Choose a png File: ", type=["png"])

if file_upload is not None:

    if choice == "Text To Image":
        if st.button("Convert It to Image"):
            TextToImage(file_upload).text_to_image()
    
    elif choice == "Image To Text":
        TextToImage(file_upload).image_to_text()