from setuptools import setup, find_packages
from UTN_Heroes_Dataset import VERSION

setup(
    name= 'UTN_Heroes_Dataset',
    version=VERSION,
    description= 'Set de datos con informacion de heroes y villanos para los desafios',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author= 'Facundo Falcone',
    author_email="ffalcone@fra.utn.edu.ar",
    packages= find_packages(),
    py_modules=['UTN_Heroes_Dataset'],
    requires=['setuptools', 'pygame'],
    include_package_data=True,
    package_data={
        'utn_assets': ['select.mp3'],
    },
    entry_points={
      'console_scripts': ['UTN_Heroes_Dataset=UTN_Heroes_Dataset.utn_funciones:saludo']  
    },
    script_name='UTN_Heroes_Dataset:saludo',
    keywords=['UTN_Heroes_Dataset', 'UTN-FRA'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11'
)