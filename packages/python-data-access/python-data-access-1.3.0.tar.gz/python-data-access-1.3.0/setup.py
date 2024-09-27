from setuptools import setup
import os


def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as file:
        return file.read()


setup(
    name='python-data-access',
    version='1.3.0',
    description='Lightweight and fast database access layer with query builder for MySQL and SQLite databases',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    url='https://github.com/expandmade-tb/python-data-access',
    author='tbednarek',
    author_email='thomas.bednarek@expandmade.com',
    license='MIT',
    packages=['easydb'],
    install_requires=['mysql.connector',
                      ],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux', 
        'Programming Language :: Python :: 3.10',
    ],
)
