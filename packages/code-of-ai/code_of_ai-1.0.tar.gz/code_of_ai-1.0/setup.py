# setup.py

from setuptools import setup, find_packages

setup(
    name='code_of_ai',           # Package name
    version='1.0',                    # Package version
    packages=find_packages(),         # Automatically find packages in the directory
    description='all codes available',
    author='SY IT',            # Your name
    author_email='your_email@example.com',  # Your email
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',          # Python version compatibility
)
