from setuptools import setup, find_packages

setup(
    name='pyndas',
    version='0.0.4',
    packages=['pyndas'], # 
    install_requires=['pymongo','time'],  # Tambahkan dependencies yang diperlukan
    author='Mfaidiq',
    author_email='faisalsidiq14@gmail.com',
    description='Library for MongoDB data transformation and redundancy removal',
    url="https://github.com/mfaisal-Ash/pyndas",
    download_url='https://github.com/mfaisal-Ash/pyndas/archive/refs/tags/v0.0.4.tar.gz',
    keywords = ['pyndas','py-ndas'],  
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
    'Programming Language :: Python :: 3.11',
    'Programming Language :: Python :: 3.12',
    ],
)
