FROM conda/miniconda2:latest

MAINTAINER acosta@gradiant.org

RUN apt-get update && apt-get -y install git libopenblas-dev
ENV BUILD_NUMBER 0
RUN conda config --env --add channels defaults
RUN conda config --env --add channels https://www.idiap.ch/software/bob/conda
RUN conda install gitpython h5py pillow scikit-learn mock sphinx_rtd_theme bob.extension
RUN pip install enum34
