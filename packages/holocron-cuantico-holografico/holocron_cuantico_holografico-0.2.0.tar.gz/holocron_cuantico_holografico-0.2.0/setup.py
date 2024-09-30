from setuptools import setup, find_packages

setup(
    name='holocron_cuantico_holografico',  # Nombre del paquete en PyPI
    version='0.2.0',  # Versión del paquete
    author='Adolfo González Hernández',
    author_email='adolfogonzal@gmail.com',
    description='Una librería para simular el Holocron Cuántico Holográfico',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Alphonsus411/holocron_cuantico',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy',
        'matplotlib',
    ],
)
