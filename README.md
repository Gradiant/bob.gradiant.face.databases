# bob.gradiant.face.databases 

[Bob](https://www.idiap.ch/software/bob/) package (python) which defines databases protocols. This repository does not include data from the databases, these must be requested from the entities responsible for them.


## Environment

We strongly recommend to use [conda](https://conda.io/docs/) to manage the project environment.

There is available two shared recipes to create the enviroment for this project on anaconda cloud.

*Linux*
~~~
conda env create gradiant/biometrics_py27
~~~

*Mac Os*
~~~
conda env create gradiant/biometrics_mac_py27
~~~

If you prefer to install the environment from yaml files:

*Linux*
~~~
conda env create -f environments/biometrics_ubuntu_py27.yml
~~~

*Mac Os*
~~~
conda env create -f environments/biometrics_mac_py27.yml
~~~


## Installation

We assume you have activate biometrics_py27 (or biometrics_mac_py27) environment 

~~~
source activate biometrics_py27
~~~

Then, you can buildout the project with:

~~~
  cd bob.gradiant.face.databases 
  python bootstrap-buildout.py
  bin/buildout
~~~

## Test

~~~
  bin/nosetests -v
~~~

Note that if we do not export the environment variables with the database paths, most tests will be skipped.

## Clean

~~~
  python clean.py
~~~

## Coverage

~~~  
  bin/coverage run -m unittest discover
  bin/coverage html -i
  bin/coverage xml -i
~~~

Coverage result will be store on htmlcov/.

## Doc

~~~
bin/sphinx-build -b html doc/ doc/html/
~~~
