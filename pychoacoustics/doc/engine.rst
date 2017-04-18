.. _sec_engine:

*******************************
The ``pychoacoustics`` Engine
*******************************

.. _sec-sound_output:

Sound Output
============


Sound Output on Linux
---------------------

On Linux systems ``pychoacoustics`` can either output sound (numpy
arrays) directly to the soundcard, or write a ``WAV`` file for each sound
and call an external command to play it. Currently, sending
sounds directly to the soundcard is possible only through the
`alsaaudio <http://pyalsaaudio.sourceforge.net/>`_,
or through the `pyaudio <http://people.csail.mit.edu/hubert/pyaudio/>`_
Python modules. These modules are optional, and you need to install them 
yourself to be able to use them. Note that I've experienced issues (occasional
pops and crackles) with ``pyaudio`` on the hardware that I have tested.
Sound output with ``alsaaudio``, on the other hand, has been working very well.
Once the modules are installed, they will be detected automatically and you will
be able to select one of them as the “Play Command” in the sound preferences 
dialog. When you select ``alsaaudio`` as the play command, if you have multiple
soundcards, you can select the device to which the sound will be sent.
There will be also an option to set the size of the buffer that
``alsaaudio`` uses to play sounds. If the buffer is not filled completely by
a sound (buffer size greater than number of samples in the sound), it
will be zero padded. This may lead to some latency between the offset of
a sound and the onset of the following one. If you set a value smaller
than one the buffer size will be automatically set to the number of
samples in the sound that is being played.

Using an external command to play sounds generally works very well and
is fast on modern hardware. ``pychoacoustics`` tries to detect available
play commands on your system each time it starts up. On Linux systems,
the recommended play command is ``aplay``, which is installed by default
on most Linux distributions. ``aplay`` supports 24-bit output on 24-bit
soundcards with appropriate Linux drivers. Other possible play commands
are ``play``, which is provided by `sox <http://sox.sourceforge.net/>`_
and ``sndfile-play``, which is provided by the
`libsndfile <http://www.mega-nerd.com/libsndfile/>`_ tools. You can call
another program by choosing “custom” in the “Play Command” drop-down
menu and spelling out the name of the command in the box below.

Sound Output on Windows
-----------------------

The command that ``pychoacoustics`` uses by default on Windows is
``winsound``. This command supports only 16-bit output. ``pychoacoustics``
can also use ``pyaudio`` to output sound on Windows. ``pyaudio``,
however, needs to be manually installed. ``pyaudio`` can use several
Windows sound APIs, including MME, ASIO, and WASAPI. The ``pyaudio``
binaries available on the official project
`website <http://people.csail.mit.edu/hubert/pyaudio/support>`_ support
only the MME API, which is limited to 16-bit output. ASIO and WASAPI
on the other hand, can play sounds with full 24-bit resolution.
In order to have ``pyaudio`` built with ASIO and/or WASAPI support
you need to either build it from source, enabling these APIs (not for the
faint of heart), or dowload the unoffical binaries made available by  Christoph 
Gohlke on his `website <http://www.lfd.uci.edu/~gohlke/pythonlibs/>`_.

Other possible play commands on Windows are ``play``, which is provided by
`sox <http://sox.sourceforge.net/>`_ and ``sndfile-play``, which is
provided by the `libsndfile <http://www.mega-nerd.com/libsndfile/>`_
tools. These programs need to be installed by the user. If they are in
the system path, ``pychoacoustics`` will detect them automatically. 
Note that external media players with a graphical user interface (like
foobar2000) may not work well with ``pychoacoustics``.

Sound Output on macOS
---------------------

By default ``pychoacoustics`` uses the ``afplay`` command to output sound
on macOS. If ``pyaudio`` is properly installed and configured for the Python
distribution used to run ``pychoacoustics`` it can also be used by ``pychoacoustics`` to play sounds on macOS.

Sound Output on FreeBSD
-----------------------

The default command used by ``pychoacoustics`` to play sound on FreeBSD is ``wavplay``.
Several other commands can be used to play sound on FreeBSD systems, see `here <https://forums.freebsd.org/threads/59793/>`_.

.. _sec-parameters_files:

Parameters Files
================

