from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="nexusfm",
    version="0.4.0",
    author="Jahid Hasan",
    author_email="engjahidhasan20@gmail.com",
    description="An advanced personalized file manager with GUI and terminal interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jhasanlinix/nexusfm",
    packages=find_packages(),
    install_requires=[
        "PyQt5",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "nexusfm-gui=nexusfm.gui:main",
        ],
    },
)