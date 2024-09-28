from setuptools import setup, find_packages

setup(
    name='Abs_package',  
    version='0.1.1',  # Initial version
    packages=find_packages(),  # Automatically finds all packages
    install_requires=[],  # Add external dependencies here
    description='',
    author='Praveen',
    author_email='',
    url='',  # Your package repository URL
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',  # Your license
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',  # Minimum Python version requirement
)
