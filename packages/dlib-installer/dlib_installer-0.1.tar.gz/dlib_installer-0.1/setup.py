from setuptools import setup, find_packages

setup(
    name='dlib_installer',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    description='A package to install the correct version of dlib on Windows.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Ibrahim Aloui',
    author_email='ibrahimaloui433@gmail.com',
    url='https://github.com/yourusername/dlib_installer',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: Microsoft :: Windows',
    ],
    install_requires=[],  # No dependencies other than pip
)
