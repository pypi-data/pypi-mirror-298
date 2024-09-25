from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="image_processing_alisson",
    version="0.0.1",
    author="Alisson",
    description="Image Processing Package using Skimage",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alissonwr/Desafios_Ntt_Data_Dio/tree/1bfc7e799f6ae9519bec3bf8c668cda0931e30ec/image-processing-package",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.5',
)