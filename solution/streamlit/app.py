import streamlit as st
import os
import json

from model_inference import process_video
import shutil


def move_files_to_parent_folder(root_folder):
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                shutil.move(file_path, os.path.join(root_folder, file))
            except:
                print('fail')

DATA_FILE = 'data.json'

UPLOAD_FOLDER = 'input_data'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return []


def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)


def add_data(name, file_path, output_path):
    data = load_data()
    data.append({'name': name, 'file': file_path, 'output': output_path})
    save_data(data)


st.set_page_config(page_title="Scooter Tracking App", layout='wide')
if 'page' not in st.session_state:
    st.session_state.page = 'Tracking'

def go_to_tracking():
    st.session_state.page = 'Tracking'


def go_to_examples():
    st.session_state.page = 'Examples'


st.sidebar.title("Menu")
tracking_button = st.sidebar.button('Tracking', on_click=go_to_tracking)
examples_button = st.sidebar.button('Examples', on_click=go_to_examples)

if st.session_state.page == 'Tracking':
    st.header("Tracking")

    with st.form("track_form"):
        name = st.text_input("Enter the name:")
        uploaded_file = st.file_uploader("Upload a video file:", type=["mp4", "avi", "mov"])
        submit_button = st.form_submit_button(label='Track')

        if submit_button and name and uploaded_file:
            file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
            with open(file_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())

            output_path = process_video(file_path, uploaded_file.name, name)
            output_path = output_path[:-4] + '.avi'
            move_files_to_parent_folder('output_data')
            add_data(name, file_path, output_path)

            st.success(f"Added {name} with file {uploaded_file.name}")

elif st.session_state.page == 'Examples':
    st.header("Examples")

    data = load_data()

    if data:
        try:
            for item in data:
                file_name = os.path.basename(item['output'])
                with open(item['output'], 'rb') as file:
                    st.download_button(
                        label=f"Download {item['name']}",
                        data=file,
                        file_name=file_name,
                        mime="application/octet-stream"
                    )
        except:
            st.info("No examples available.")
    else:
        st.info("No examples available.")

st.markdown(
    """
    <style>
    body {
        background-color: white;
        color: black;
    }
    </style>
    """,
    unsafe_allow_html=True
)
