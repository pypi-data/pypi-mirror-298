from setuptools import setup, find_packages

setup(
    name='maze-generator-jotbleach',
    version='1.1.0',
    description='A Python library for generating and visualizing mazes with custom properties.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='JotBleach',
    author_email='jotbleach@gmail.com',
    url='https://github.com/JotBleach/maze_generator',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'matplotlib'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
