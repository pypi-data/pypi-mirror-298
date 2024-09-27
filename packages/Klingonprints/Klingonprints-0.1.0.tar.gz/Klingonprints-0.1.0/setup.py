from setuptools import setup, find_packages

setup(
    name='Klingonprints',
    version='0.1.0',
    author='Ole Wegener',
    author_email='ole.wegener@aol.com',
    description='4 Theme options to change string appearance and option to translate to Klingon Language',
                
    packages=find_packages(),
    install_requires=[
        'requests',
        'string-color',
        "random"
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.0',
)