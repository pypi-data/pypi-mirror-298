from setuptools import setup, find_packages

setup(
    name='bourguiba',
    version='2.0.9',
    description='Generate shell commands based on natural language input using the T5 model',
    author='Si mohamed aziz bahloul wo chrikou il mangouli mehdi magroun ',
    author_email='azizbahloul3@gmail.com',
    packages=find_packages(),
    install_requires=[
        'transformers',  # Make sure you have the correct transformers version
        'torch',
        'sentencepiece',         # Needed for T5Tokenizer
    ],
    entry_points={
        'console_scripts': [
            'bourguiba=bourguiba.bourguiba:main',
        ],
    },
)
