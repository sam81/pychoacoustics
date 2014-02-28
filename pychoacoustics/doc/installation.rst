.. _sec-installation:

*************
Installation
*************

``pychoacoustics`` has been successfully installed and used on Linux and
Windows platforms. Given that it is entirely written in Python, it should be
fully cross-platform and should work on the Mac as well, but this has
never been tested. ``pychoacoustics`` depends on the installation of a
handful of other programs:

-  Python (version 3) `http://www.python.org/ <http://www.python.org/>`_

-  pyqt4
   `http://www.riverbankcomputing.co.uk/software/pyqt/download <http://www.riverbankcomputing.co.uk/software/pyqt/download>`_

-  numpy
   `http://sourceforge.net/projects/numpy/files/ <http://sourceforge.net/projects/numpy/files/>`_

-  scipy
   `http://sourceforge.net/projects/scipy/files/ <http://sourceforge.net/projects/scipy/files/>`_

these programs need to be installed manually. Once these programs are
installed you can proceed with the installtion of ``pychoacoustics``.

Installation on Linux
---------------------

Binary deb packages for Debian are provided (starting from Wheezy), 
and can be installed using gdebi which automatically handles dependencies. 
For other linux systems, once all of
the dependencies have been installed, ``pychoacoustics`` can be
installed as a standard python package using

::

    sudo python3 setup.py install

you can then invoke ``pychoacoustics`` from a terminal by typing the
command

::

    pychoacoustics.pyw

Installation on Windows
-----------------------

Using the binary installer
~~~~~~~~~~~~~~~~~~~~~~~~~~

After installing the dependencies (``python``, ``pyqt4``, ``numpy``, and
``scipy``), simply double click on the ``pychoacoustics`` windows
installer to start the installation procedure. Currently the installer
does not provide an application launcher. There is, however, a file called
``pychoacoustics-qt4.bat`` inside the source distribution of
pychoacoustics that after some modifications can be used as a launcher.
The content of the file is the following:

::

    C:\Python32\python "C:\Python32\site-packages\pychoacoustics.pyw" 
    %1 %2 %3 %4 %5 %6 %7 %8

The first statement ``C:\Python32\python`` is the path to the Python
executable. The second statement is the path to the main file of the
``pychoacoustics`` app. You simply need to replace those two statements
to reflect the Python installation on your system. You can place the ``.bat`` launcher wherever you want, for example on your ``Desktop`` folder. Simply double click on it, and ``pychoacoustics`` should start.

Installing from source
~~~~~~~~~~~~~~~~~~~~~~

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

To install ``pychoacoustics`` from source, unpack the ``pychoacoustics``
``.zip`` file containing the source code. Open a ``DOS`` shell and
``cd`` to the directory where you unzipped pychoacoustics. The program
can then be installed as a standard python package using the following
command:

::

    python setup.py install

If you have installed the dependencies, you can also use pychoacoustics
without installing it. Open a ``DOS`` shell, ``cd`` to the directory
where you unzipped pychoacoustics and launch it with the following
command:

::

    python pychoacoustics.pyw

As mentioned in the previous section, there is also a ``.bat`` launcher
that can be used to launch ``pychoacoustics`` without needing to open a
``DOS`` shell each time. You can read the previous section for further
info.
