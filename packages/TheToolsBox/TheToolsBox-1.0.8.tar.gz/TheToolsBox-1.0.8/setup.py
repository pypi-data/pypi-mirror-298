from setuptools import setup, find_packages

setup(
    name="TheToolsBox",  # Nom de la librairie
    version="1.0.8",  # Version de la librairie
    description="Description de ma librairie",  # Courte description
    long_description=open('README.md').read(),  # Description plus complète venant du fichier README
    long_description_content_type='text/markdown',  # Type de contenu pour le long_description
    author="Vectra",  # Nom de l'auteur
    author_email="Jarvis.noxingcorporation@gmail.com",  # E-mail de l'auteur
    url="https://github.com/VectraNoxCorp/TheToolsBox",  # URL vers ton dépôt ou ta page d'accueil
    packages=find_packages(),  # Trouve tous les sous-packages à inclure
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],  # Métadonnées pour l'identification du package
    python_requires='>=3.6',  # Version minimale de Python
    install_requires=[
        "python-docx",  # Liste des dépendances à installer
        "openpyxl",
        "gtts",
        "requests",
        "time",
        "psutil"
    ],
    include_package_data=True,  # Inclure les fichiers de données spécifiés dans MANIFEST.in
)
