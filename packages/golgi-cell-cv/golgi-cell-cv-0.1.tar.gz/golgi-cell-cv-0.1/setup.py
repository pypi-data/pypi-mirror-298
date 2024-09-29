from setuptools import find_packages, setup

setup(
    name="golgi-cell-cv",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir= {"": "src"},
    package_data= {"": ["*/.gitkeep"]},
    description="description",
    url="https://github.com/AndKaminer/golgi",
    author="Andrew Kaminer",
    author_email="akaminer@gatech.edu",
    install_requires=[
        'opencv-python',
        'numpy',
        'roboflow',
        'easygui',
        'huggingface_hub',
        'ultralytics',
        'diplib'
    ]
)
