import os
import math
import tempfile
import cv2
import numpy as np
import streamlit as st
import base64
from datetime import datetime
import zipfile


def download_button(encoded, file_name):

    now = datetime.now()
    formatted_date_time = now.strftime("%Y-%m-%d_%H_%M_%S")

    st.markdown(
                    f"""
                    <a href="data:application/zip;base64,{encoded}" download="{file_name}_{formatted_date_time}.zip">
                        <h3>Download</h3>
                    </a>
                    """,
                    unsafe_allow_html=True,
                )


class TextToImage:

    def __init__(self, text_file):

        self.text_file = text_file
    

    def text_to_image(self):

        txt_file = self.text_file

        with tempfile.TemporaryDirectory() as temp_dir:

            with open(os.path.join(temp_dir, txt_file.name), "wb") as f:
                    f.write(txt_file.getbuffer())
            
            
            input_file = os.path.join(temp_dir, txt_file.name)
            
            with open(input_file, "rb") as f:
                data = f.read()

            image_size = len(data)
            image_dim = int(math.ceil(math.sqrt(image_size)))
            image_height = image_dim
            image_width = image_dim


            data += b"\x00" * (image_width * image_height - image_size)

            bin_file_loc = os.path.join(temp_dir, "padded_data.bin")

            with open(bin_file_loc, "wb") as f:
                f.write(data)
            
            image = np.zeros((image_height, image_width, 3), dtype=np.uint8)


            for i in range(image_size):
                row = i // image_width
                col = i % image_width
                image[row, col, 0] = data[i]
                image[row, col, 1] = data[i]
                image[row, col, 2] = data[i]

            image_output_loc = os.path.join(temp_dir, "output.png")
            cv2.imwrite(image_output_loc, image)

            st.image(image_output_loc)

            zip_path = os.path.join(temp_dir, "images.zip")
            with zipfile.ZipFile(zip_path, "w") as zip:
                zip.write(image_output_loc)

            with open(zip_path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode()
            
            download_button(encoded, file_name="txt-to-image")
    

    def image_to_text(self):

        txt_file = self.text_file
        
        with tempfile.TemporaryDirectory() as temp_dir:

            with open(os.path.join(temp_dir, txt_file.name), "wb") as f:
                    f.write(txt_file.getbuffer())

            input_file = os.path.join(temp_dir, txt_file.name)

            image = cv2.imread(input_file)

            data = bytearray()
            for row in range(image.shape[0]):
                for col in range(image.shape[1]):
                    pixel = image[row, col]
                    data.append(pixel[0])


            while data[-1] == 0:
                data.pop()

            output_data = data.decode('utf-8')

            text_output_loc = os.path.join(temp_dir, "output.txt")
            with open(text_output_loc, "w") as f:
                f.write(output_data)
            
            zip_path = os.path.join(temp_dir, "text.zip")
            with zipfile.ZipFile(zip_path, "w") as zip:
                zip.write(text_output_loc)

            with open(zip_path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode()
            
            download_button(encoded, file_name="image-to-text")