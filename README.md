# bob.gradiant.face.databases [![Build Status](https://travis-ci.org/Gradiant/bob.gradiant.pipelines.svg?branch=master)](https://travis-ci.org/Gradiant/bob.gradiant.face.databases) [![Doc](http://img.shields.io/badge/docs-latest-orange.svg)](https://gradiant.github.io/bob.gradiant.face.databases/)




[Bob](https://www.idiap.ch/software/bob/) package (python) which defines databases protocols. This repository does not include data from the databases, these must be requested from the entities responsible for them.


## Docker 

The fastest way to contact the package is to use docker. 

You can download the docker image from dockerhub

~~~
docker pull acostapazo/bob.gradiant:latest 
~~~

or build it from Dockerfile

~~~
docker build --no-cache -t acostapazo/bob.gradiant:latest  .
~~~

To check if everything is alright you can run the ci.sh script with:

~~~
docker run -v $(pwd):/bob.gradiant.face.databases acostapazo/bob.gradiant:latest bin/bash -c "source activate bob.gradiant; cd bob.gradiant.face.databases; ./ci.sh"
~~~


## Installation (Manual)


1. Install conda -> https://conda.io/docs/user-guide/install/index.html

2. Create the conda env

~~~
    conda env create -f envs/ubuntu_environment.yml
~~~

or if run this in macosx platform

~~~
    conda env create -f envs/mac_environment.yml
~~~

3. Activate the environment and add some channels

~~~
   source activate bob.gradiant
~~~


## Test

~~~
  bin/nosetests -v
~~~

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
