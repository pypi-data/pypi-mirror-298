from setuptools import setup, find_packages

setup(
    name="Boyoke_Encok",
    version="0.1.2",
    description="Auto claim",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    author="Shairul alim",
    author_email="shairulalim644@gmail.com",
    packages=find_packages(),
    install_requires=[
        "colorama",
        "requests",
        "brotli",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
