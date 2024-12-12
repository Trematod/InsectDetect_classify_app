import streamlit as st
import subprocess
import os

# Fonction principale de l'application Streamlit
def main():
    st.title("Traitement des Métadonnées avec Streamlit")

    # Saisie du chemin d'accès pour le dossier source
    source = st.text_input("Dossier source", "yolov5-master/runs/predict-cls/<NAME>/results")

    # Saisie des dimensions (taille de l'image)
    size_width = st.number_input("Largeur de l'image", min_value=1, value=350)
    size_height = st.number_input("Hauteur de l'image", min_value=1, value=200)

    # Saisie du nombre d'images (images de début et fin)
    start_image = st.number_input("Image de début", min_value=1, value=3)
    end_image = st.number_input("Image de fin", min_value=1, value=1800)

    # Bouton pour exécuter la commande
    if st.button("Lancer le traitement"):
        if source:
            try:
                # Construire la commande
                command = [
                    "python", "/Users/leslie/Desktop/yolov5-master/process_metadata.py",
                    "-source", source,
                    "-size", str(size_width), str(size_height),
                    "-images", str(start_image), str(end_image)
                ]
                
                # Afficher la commande pour information
                st.write("Commande exécutée :", " ".join(command))

                # Exécuter la commande
                result = subprocess.run(command, capture_output=True, text=True)
                
                # Vérifier les résultats de l'exécution
                if result.returncode == 0:
                    st.success("Traitement terminé avec succès !")
                    st.text(result.stdout)
                else:
                    st.error("Erreur lors de l'exécution de la commande.")
                    st.text(result.stderr)
            
            except Exception as e:
                st.error(f"Une erreur est survenue : {e}")
        else:
            st.error("Veuillez spécifier un dossier source.")

if __name__ == "__main__":
    main()
