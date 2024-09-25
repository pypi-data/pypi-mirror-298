#!/usr/bin/env python
from setuptools import setup

setup(
    name='asciitoart',
    python_requires=">=3.9",
    version="0.1.1",
    description='Render Text as ascii art',
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Natural Language :: Japanese',
        'Natural Language :: Bulgarian',
        'Natural Language :: Bosnian',
        'Natural Language :: Macedonian',
        'Natural Language :: Russian',
        'Natural Language :: Serbian',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Fonts',
    ],
    author='James Miguel',
    url='https://github.com/0xJMiguel/asciitoart',
    packages=['asciitoart', 'asciitoart.fonts'],
    package_data={'asciitoart.fonts': ['*.flf', '*.flc']},
    entry_points={
        'console_scripts': [
            'asciitoart = asciitoart:main',
        ],
    }
)