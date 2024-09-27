X-SOCS
======

The X-ray Strain Orientation Calculation Software (X-SOCS) is a user-friendly software,
developed for automatic analysis of 5D sets of data recorded during continuous mapping measurements.
X-SOCS aims at retrieving strain and tilt maps of nanostructures, films, surfaces or even embedded structures.

`Documentation <http://kmap.gitlab-pages.esrf.fr/xsocs>`_

Installation
------------

X-SOCS runs on Linux, Windows and macOS with `Python <https://www.python.org/>`_ >=3.8 and can be installed with::

    pip install xsocs[gui]

or with conda::

    conda install -c conda-forge xsocs

See `How to install XSocs <http://kmap.gitlab-pages.esrf.fr/xsocs/install.html>`_ for details.

Using XSOCS
------------

Once installed, you can run X-SOCS from the console with either::

    xsocs

Or::

    python -m xsocs

See `Using X-Socs documentation <http://kmap.gitlab-pages.esrf.fr/xsocs/using.html>`_ and
the `video tutorials <http://kmap.gitlab-pages.esrf.fr/xsocs/tutorials.html>`_.

License
-------

The source code of X-SOCS is licensed under the `MIT license <https://gitlab.esrf.fr/kmap/xsocs/blob/main/LICENSE>`_.

References
----------

X-SOCS can be referred by its DOI on Zenodo: |zenodo DOI|

.. |zenodo DOI| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.10777448.svg
  :target: https://doi.org/10.5281/zenodo.10777448

Reference publication:

Chahine, G. A., Richard, M.-I., Homs-Regojo, R. A., Tran-Caliste, T. N., Carbone, D., Jacques, V. L. R., Grifone, R., Boesecke, P., Katzer, J., Costina, I., Djazouli, H., Schroeder, T. & Schulli, T. U. *"Imaging of strain and lattice orientation by quick scanning X-ray microscopy combined with three-dimensional reciprocal space mapping."* `J. Appl. Cryst. (2014) 47, 762-769. <https://doi.org/10.1107/S1600576714004506>`_
