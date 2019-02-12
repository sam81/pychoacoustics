.. _sec-installation:

*************
Installation
*************

``pychoacoustics`` has been successfully installed and used on Linux,
Windows, and Mac platforms. Installation instructions for each operating system are
provided below.
    

Installation on Linux
=====================

For Debian and Ubuntu LTS releases there are apt repositories that can be used
to install and update ``pychoacoustics``. For other Linux distributions
``pychoacoustics`` has to be installed from source (see Section :ref:`sec-install_from_source`).

Installation on Debian
----------------------

Binary packages for the Debian amd64 architecture are hosted on
`bintray <https://bintray.com/sam81/hearinglab>`_.
To install ``pychoacoustics`` first install the ``apt-transport-https`` package if it is not already installed:

::
   
   sudo apt-get install apt-transport-https 

then add one of the following lines to ``/etc/apt/sources.list`` depending on your Debian version:
For Stretch (stable):

::

   deb https://dl.bintray.com/sam81/hearinglab stretch main


For Jessie (oldstable):

::

   deb https://dl.bintray.com/sam81/hearinglab jessie main

Download the key with which the repository is signed and add it to the apt keyring:

::

   wget -qO - https://bintray.com/user/downloadSubjectPublicKey?username=bintray | sudo apt-key add -

Refresh the package database and install the package:

::
   
   sudo apt-get update
   sudo apt-get install pychoacoustics

Installation on Ubuntu LTS Releases
-----------------------------------

Binary packages for Ubuntu Long Term Support (LTS) releases are hosted on
`Launchpad <https://launchpad.net/~samuele-carcagno/+archive/ubuntu/hearinglab>`_.
To install pychoacoustics run the following commands:

::

   sudo add-apt-repository ppa:samuele-carcagno/hearinglab
   sudo apt-get update
   sudo apt-get install pychoacoustics


Installation on Windows and MacOS
-----------------------

There are experimental binary installers for Windows and MacOS on the downloads page:

`http://samcarcagno.altervista.org/pychoacoustics/pychoacoustics.html <http://samcarcagno.altervista.org/pychoacoustics/pychoacoustics.html#downloads>`_

these are OK if you just want to try out pychoacoustics to see its look and feel. However, if you want to use pychoacoustics in research
it's recommended that for Windows and MacOS you install from source (see below). Producing the binaries for these OSs is time consuming, so the binary
installers may be updated less often with the latest bug fixes.

.. _sec-install_from_source:

Installation from source
-------------------------

``pychoacoustics`` depends on Python and a handful of Python modules.
There are two ways to obtain these dependencies. One is to install Python
and all the dependencies "manually" (that is one by one). The other (and easier)
way is to install a Python distribution that comes with a bundle of pre-installed
modules. These include:

- Anaconda: `https://www.continuum.io/downloads https://www.continuum.io/downloads>`_
  
- Pyzo: `http://www.pyzo.org/ <http://www.pyzo.org/>`_
    
- WinPython (Windows only): `http://winpython.github.io/ http://winpython.github.io/>`_

Step by step instructions to install ``pychoacoustics`` on Windows with WinPython are provided below.
Although these instructions are specific to Windows the installation steps are similar on Mac OS X
and Linux systems. If you get stuck at some point don't hesitate to get in touch <sam.carcagno@gmail.com>.

