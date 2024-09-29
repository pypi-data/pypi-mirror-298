from setuptools import setup, find_packages

setup(
    name='voyager_prime',
    version='0.1.0',
    packages=find_packages(),  # Automatically find and include all packages
    description='A simple but useful library for work with prime numbers',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Olaf Baca',
    author_email='olaf.baca@hotmail.com',
    url='https://github.com/yourusername/voyager_prime',  # Change to your repo link
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[],  # Add any dependencies here
)
