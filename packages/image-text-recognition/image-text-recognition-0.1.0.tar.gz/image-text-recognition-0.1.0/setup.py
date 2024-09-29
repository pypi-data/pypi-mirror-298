from setuptools import setup, find_packages

setup(
    name="image-text-recognition",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "easyocr",
        "numpy",
        "Pillow",
        "opencv-python",
        "scikit-learn",
    ],
    author="Amit Acharya",
    author_email="amitjagadeesh2004@gmail.com",
    description="A package for recognizing and evaluating text in images",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)