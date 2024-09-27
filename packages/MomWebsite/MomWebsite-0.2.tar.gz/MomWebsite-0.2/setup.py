from setuptools import setup, find_packages

setup(
    name="MomWebsite",
    version="0.2",
    description="A simple Python package to host a website without using Flask or external frameworks",
    author="Momwhyareyouhere",
    author_email="youremail@example.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],  # No external dependencies
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
