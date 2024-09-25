from setuptools import setup, find_packages

setup(
    name='tintalib', 
    version='0.1',  
    packages=find_packages(), 
    install_requires=[],  
    author='Julio balladares',
    author_email='julio.balladares@icloud.com',
    description=(
        'tintalib is a Python library for adding text styling and colors to '
        'the terminal, supporting ANSI codes, RGB, and special effects like '
        'rainbow animations.'
    ),
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown', 
    url='https://github.com/managua48/tintalib', 
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Terminals',
        'Topic :: Utilities',
        'Topic :: System :: Logging',
        'Topic :: System :: Shells',
    ],
    python_requires='>=3.6',
)
