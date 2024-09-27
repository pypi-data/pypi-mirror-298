from setuptools import setup, find_packages
import os

# Fonction pour récupérer les fichiers dans les sous-dossiers de manière récursive
def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            # Ajoute les fichiers avec leur chemin relatif
            paths.append(os.path.relpath(os.path.join(path, filename), directory))
    return paths

# Inclut tous les fichiers dans src/aait4all/gpt4all
binary_files = package_files('src/gpt4all-pypi-part2/gpt4all')


setup(
    name='gpt4all-pypi-part2',  # Nom du package
    version='0.0.1',
    description='Package with binary files and subfolders',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    package_data={
        'gpt4all-pypi-part1': binary_files,  # Inclut les fichiers binaires
    },
    include_package_data=True,
    install_requires=['gpt4all-pypi-part1',],
)