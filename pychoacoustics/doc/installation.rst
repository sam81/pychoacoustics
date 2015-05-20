.. _sec-installation:

*************
Installation
*************

.. todo::
   
   Add info on optional python packages (matplotlib and pandas).
   Add info on using scientific Python bundles, such as Anaconda.

``pychoacoustics`` has been successfully installed and used on Linux,
Windows, and Mac platforms. ``pychoacoustics`` depends on the installation of a
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

Currently there is no binary installer for `pychoacoustics`
on Windows. To use `pychoacoustics` on Windows you need to either
install Python and all the modules on which `pychoacoustics` depends
(PyQt4, numpy, scipy), or use a Python distribution such as Pyzo, which
includes python and the dependencies. Using Pyzo is currently the easiest
way to get `pychoacoustics` running quickly on Windows.

Install with Pyzo
~~~~~~~~~~~~~~~~~~~~~~~

Download the latest version on Pyzo and unpack it to a folder of your choice.
Download the Windows source package (PySide) of `pychoacoustics`. Open the DOS
command prompt and change directory to the folder where you unpacked PyZo, which 
should contain the `python.exe` executable. For example:

::

   cd C:\Users\audiolab\Desktop\pyzo2013c

once you're in the Pyzo folder, you can instruct the Pyzo Python interpreter
to run `pychoacoustics` by calling python.exe followed by the path where the `pychoacoustics`
main file is located. For example:

::
   
   python.exe "C:\Users\audiolab\Desktop\pychoacoustics-pyside-0.2.81\pychoacoustics.pyw"


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

    C:\Users\audiolab\Desktop\pyzo2013c\python.exe "C:\Users\audiolab\Desktop\pychoacoustics-pyside-0.2.81\pychoacoustics.pyw"
    %1 %2 %3 %4 %5 %6 %7 %8

You can place the ``.bat`` 
launcher wherever you want, for example on your ``Desktop`` folder. 
Simply double click on it, and ``pychoacoustics`` should start.

Installation on the Mac
------------------------

The easiest way to install ``pychoacoustics`` on the Mac is 
to use Pyzo as a Python distribution.
The steps are the same as for the installation with Pyzo on 
Windows (see above). Please, note that if you install with Pyzo you
will need to use the PySide version of ``pychoacoustics``.


Install Python and the Dependencies manually
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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





