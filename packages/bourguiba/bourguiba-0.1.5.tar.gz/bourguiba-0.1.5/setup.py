from setuptools import setup, find_packages

setup(
    name='bourguiba',
    version='0.1.5',
    description='A Python library to generate commands based on descriptions using T5',
    author='si mohamed aziz bahloul wo chrikou si mahdi magroun',
    author_email='azizbahloul3@gmail.com',
    packages=find_packages(),
    install_requires=[
        'torch',
        'transformers',
        'sentencepiece'
    ],
    entry_points={
        'console_scripts': [
            'bourguiba=bourguiba.bourguiba:main',
        ],
    },
    include_package_data=True,
)