Parameters files are plain text files, that can be modified through 
``pychoacoustics`` or through a text editor. They contain a header 
with information that applies to all the experimental blocks stored 
in a parameters file, and sections corresponding to the parameters 
that are specific to each experimental block store in a parameters 
file. The header contains the following fields:

-  Phones

-  Shuffle Mode

-  Response Mode

-  Auto Resp. Mode Perc. Corr.

-  Sample Rate

-  Bits

-  Trigger On/Off

-  Experiment Label

-  End Command

-  Shuffling Scheme

-  No. Repetitions

-  Proc. Res.

-  Proc. Res. Table

-  Plot

-  PDF Plot

You can refer to Section :ref:`sec-gui_left_panel` to know what each 
of these fields represents.

The sections that contain the parameters for each experimental block are
subdivided into fields that are separated by one or more dots. You
should not change this formatting when modifying parameters files.

A fragment from a parameters file is shown below:

::

    Paradigm: Adaptive
    Intervals: 2 :False
    Alternatives: 2 :False

each entry here has two or three elements separated by colons. The first
element represents the variable of interest, the second element its
value, and the third element is a boolean value that determines whether
the ``inSummary`` checkbox will be checked or not (see 
Section :ref:`sec-results_files` for more info on this).
You can have one or more spaces between each element and the colon
separator. Each entry has to be written on a single line.


.. _sec-shuffling:

Block Presentation Position
===========================


We will define the serial position at which a block is presented during
an experimental session as its “presentation position”, and the serial
position at which a block is stored in a parameters file as its “storage
point”.

Clicking the “Shuffle” button randomises the presentation positions of
the blocks, but leaves the order in which the blocks are stored in a
parameters file untouched. The “Previous” and “Next” buttons, as well as
the “Jump to Block” chooser let you navigate across the blocks storage
points, while the “Previous Position”, and the “Next Position” buttons,
as well as the “Jump to Position” chooser let you navigate across the
blocks presentation positions.

The block presentation positions are recorded in the parameters files.
This is useful in case you have to interrupt an experimental session
whose block presentation positions had been randomized, before it is
finished, and continue it at a later date. In this case you can save the
parameters file, reload it next time, and let the listener complete the
experimental blocks that s/he had not run because of the interruption.
Notice that each time you load a parameters file ``pychoacoustics`` will
automatically move to the first block presentation position. Therefore,
you will have to note down what was the last block that your listener
had run in the interrupted session (or find out by looking at the
results file) and move to the presentation position of the following
block yourself.

By default clicking on the “Shuffle” button performs a simple full
randomization of the block presentation positions. However, you can
specify more complex shuffling schemes in the “Shuffling Scheme” text
field. Let’s say you want to present two tasks in your experiment, a
frequency discrimination and an intensity discrimination task. Each task
has four subconditions, (e.g. four different base frequencies for the
frequency discrimination task and four different base intensities for
the intensity discrimination task). Your parameters file will contain
eight blocks in total, blocks one to four are for the frequency
discrimination task and blocks five to eight are for the intensity
discrimination task. During the experiment you want your participants to
run first the four frequency discrimination conditions in random order,
and afterwards the four intensity discrimination conditions in random
order. To achieve this you can enter the following shuffling scheme:

::

    ([1,2,3,4], [5,6,7,8])

basically you specify sequences (which can be nested) with your
experimental blocks, sequences within round parentheses ``()`` are not
shuffled, while sequences within square brackets ``[]`` are shuffled.
Following the previous example, if you want to present first the four
blocks of one of the tasks (either frequency or intensity) in random
order, and then the four blocks of the other task in random order, you
would specify your shuffling scheme as follows:

::

    [[1,2,3,4], [5,6,7,8]]

on the other hand, if you want to present first the four blocks of one
of the tasks (either frequency or intensity) in sequential order and
then the four blocks of the other task in sequential order, you would
specify your shuffling scheme as follows:

::

    [(1,2,3,4), (5,6,7,8)]

you can have any variation you like on the theme, and the lists can be
nested ad libitum, so for example you could have:

::

    [(1,2,[3,4]), (5,6,7,8)]

this would instruct ``pychoacoustics`` to present first either the four
frequency conditions or the four intensity conditions. The first two
frequency conditions are presented sequentially, while the last two are
shuffled. To save typing you can give ranges rather than listing all
blocks individually. For example:

::

    ([1-4], [5-8])

is equivalent to:

