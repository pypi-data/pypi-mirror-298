from setuptools import setup,find_packages

setup(
    name='ultimate-unit-converter',
    version='0.1.0',
    author='Nizarus.py',
    author_email='nizar.chawechy.1618@gmail.com',
    description='A package to convert units of distance, temperature, mass, and currency.',
    packages=find_packages(),
    install_requires = [
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