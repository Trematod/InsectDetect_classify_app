import streamlit as st
import subprocess
import os

# Stockage temporaire des projets
classification_results = {}

st.title("Image Classification and Metadata Processing")

# Classification Section
st.header("Step 1: Classify Images")
source = st.text_input("Source Folder (Path to Images)", "")
name = st.text_input("Project Name", "default_name")
weights = st.text_input("Weights File Path", "path_to_default_weights.onnx")
if st.button("Run Classification"):
    if not source:
        st.error("Source folder is required.")
    else:
        command = [
            'python3', '/Users/leslie/Desktop/yolov5-master/classify/predict.py',
            '--name', name,
            '--source', source,
            '--weights', weights,
            '--img', '128',
            '--sort-top1',
            '--sort-prob',
            '--concat-csv'
        ]
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            classification_results[name] = {
                "source": source,
                "path": f"yolov5-master/runs/predict-cls/{name}/results"  # chemin automatiquement généré
            }
            st.success("Classification completed successfully!")
            st.text(result.stdout)
        except subprocess.CalledProcessError as e:
            st.error("An error occurred during classification.")
            st.text(e.stderr)

# Processing Section
st.header("Step 2: Process Results")

# Option 1 : Laisser l'utilisateur donner le chemin vers les résultats
path_option = st.radio("Do you want to provide a custom path or use the project name?", ("Custom Path", "Use Project Name"))

if path_option == "Custom Path":
    custom_path = st.text_input("Custom Path to Classification Results", "")
    if st.button("Process Metadata with Custom Path"):
        if not custom_path:
            st.error("Please provide a valid custom path.")
        else:
            size = st.text_input("Size Parameters (e.g., 350 200)", "350 200")
            images = st.text_input("Images Parameters (e.g., 3 1800)", "3 1800")
            size_params = size.split()
            images_params = images.split()
            if len(size_params) != 2 or len(images_params) != 2:
                st.error("Invalid size or image parameters. Provide two values for each.")
            else:
                command = [
                    'python3', '/Users/leslie/Desktop/yolov5-master/process_metadata.py',
                    '-source', custom_path,
                    '-size', size_params[0], size_params[1],
                    '-images', images_params[0], images_params[1]
                ]
                try:
                    result = subprocess.run(command, capture_output=True, text=True, check=True)
                    st.success("Metadata processing completed successfully!")
                    st.text(result.stdout)
                except subprocess.CalledProcessError as e:
                    st.error("An error occurred while processing metadata.")
                    st.text(e.stderr)

# Option 2 : Utiliser le nom du projet pour construire le chemin automatiquement
if path_option == "Use Project Name":
    selected_project = st.selectbox("Select Project", list(classification_results.keys()))
    if st.button("Process Metadata with Project Name"):
        if not selected_project:
            st.error("Please select a project.")
        else:
            # Utilisation du nom pour créer le chemin vers les résultats
            source = classification_results[selected_project]["path"]
            size = st.text_input("Size Parameters (e.g., 350 200)", "350 200")
            images = st.text_input("Images Parameters (e.g., 3 1800)", "3 1800")
            size_params = size.split()
            images_params = images.split()
            if len(size_params) != 2 or len(images_params) != 2:
                st.error("Invalid size or image parameters. Provide two values for each.")
            else:
                command = [
                    'python3', '/Users/leslie/Desktop/yolov5-master/process_metadata.py',
                    '-source', source,
                    '-size', size_params[0], size_params[1],
                    '-images', images_params[0], images_params[1]
                ]
                try:
                    result = subprocess.run(command, capture_output=True, text=True, check=True)
                    st.success("Metadata processing completed successfully!")
                    st.text(result.stdout)
                except subprocess.CalledProcessError as e:
                    st.error("An error occurred while processing metadata.")
                    st.text(e.stderr)
