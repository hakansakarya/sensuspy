from setuptools import setup

setup(
   name='sensuspy',
   version='1.0',
   description='A module that helps with the retrieval and analysis of data collected via the Sensus app.',
   author='Sait Hakan Sakarya',
   author_email='shs5fh@virginia.edu',
   packages=['sensuspy'],
   install_requires=['geopy', 'gmplot', 'matplotlib', 'numpy', 'tzlocal', 'pandas', 'pycrypto'], #external packages as dependencies
)