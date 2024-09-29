from setuptools import setup, find_packages

setup(
    name="toretools",
    version="0.1.1",
    author="Torrez Tsoi",
    author_email="that1.stinkyarmpits@gmail.com",
    description="Useful functions and classes for creating mathematical or scientific programs!",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=["echowave", "yt_dlp", "random"],
    include_package_data=True,
)
