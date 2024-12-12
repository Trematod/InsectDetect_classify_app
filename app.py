import streamlit as st
import os
import subprocess
from pathlib import Path

# Titre de l'application
st.title("Classification d'Images avec YOLOv5")

# Choix du dossier d'images
folder = st.text_input("Entrez le chemin du dossier d'images")

# Bouton pour lancer la classification
if st.button("Classify Images"):
    if folder:
        # Vérification que le dossier existe
        if os.path.isdir(folder):
            st.write(f"Classification en cours sur le dossier: {folder}")
            
            # Commande pour exécuter le script de classification, tu peux adapter selon ton script
            try:
                result = subprocess.run(
                    ['python3', 'classify/predict.py', '--source', folder], 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE
                )
                if result.returncode == 0:
                    st.success("Classification terminée avec succès!")
                    st.write(result.stdout.decode())
                else:
                    st.error(f"Erreur: {result.stderr.decode()}")
            except Exception as e:
                st.error(f"Erreur lors de l'exécution du script: {str(e)}")
        else:
            st.error("Le dossier spécifié n'existe pas.")
    else:
        st.error("Veuillez spécifier un chemin valide.")

