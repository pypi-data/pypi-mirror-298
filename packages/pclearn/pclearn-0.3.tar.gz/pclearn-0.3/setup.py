from setuptools import setup, find_packages

setup(
    name="pclearn",  # Package name
    version="0.3",
    packages=find_packages(),  # Automatically find and include all packages in this directory
    description="A package to create folders and store .py files",
    author="jerrry",
    author_email="jerryjones23@gmail.com",
    python_requires='>=3.6',  # Specify the required Python version
    install_requires=[],  # List your package dependencies here if any
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={
        'pclearn': ['*.py'],  # Include all .py files in the package
    },
    entry_points={
        'console_scripts': [
            'build-folder=pclearn:build',  # Make the function executable from CLI
        ],
    },
)
