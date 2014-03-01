****************************
What is ``pychoacoustics``?
****************************

``pychoacoustics`` is a software for programming and running experiments 
in auditory psychophysics (psychoacoustics). The software contains a set 
of predefined experiments that can be immediately run after installation. 
Importantly, ``pychoacoustics`` is designed to be extensible so that users 
can add new custom experiments with relative ease. Custom experiments are 
written in Python, a programming language renowned for its clarity and 
ease of use. The application is divided in two graphical windows 
a) the “response box”, shown in Figure :ref:`fig-response_box`, with 
which listeners interact during the experiment b) the control window, 
shown in Figure :ref:`fig-control_window`, that contains a series of 
widgets (choosers, text field and buttons) that are used by the experimenter 
to set all of the relevant experimental parameters which can also be stored 
and later reloaded into the application. 

.. _fig-response_box:

.. figure:: Figures/response_box.png
   :scale: 50%
   :alt: The pychoacoustics response box

   The pychoacoustics response box

.. _fig-control_window:

.. figure:: Figures/control_window.png
   :scale: 50%
   :alt: The pychoacoustics control window

   The pychoacoustics control window


I started writing ``pychoacoustics`` for fun and for the sake of
learning around 2008 while doing my PhD with Professor Chris Plack at
Lancaster University. At that time we were using in the lab a MATLAB
program called the “Earlab” written by Professor Plack.
``pychoacoustics`` has been greatly influenced and inspired by the
“Earlab”. For this reason, as well as for the time he dedicated to teach
me audio programming, I am greatly indebted to Professor Plack.    
