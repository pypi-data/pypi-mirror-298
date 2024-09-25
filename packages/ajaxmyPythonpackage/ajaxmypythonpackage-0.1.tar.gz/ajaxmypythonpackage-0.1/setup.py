from setuptools import setup, find_packages

setup(
    name="ajaxmyPythonpackage",  # Replace with your package name
    version="0.1",
    description="A simple Python package",
    author="Ajit",
    author_email="ajitg@sigmoidanalytics.com",
    url="https://github.com/yourusername/myPythonpackage",  # Replace with your project URL
    packages=find_packages(),  # Automatically finds all packages inside the directory
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