::

    ([1,2,3,4], [5,6,7,8])

    

.. _sec-task_instructions:

Displaying Task Instructions
============================

Although it is common to simply give task instructions verbally for
psychophysics experiments, sometimes it is useful to present task
instructions on the computer screen while the listener is running a test.
For example, there may be cases in which you want to your participants to perform two
different tasks within the same session. You may want your
participants to perform a frequency discrimination task with a pure
tone for the first two blocks of trials, and then run two blocks of
an intensity discrimination task with the same stimulus. In these
cases it is necessary to present visually the task instructions on the
computer screen either at the beginning of each block, or only at the
blocks where the task changes. `pychoacoustics` allows you to store
task instructions for each block of trials in the "Instructions" box
on the left side of the control window. The "Show Instructions At BP"
box below allows you to set the block positions at which the
instructions will be shown. In the example above, in which the
listener has to complete two blocks of the frequency discrimination
task first, and then complete two blocks of the intensity
discrimination task, you could input`1,2,3,4` in the "Show
Instructions At BP" box to show task instructions at the beginning of
each block. Alternatively, you could input`1,3` in the "Show
Instructions At BP" box to show task instructions only when a new task
is starting. You should keep in mind that the "Show
Instructions At BP" box sets the block positions at which the
instructions will be shown. Depending on the shuffling scheme that
you're using these may be different from the block storage points (see
:ref:`sec-shuffling` above for more info). 

.. _sec-os_commands:

OS Commands
===========


``pychoacoustics`` can be instructed to run operating system (OS)
commands at the end of an experiment. This may be useful to run custom
scripts that may analyse the result files, backup result files or
perform other operations.

In the control window, you can enter commands that you want to be
executed at the end of a specific experiment in the "End Command" box.
This command will be saved in the parameters file of the experiment.

In the "Preferences Dialog", under the "Notifications" tab you can
instead set a command that will be executed at the end of each
experiment you run, or :math:`n` blocks before the end of each
experiment you run. These commands should be entered in the "Execute
custom command" boxes.

The commands that you can execute are OS commands, therefore they are
different on Linux and Windows platforms. On Linux, for example,
assuming that you store all your experimental results in the directory
"/home/foo/exp/", you could automatically make a backup of these files
in the directory "/home/foo/backup/exp/" by using the command

.. code-block:: bash

    $ rsync -r -t -v --progress -s /home/foo/exp/ /home/foo/backup/exp/

To make things more interesting, you can use some special strings to
pass ``pychoacoustics`` internal variables to your commands. For
example, if you want to copy the results file of the current experiment
to the directory "/home/foo/res/", you can use the command

.. code-block:: bash

    $ cp [resFile] /home/foo/backup/exp/

here the special string ``[resFile]`` will be converted to the name of
the file where ``pychoacoustics`` has saved the data. To make sure that
the command executes without errors even if the name of the result file
contains white spaces you should put the variable referring
to the filename between quotes:

.. code-block:: bash

    $ cp "[resFile]" /home/foo/backup/exp/

A full listing of the internal ``pychoacoustics`` variables that
can be called by special strings in your commands is given in
Table :ref:`tab-pycho_variables`

.. _tab-pycho_variables:

.. table:: `pychoacoustics` variables

   ==================   =================================

   **String**           **Variable**

   ``[resDir]``         Results file directory
   ``[resFile]``        Plain-text block-summary results file
   ``[resFileTrial]``   Plain-text trial-summary results file
   ``[resFileSess]``    Plain-text session-summary results file
   ``[resTable]``       Tabular block-summary results file
   ``[resTableTrials]`` Tabular trial-summary results file
   ``[resTableSess]``   Tabular session-summary results file
   ``[listener]``       Listener label
   ``[experimenter]``   Experimenter ID
   ``[pdfPlot]``        pdf plot file of the session summary

   ==================   =================================




Preferences Settings
====================

All the settings that can be manipulated in the
“Preferences” dialog, as well as the “Phones” and “Experimenters”
dialogs are stored in a file in the user home directory. On Linux this
file is located in:

::

    ~/.config/pychoacoustics/preferences.py

On Windows, assuming the root drive is “C” it is located in:

::

    C:\\Users\username\.config/pychoacoustics\preferences.py

