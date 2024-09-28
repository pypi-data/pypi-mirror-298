from setuptools import setup, find_packages

setup(
    name='clr-scrn',
    version='0.1.2',
    packages=find_packages(),
    description='A simple package to clear the terminal screen.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Suswin Palaniswamy',
    author_email='psuswin00@gmail.com',
    url='https://github.com/SIWNUS/clr-screen',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
