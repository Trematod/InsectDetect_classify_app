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
predict_script_path = st.text_input("Path to predict.py", "/Users/leslie/Desktop/yolov5-master/classify/predict.py")  # Demande du chemin vers predict.py

if st.button("Run Classification"):
    if not source:
        st.error("Source folder is required.")
    elif not predict_script_path:  # Vérification que le chemin vers predict.py est fourni
        st.error("Path to predict.py is required.")
    else:
        command = [
            'python3', predict_script_path,  # Utilise le chemin fourni par l'utilisateur
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

# Demander le chemin de process_metadata.py
process_script_path = st.text_input("Path to process_metadata.py", "/Users/leslie/Desktop/yolov5-master/process_metadata.py")

# Option 1 : Laisser l'utilisateur donner le chemin vers les résultats
path_option = st.radio("Do you want to provide a custom path or use the project name?", ("Custom Path", "Use Project Name"))

# Afficher les champs de paramètres de taille et d'images avant l'action de bouton
size = st.text_input("Size Parameters (e.g., 350 200)", "350 200")
images = st.text_input("Images Parameters (e.g., 3 1800)", "3 1800")
size_params = size.split()
images_params = images.split()

# Validation des paramètres
if len(size_params) != 2 or len(images_params) != 2:
    st.error("Invalid size or image parameters. Provide two values for each.")
else:
    if path_option == "Custom Path":
        custom_path = st.text_input("Custom Path to Classification Results", "")
        if st.button("Process Metadata with Custom Path"):
            if not custom_path:
                st.error("Please provide a valid custom path.")
            elif not process_script_path:  # Vérification du chemin vers process_metadata.py
                st.error("Path to process_metadata.py is required.")
            else:
                command = [
                    'python3', process_script_path,  # Utilise le chemin fourni par l'utilisateur
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
            elif not process_script_path:  # Vérification du chemin vers process_metadata.py
                st.error("Path to process_metadata.py is required.")
            else:
                # Utilisation du nom pour créer le chemin vers les résultats
                source = classification_results[selected_project]["path"]
                command = [
                    'python3', process_script_path,  # Utilise le chemin fourni par l'utilisateur
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


