.. vim: set fileencoding=utf-8 :
.. Gradiant's Biometrics Team <biometrics.support@gradiant.org>
.. Copyright (C) 2017 Gradiant, Vigo, Spain

.. _bob.gradiant.face.databases:

===========================
bob.gradiant.face.databases
===========================

.. todolist::

At present, this plugin provides support for the following databases:

* CASIA `[Paper 2012] <https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=6199754>`_.
* REPLAY-ATTACK `[Paper 2012] <https://www.idiap.ch/dataset/replayattack>`_.
* 3DMASK `[Paper 2013] <https://www.idiap.ch/dataset/3dmad>`_.
* MSU-MFSD `[Paper 2015] <https://www.cse.msu.edu/rgroups/biometrics/Publications/Databases/MSUMobileFaceSpoofing/index.htm>`_.
* UVAD `[Paper 2015] <https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=7017526&isnumber=7073680&tag=1>`_.
* REPLAY-MOBILE `[Paper 2016] <https://www.idiap.ch/dataset/replay-mobile>`_.
* HKBU `[Paper 2016] <http://rds.comp.hkbu.edu.hk/mars/>`_.
* OULU-NPU `[Paper 2017] <https://sites.google.com/site/oulunpudatabase/>`_.
* SMAD `[Paper 2017] <http://iab-rubric.org/papers/Manjani-DDLSpoofing.pdf>`_.
* ROSE_YOUTU `[Paper 2018] <http://rose1.ntu.edu.sg/Datasets/faceLivenessDetection.asp>`_.
* SIW `[Paper 2018] <http://cvlab.cse.msu.edu/spoof-in-the-wild-siw-face-anti-spoofing-database.html>`_.
* CSMAD `[Paper 2018] <http://publications.idiap.ch/downloads/papers/2018/Bhattacharjee_BTAS2018_2018.pdf>`_.


In addition, we propose a novel AggregateDatabase using all the data of the above datasets.


If you use this framework, please cite the following publication:

.. code-block::

    @INPROCEEDINGS{Costa-Pazo-ICB-2019,
        title = {Generalized Presentation Attack Detection: a face anti-spoofing evaluation proposal},
        author={Costa-Pazo, Artur and David Jim\'enez-Cabello and V\'azquez-Fern\'andez, Esteban and Alba-Castro, Jos\'e Luis and L\'opez-Sastre, Roberto J.},
        year = {2019},
        booktitle={The 12th IAPR International Conference On Biometrics (ICB)}
    }

To reproduce the research carried out in [Generalized Presentation Attack Detection: a face anti-spoofing evaluation proposal
](https://arxiv.org/abs/1904.06213) check the github package [bob.paper.icb2019.gradgpad](https://github.com/Gradiant/bob.paper.icb2019.gradgpad).


Useful entry_points
...................

Export database path from a filename:

.. code-block:: python

    bin/export_database_paths.py -f database_path.json

were database_path.json has to be as the code below:

.. code-block:: python


    {
        "CASIA": "/media/data/databases/BBDD/AntiSpoofing/CASIA_FASD/CBSR-Antispoofing",
        "REPLAY_ATTACK_PATH": "/media/data/databases/BBDD/AntiSpoofing/replay-attack/Movies",
        "THREEDMAD_PATH": "/media/data/databases/BBDD/AntiSpoofing/3DMAD/Data",
        "MSU_MFSD_PATH": "/media/data/databases/BBDD/AntiSpoofing/MSU_MFSD/MSU-MFSD/scene01",
        "UVAD_PATH": "/media/data/databases/BBDD/AntiSpoofing/UVAD",
        "REPLAY_MOBILE_PATH": "/media/data/databases/BBDD/AntiSpoofing/replay-mobile/database",
        "HKBU_PATH": "/media/data/databases/BBDD/AntiSpoofing/HKBU",
        "OULU_NPU_PATH": "/media/data/databases/BBDD/AntiSpoofing/OULU_NPU",
        "SMAD": "/media",
        "ROSE_YOUTU_PATH": "/media/data/databases/BBDD/AntiSpoofing/RoseYoutu2008",
        "SIW_PATH": "/media/data/databases/BBDD/AntiSpoofing/SiW",
        "CSMAD": "/media"
    }


Show useful info of parsed database with:

.. code-block:: python

    bin/face_databases_info.py


Save database labels with save_database_labels_info script:


.. code-block:: python

    usage: save_database_labels_info.py [-h] [-db DATABASE] [-f FILENAME]
                                        [-p PROTOCOL]

    optional arguments:
      -h, --help            show this help message and exit
      -db DATABASE, --database DATABASE
                            name of the database
      -f FILENAME, --filename FILENAME
                            output file (.pickle)
      -p PROTOCOL, --protocol PROTOCOL
                            name of the database default(grandtest)











Documentation
-------------

.. toctree::
   :maxdepth: 2

   py_api

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. include:: links.rst
