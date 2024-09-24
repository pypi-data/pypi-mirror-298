from setuptools import setup, find_packages
import os

# Read the contents of your README.md file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='flexible_scorer',
    version='0.1.14',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'openai',
        'plotly',
        'scipy',
    ],
    description='A flexible scoring library using OpenAI models.',
    long_description=long_description,  # Pass the README content here
    long_description_content_type='text/markdown',  # Specify the content type
    author='Michael',
    author_email='miryaboy@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Update based on your chosen license
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

