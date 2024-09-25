from setuptools import setup, find_packages

setup(
    name="pclearn",  # Package name changed to pclearn
    version="0.2",
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
        'pclearn': ['ai.py'],  # Ensure 'ai.py' is included in the package
    },
    entry_points={
        'console_scripts': [
            'create-folder=pclearn:create_folder_with_pyfile',  # Add this to make the function executable from CLI
        ],
    },
)
