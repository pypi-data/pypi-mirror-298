from setuptools import setup, find_packages

setup(
    name='useragent-generator',
    version='1.0.0',
    author='VampXD',
    author_email='bagasmuhammadriszki2@gmail.com',
    description='A library to generate random user agents for various platforms.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/VampXDH/useragent-generator',  # Ganti dengan URL repositori GitHub kamu
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
