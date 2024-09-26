from setuptools import setup, find_packages

setup(
    name='very-cool-converter100',
    version='0.2.0',
    author='Your Name',
    author_email='your_email@example.com',
    description='A package to convert units of distance, temperature, mass, and currency.',
    packages=find_packages(),
    install_requires=[
        'requests',
        'string-color'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)