from flask import Flask, render_template, request, jsonify, send_from_directory, send_file
import streamlit as st
import imageio
import os
from model import *
import tensorflow as tf
from werkzeug.utils import secure_filename

st.set_page_config(layout='wide')
with st.sidebar:
    st.image('https://www.onepointltd.com/wp-content/uploads/2020/03/inno2.png')
    st.title('Lip to to speech converter')
    st.info('This application is originally developed from the LipNet deep learning model.')

image_file = st.file_uploader("you can upload a file here", type=['mp4','mpg'])
option = os.listdir(os.path.join('..', 'data', 's1'))
# print(option)
select_video = st.selectbox('choose video', option)
col1, col2 = st.columns(2)
if image_file is not None:
    select_video = image_file
    with open(os.path.join('..','data','s1', image_file.name), "wb") as f:
        f.write(image_file.getbuffer())
    with col1:
        st.info("The video below shows the seleted video in mp4 format \n file name: "+image_file.name)
        file_path = os.path.join('..','data','s1', image_file.name)
        os.system(f'ffmpeg -i {file_path} -vcodec libx264 test_video.mp4 -y')

        Video = open(file_path,'rb')
        video_bytes = Video.read()
        st.video(video_bytes)

    with col2:
            model = readLip(image_file.name)
            st.title("This is the predicted answer by the model")
            st.info("Answer: "+model)

else:
    if option:
        with col1:
            st.info("The video below shows the seleted video in mp4 format \n")
            file_path = os.path.join('..','data','s1', select_video)
            os.system(f'ffmpeg -i {file_path} -vcodec libx264 test_video.mp4 -y')

            Video = open(file_path,'rb')
            video_bytes = Video.read()
            st.video(video_bytes)
        with col2:
            model = str(readLip(select_video))
            st.text("This is the predicted answer by the model")
            st.info("Answer: "+model)
            
with open("./__temp__.mp4", "rb") as file:
    btn = st.download_button(
            label="click to download the __temp__.mp4",
            data=file,
            file_name="__temp__.mp4",
            mime="video/mp4"
          )