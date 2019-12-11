import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="find-the-scroll",
    version="0.0.1",
    author="Martin Wustinger",
    author_email="mwustinger@student.tgm.ac.at",
    description="Find the Scroll",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mwustinger-tgm/sew5-ek1-find-the-scroll.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)