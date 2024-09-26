from setuptools import setup, find_packages

setup(
    name='pyndas',
    version='0.0.2',
    packages=find_packages(),  # Pastikan ini sesuai dengan direktori yang ada
    install_requires=['pymongo'],  # Tambahkan dependencies yang diperlukan
    description='Library for MongoDB data transformation and redundancy removal',
    author='Mfaidiq',
    url="https://github.com/mfaisal-Ash/pyndas",
    download_url = '',  
    classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Programming Language :: Python :: 3.12',
    ],
    entry_points={
        "console-scripts":[
            "pyndas = pyndas.__init__:init",

        ],
    },
)