where ``username`` is your Windows login username. Although I strive to
avoid this, the way in which the preferences settings are stored may
change in newer versions of pychoacoustics. This means that when
pychoacoustics is upgraded to a newer version it may sometimes not start
or throw out errors. To address these issues, please, try removing the
old preferences file. Of course this means that you’re going to lose all
the settings that you had previously saved. To avoid loosing any
precious information, such as the calibration values of your headphones,
write down all important info before removing the preferences file.

.. _sec-response_mode:

Response Mode
=============

``pychoacoustics`` was designed to run interactive experiments in which
a listener hears some stimuli and gives a response through a button or
key press. This is the default mode, called “Real Listener” mode.
``pychoacoustics`` provides two additional response modes, “Automatic”
and “Simulated Listener”. These modes can be set through the control
window.

In “Automatic” response mode, rather than waiting for the listener to
give a response, ``pychoacoustics`` gives itself a response and proceeds
to the next trial. The probability that this automatic response is
correct can also be set through the control window. The “Automatic”
response mode has two main functions. The first is testing and debugging
an experiment. Rather than running the experiment yourself, you can
launch ``pychoacoustics`` in “Automatic” response mode and check that
everything runs smoothly, the program doesn’t crash, and the result
files are saved correctly. The second function of the automatic response
mode is to allow passive presentation of the stimuli. Some neuroimaging
experiments (e.g. electroencephalographic or functional magnetic
resonance recordings) are performed with listeners passively listening
to the stimuli. These experiments usually also require that the program
presenting the stimuli sends triggers to the recording equipment to flag
the start of a trial. Potentially this can also be done in
``pychoacoustics`` (and we’ve done it in our lab for
electroencephalographic recordings), but at the moment this
functionality is not implemented in a general way in the program.

The “Simulated Listener” mode is simply a hook that allows you to
redirect the control flow of the program to some code that simulates a
listener and provides a response. Notice that ``pychoacoustics`` does
not provide any simulation code in itself, the simulation code has to be
written by you for a specific experiment. If no simulation code is
written in the experiment file, ``pychoacoustics`` will do nothing in
simulated listenr mode. Further details on how to use the “Simulated
Listener” mode are provided in Section :ref:`sec-simulations`.

Both the “Automatic” and the “Simulated Listener” make recursive
function calls. In Python the number of recursive function calls that
you can make is limited. If your experiment passes this limit
``pychoacoustics`` will crash. The limit can be raised, up to a certain
extent (which is dependent on your operating system, see the
documentation for the setrecursionlimit function in the Python ``sys``
module) through the “Max Recursion Depth” setting that you can find in
the preferences window, or set through a command line option when
running ``pychoacoustics`` from the command line. Notice that the total
number of recursive calls that your program will make to complete an
experiments will be higher than the number of trials in the experiment,
so you should set the “Max Recursion Depth” to a value higher than the
number of trials you’re planning to perform (how much higher I don’t
know, you should find out by trial and error, a few hundred points
higher is usually sufficient). If you’re planning to run a very high
number of trials in “Automatic” or “Simulated Listener” mode, rather
than raising the max recursion depth, it may be better to split the
experiment in several parts. You can always write a script that
automatically launches ``pychoacoustics`` from the command line
instructing it to load a given parameters file. On UNIX machines you
could write a shell script to do that, but an easier way is perhaphs to
use python itself to write the script. For example, the ``python``
script could be:

.. code-block:: python

    #! /usr/bin/env python
    for i in range(5):
       cmd = "pychoacoustics --file prms.prm -l L1 -s s1 -q -a \
             --recursion-depth 3000" 

here we’re telling ``pychoacoustics`` to load the parameters file
``prms.prm``, set the listener identifier to “L1” and the session label
to s1. The ``-q`` option instructs the program to exit at the end of the
experiment. This way the recursion depth count is effectively restarted
each time ``pychoacoustics`` is closed and launched again from the
script. When the ``--recursion-depth`` option is passed as a command
line argument, as in the example above, it overrides the max recursion
depth value set in the preferences window. If the ``-a`` option is
passed, as in the examples above, ``pychoacoustics`` will start
automatically at the beginning of each of the five series . This is
useful for debugging or simulations, so that you can start the script
and leave the program complete unattended (you need to make sure that
the “Shuffling Mode” is not set to “Ask” and that you pass listener and
session labels if you want the program to run completely unattended).
