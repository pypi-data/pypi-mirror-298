from setuptools import find_packages, setup

with open("app/README.md", "r") as f:
    long_description = f.read()

setup(
    name="simtkinter",
    version="0.0.6",
    description="Makes the Tkinter simpler",
    package_dir={"": "app"},
    packages=find_packages(where="app"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://hacker-bin.com",
    author="George Langas",
    author_email="hackerakos@hacker-bin.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    install_requires=[""],
    #extras_require={
        #"dev": ["pytest>=7.0", "twine>=4.0.2"],
    #},
    python_requires=">=3.10",
)