# sensuspy
A Python package that provides utilities when working with data collected via the Sensus app.

## Getting Started

###   Prerequisites
sensuspy requires the AWS Command Line Interface to be installed in order to synchronise data from a S3 bucket. In order to install AWS CLI see http://docs.aws.amazon.com/cli/latest/userguide/installing.html

###   Installing
The package was developed using python 3.5, however it should be compatible with any python 3.x. Testing on python 3.6 yielded no unexpected behavior, but using python 3.5 is advised for optimal behavior. Working with a virtual environment is also advised.

In order to setup a virual environment (using anaconda):
```
conda create -n yourenvname python=3.5
```
To activate your virtual environment:
```
source activate yourenvname
```
Required packages can be easily installed within the virual environment using pip with:
```
pip install -r requirements.txt
```
After you are confident the requirements are satisfied just run:
```
Python3.5 setup.py install
```
If setup is successful sensuspy should be available as a package and you can import it with:
```
import sensuspy as sp
```

## Usage
Sensuspy relies heavily on pandas. The main data structures used include pandas dataframes and pandas series, with a dictionary containing these structures as its values depending on the occasion. Users can carry out operations specific to pandas and are therefore not limited to the functions available in this package.