Install with WinPython on Windows
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Download the latest version on [WinPython](https://winpython.github.io/) and unpack it to a folder of your choice.
Download the Windows source package of `pychoacoustics`. Open the DOS
command prompt and change directory to the folder where you unpacked ``WinPython``, which 
should contain the `python.exe` executable. For example:

::

   cd C:\Users\audiolab\Desktop\WinPython

once you're in the WinPython folder, you can instruct the Pyzo Python interpreter
to run `pychoacoustics` by calling python.exe followed by the path where the `pychoacoustics`
main file is located. For example:

::
   
   python.exe "C:\Users\audiolab\Desktop\pychoacoustics-0.4.8\pychoacoustics.pyw"


Currently there is not an application launcher. There is, however, a file called
``pychoacoustics-launcher.bat`` inside the `scripts` folder of the source distribution of
`pychoacoustics` that after some modifications can be used as a launcher.
The content of the file is the following:

::

    C:\Python32\python "C:\Python32\site-packages\pychoacoustics.pyw" 
    %1 %2 %3 %4 %5 %6 %7 %8

The first statement ``C:\Python32\python`` is the path to the Python
executable. The second statement is the path to the main file of the
``pychoacoustics`` app. You simply need to replace those two statements
to reflect the Python installation on your system. Following the example 
above, you would change the contents of the file to:

::

    "C:\Users\audiolab\Desktop\WinPython\python.exe" "C:\Users\audiolab\Desktop\pychoacoustics-pyside-0.4.8\pychoacoustics.pyw"
    %1 %2 %3 %4 %5 %6 %7 %8

You can place the ``.bat`` 
launcher wherever you want, for example on your ``Desktop`` folder. 
Simply double click on it, and ``pychoacoustics`` should start.


"Manual" Installation from Source
---------------------------------

``pychoacoustics`` depends on the installation of a
handful of other Python modules:

-  Python (version 3) `http://www.python.org/ <http://www.python.org/>`_

-  numpy
   `http://sourceforge.net/projects/numpy/files/ <http://sourceforge.net/projects/numpy/files/>`_

-  scipy
   `http://sourceforge.net/projects/scipy/files/ <http://sourceforge.net/projects/scipy/files/>`_

additionally it is necessary to install one of the modules providing Python bindings to the Qt widgets toolkit.
There are three parallel versions of ``pychoacoustics`` that support the major
modules providing Python bindings to Qt (PyQt5, PyQt4, and PySide). You need to install only one
of these modules, and use the corresponding version of ``pychoacoustics``

- PyQt5
  `https://riverbankcomputing.com/software/pyqt/download5 <https://riverbankcomputing.com/software/pyqt/download5>`_
  
these programs need to be installed manually. Once these programs are
installed you can proceed with the installtion of ``pychoacoustics``:

::

    python3 setup.py install

you can then invoke ``pychoacoustics`` from a terminal by typing the
command

::

   pychoacoustics.pyw

There are two additional optional dependencies:

- matplotlib
  `http://matplotlib.org/ <http://matplotlib.org/>`_

- pandas
  `http://pandas.pydata.org/ <http://pandas.pydata.org/>`_
  
if matplotlib and pandas are installed pychoacoustics can generate graphical summaries
of the results of an experimental session.  



Install Python and the Dependencies manually on Windows
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Please, note that you will need Python version 3 or above to run `pychoacoustics`.

To install the dependencies, download them from their respective websites. 
Make sure that you pick versions compatible with your architecture (64 or 32 bits), 
and compatible with you Python version. 

After installing the dependencies, it is recommended to add the
directory where the Python executable resides to the system ``PATH``. In
this way you can call ``python`` from a ``DOS`` shell by simply typing
its name, rather than typing the full path to the Python executable.

By default ``python`` is installed in ``C:``. The name of the Python
directory depends on its version number, for example, if you installed
Python version 3.2, the python directory will be ``C:\Python32``. To add
this directory to the system path go to ``My Computer`` and click
``Properties``, then click ``Advanced System Settings``. In the
``System Properties`` window click ``Environment Variables``. There you
will find an entry called ``Path``. Select it and click ``Edit``. Be
careful not to remove any of the entries that are already written there
because it could corrupt your system. Simply append the name of the full
path of the folder where Python is installed, at the end of the
other entries.

To run ``pychoacoustics``, unpack the ``pychoacoustics``
``.zip`` file containing the source code. Open a ``DOS`` shell, ``cd`` to the directory
where you unzipped pychoacoustics and launch it with the following
command:

::

    python pychoacoustics.pyw


Currently there is not an application launcher. There is, however, a file called
``pychoacoustics-launcher.bat`` inside the `scripts` folder of the source distribution of
`pychoacoustics` that after some modifications can be used as a launcher.
The content of the file is the following:

::

    C:\Python32\python "C:\Python32\site-packages\pychoacoustics.pyw" 
    %1 %2 %3 %4 %5 %6 %7 %8

The first statement ``C:\Python32\python`` is the path to the Python
executable. The second statement is the path to the main file of the
``pychoacoustics`` app. You simply need to replace those two statements
to reflect the Python installation on your system. You can place the ``.bat`` 
launcher wherever you want, for example on your ``Desktop`` folder. 
Simply double click on it, and ``pychoacoustics`` should start.



