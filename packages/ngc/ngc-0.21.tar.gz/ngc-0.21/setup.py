from setuptools import setup, find_packages
import os

__version__ = '0.21' # version

lis=[]
for src in os.listdir(os.getcwd()+'/ngc'):
    if src.endswith('.py') and src[0]!='_':
        lis.append('ngc.'+src[:-3])
print(lis)

setup(name = 'ngc', 
    version = __version__,
    url='https://github.com/ngc5139/pyngc',
    author='NGC5139',
    description='Python New General Common Tool',
    long_description='# Python New General Common Tool\n\nA simple common py-tool mainly formed with easy functions for users who like to write small scripts, with less class and complex things.\n\nPlease use the newest version of python to use. It is being improved.\n\nIt use lambda in general. It includes functions of multi-regions like os as dirlist(traverse folder), IO, string operating, data struct operating and web operating.\n',
    long_description_content_type='text/markdown',
    author_email='cencrx@outlook.com',
    packages=find_packages(exclude=["tests"]),
    install_requires=['requests'],
    include_package_data=True,
    python_requires='>=3.8',
    py_modules = lis
)
