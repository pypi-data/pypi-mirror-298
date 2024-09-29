
from setuptools import setup

setup(
    name="pytextpopup",
    version="0.1.0",
    author="Andrew Goetz",
    author_email="erax0r@gmail.com",
    description="A Python package that displays floating text windows on the screen at the cursor's position. The text can be customized with different fonts, colors, and scroll speeds.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/erax0r/pytextpopup",
    packages=[""],
    install_requires=['screeninfo'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
