from setuptools import setup, find_packages

setup(
    name='tintapy',
    version='0.1.1',
    description='A package that provides tools for applying text styles and color customization in the terminal using ANSI sequences.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='managua48',
    author_email='julio.balladares@icloud.com',
    url='https://github.com/managua48/tintapy',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
