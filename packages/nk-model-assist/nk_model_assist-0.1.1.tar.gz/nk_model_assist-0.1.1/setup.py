from setuptools import setup, find_packages

setup(
    name='nk_model_assist',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'pandas',  # Add other dependencies here
    ],
    author='Nithesh Kumar',
    author_email='nitheshmanimaran@example.com',
    description='This is a package to assist with model training and evaluation.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/nk-modelling',  # Update with your repo URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)