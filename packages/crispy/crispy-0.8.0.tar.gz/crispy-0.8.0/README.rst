Crispy is a modern graphical user interface to calculate core-level spectra
using the semi-empirical multiplet approaches implemented in `Quanty
<http://quanty.org>`_. The application provides tools to generate input files,
submit calculations, and plot the resulting spectra.

|release| |downloads| |DOI| |license|

.. |downloads| image:: https://img.shields.io/github/downloads/mretegan/crispy/total.svg
    :target: https://github.com/mretegan/crispy/releases

.. |release| image::  https://img.shields.io/github/release/mretegan/crispy.svg
    :target: https://github.com/mretegan/crispy/releases

.. |DOI| image:: https://zenodo.org/badge/doi/10.5281/zenodo.1008184.svg
    :target: https://dx.doi.org/10.5281/zenodo.1008184

.. |license| image:: https://img.shields.io/github/license/mretegan/crispy.svg
    :target: https://github.com/mretegan/crispy/blob/master/LICENSE.txt

.. first-marker

.. image:: https://raw.githubusercontent.com/mretegan/crispy/main/docs/assets/main_window.png

.. second-marker

Installation
============

Latest Release
--------------

**Using the Package Installers**

The easiest way to install Crispy on Windows and macOS operating systems is to
use the installers provided on the project's `downloads page
<http://www.esrf.eu/computing/scientific/crispy/downloads.html>`_.

**Using pip**

Pip is the package manager for Python, and before you can use it to install
Crispy, you have to make sure that you have a working Python distribution. On
macOS and Windows, you can install Python using the `official installers
<https://www.python.org/downloads>`_. In particular, for Windows, you should
install the 64-bit version of Python and make sure that you select to add
Python to the system's PATH during the installation.

.. code:: sh

    python3 -m pip install crispy

After the installation finishes, you should be able to start the program from
the command line:

.. code:: sh

    crispy

If you have problems running the previous command, it is probably due to not
having your PATH environment variable set correctly.

.. code:: sh

    export PATH=$HOME/.local/bin:$PATH


Development Version
-------------------

**Using pip**

Assuming that you have a working Python distribution (version 3.7 or greater),
you can easily install the development version of Crispy using pip:

.. code:: sh

    python3 -m pip install https://github.com/mretegan/crispy/tarball/main

To update the development version of Crispy, you can use the following command:

.. code:: sh

    python3 -m pip install --ignore-installed https://github.com/mretegan/crispy/tarball/main

.. third-marker

Usage
=====

.. forth-marker

Crispy should be easy to find and launch if you have used the installers. For
the installation using pip follow the instructions from the **Installation**
section.

.. fifth-marker

Citation
========
Crispy is a scientific software. If you use it for a scientific publication,
please cite the following reference (change the version number if required)::

    @misc{retegan_crispy,
      author       = {Retegan, Marius},
      title        = {Crispy: v0.8.0},
      year         = {2024},
      doi          = {10.5281/zenodo.1008184},
      url          = {https://dx.doi.org/10.5281/zenodo.1008184}
    }

.. sixth-marker

License
=======
The source code of Crispy is licensed under the MIT license.
