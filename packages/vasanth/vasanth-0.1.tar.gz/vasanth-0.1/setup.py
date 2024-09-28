from setuptools import setup, find_packages

setup(
    name='vasanth',  # Package name
    version='0.1',  # Initial release version
    description='A simple module that provides math functions and machine learning algorithms',
    author='Vasantha Raj',
    author_email='vasanthraj679@gmail.com',
    packages=find_packages(),  # Automatically find packages in the project
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
