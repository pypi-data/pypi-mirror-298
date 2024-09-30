from setuptools import setup, find_packages

setup(
    name='Abs_package',  
    version='0.0.1',  # Increment version for the new release
    packages=find_packages(),  # Automatically finds all packages
    install_requires=[],  # Add any external dependencies if needed
    description='A Streamlit-based application to compute Harmonic Abstraction and Rouge Complement Abstraction a formula based approch',  
    long_description=open('README.md').read(),  # Detailed description from your README file
    long_description_content_type='text/markdown',  # Specify that the README is in Markdown
    author='Praveen K',
    url='https://github.com/katweNLP/AbstractionStudy/abs_package',  
    project_urls={  
        'Documentation': 'https://drive.google.com/file/d/1_tnkzaMYOuFWWf31OdYjldfZG1XSdkcb/view?usp=sharing',
        'Source': 'https://github.com/katweNLP/AbstractionStudy',
        'Research Paper': 'https://drive.google.com/file/d/1_tnkzaMYOuFWWf31OdYjldfZG1XSdkcb/view?usp=sharing',  
    },
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',  # Your license
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',  # Minimum Python version requirement
)
