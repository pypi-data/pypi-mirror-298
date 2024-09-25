from setuptools import setup, find_packages

with open('README.md', 'r') as file:
    long_description = file.read()

setup(
    name='connor_nlp',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'docx==0.2.4',
        'nltk==3.9.1',
        'numpy==2.1.1',
        'odfpy==1.4.1',
        'openpyxl==3.1.5',
        'PyPDF2==3.0.1',
        'scikit_learn==1.5.2',
        'sentence_transformers==3.1.1',
    ],
    entry_points={
        'console_scripts': [
            'connor=cli.main:cli_main',
        ],
    },
    author='Yash',
    author_email='yg@ycatsh.net',
    description='Fast and fully local NLP file organizer that organizes files based on their content.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ycatsh/connor',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)