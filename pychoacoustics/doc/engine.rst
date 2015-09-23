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

.. _sec-results_files:

Results Files
=============

``pychoacoustics`` outputs several types of
result files, these are listed in Table :ref:`tab-res_files`

.. _tab-res_files:

.. table:: List of result files produced by ``pychoacoustics``

  ======================== ============================= ========== ======================
  Type                     Example                       Formatting Suffix
  ======================== ============================= ========== ======================
  Block summary            ``myres.txt``                 Plain      ".txt"
  Full                     ``myres_full.txt``            Plain      "_full.txt"
  Session Summary          ``myres_res.txt``	         Plain      "_res.txt"
  Tabular Block Summary    ``myres_table.csv``           Tabular    "_table.csv"
  Tabular Full             ``myres_table_full.csv``      Tabular    "table_full.csv"
  Tabular Session Summary  ``myres_table_processed.csv`` Tabular    "table_processed.csv"
  ======================== ============================= ========== ======================
  
there are both "plain text" and "tabular" versions of result files. The plain text version
generally stores along with the results each parameter that was used during the experiment. The tabular result files
on the other hand store a smaller number of parameters, although additional parameters can be stored if the
experimenter wishes to do so (see :ref:`sec-tabular-results-files`). An important advantage of
tabular result files is that they are easy to import in other software (e.g. R, Libreoffice) for data analysis.
   
The “block summary” and "tabular block summary" result files contain summaries 
for each experimental block that was run. The “full” and "tabular full" result 
files instead contain information on each single
trial. The “block summary” result files (either in plain or tabular format) can be usually processed to
obtain “session summary” files.
The "session summary" files contain summaries for an entire 
experimental session. In these files the results are averaged across 
different blocks that have exactly the same stored parameters.

In order to obtain the session summary
files you need to use the appropriate functions that can be accessed
from the “File” menu. Alternatively, you can check the “Proc. Res.” 
and “Proc. Res. Table” checkboxes in the control window (see :ref:`sec-gui_left_panel`)
to let ``pychoacoustics`` automatically process these files at the end of an
experimental session. If processing the result files manually, choose
“Process Results (Plain Text)” from the “File” menu, to convert a block summary file
into a session summary file. Choose “Process Results Table” to
convert a tabular block summary file into a tabular session
summary file. You can choose to
process all blocks present in the file (default action), the last
:math:`n` blocks (of each condition), or a range of blocks (for each
condition). Once you have selected the file to process and specified the
blocks to process you can click “Run!” to perform the processing.
The functions that process the block summary files also allow you to plot the
results. Please, note that both the ability to process the block summary files
and plot the results are not available for all paradigms.
A list of the result files processing and plotting facilities available
for each paradigm is given in Table :ref:`tab-proc_res`

.. _tab-proc_res:

.. table:: Process results and plot facilities for various paradigms

  ==================================================  ========== ================== =======
  Procedure                                           Proc. Res. Proc. Res. Table   Plot
  ==================================================  ========== ================== =======
  Constant 1-Interval 2-Alternatives                  Yes        Yes                Yes
  Constant 1-Pair Same/Different                      Yes        Yes                Yes
  Constant m-Intervals n-Alternatives                 Yes        Yes                Yes
  Multiple Constants ABX                              Yes        Yes                Yes
  Multiple Constants 1-Interval 2-Alternatives        Yes        Yes                Yes
  Multiple Constants 1-Pair Same/Different            Yes        Yes                Yes
  Multiple Constants m-Intervals n-Alternatives       Yes        Yes                Yes
  Multiple Constants Odd One Out                      No         No                 No
  PEST                                                Yes        Yes                Yes
  PSI                                                 No         No                 No
  Transformed Up/Down                                 Yes        Yes                Yes
  Transformed Up/Down Interleaved                     Yes        Yes                Yes
  UML                                                 No         No                 No
  Weighted Up/Down                                    Yes        Yes                Yes
  Weighted Up/Down Interleaved                        Yes        Yes                Yes
  ==================================================  ========== ================== =======

.. _sec-tabular-results-files:

Tabular Results Files
---------------------

The tabular results files are comma separated value (csv) text files
that can be opened in a text file editor or a spreadsheet application.
The separator used by default is the semicolon “;”, but another
separator can be specified in the ``pychoacoustics`` preferences window.
When processing block summary table files, make sure that the csv
separator in the “Process Results Table” window matches the separator
used in the file.

The tabular result files contain a number of default columns that are specific 
to the paradigm used in the experiment (e.g., threshold, number of trials etc…). 
These result files also contain a "condition" column, where the "Condition Label"
is written (see :ref:`sec-gui_left_panel`). It is a good practice to assign 
a condition label as it makes it easy to sort the results as a function of the 
experimental condition.
Columns with additional parameters can be stored in these files. 
Several text fields and choosers in ``pychoacoustics`` have what we will call
``inSummary`` check boxes. Some of these are shown marked by ellipses 
in Figure :ref:`fig-inSummaryCheckBoxes`.

.. _fig-inSummaryCheckBoxes:

.. figure:: Figures/inSummaryCheckBoxes.png
   :scale: 75%
   :alt: ``inSummary`` check boxes

   ``inSummary`` check boxes

In the example shown in Figure :ref:`fig-inSummaryCheckBoxes` the frequency,
level and ear parameters will be stored, each in a separate column, in
the tabular block summary file, while the parameters
corresponding to the unchecked boxes (duration, ramps and type) will be
not. This is useful if you are running an experiment in which you are
systematically varying only a few parameters across different blocks,
and want to keep track of only those parameters. The ``inSummary`` check
boxes also provide visual landmarks for quickly spotting the widgets
with your parameters of interest in ``pychoacoustics``.

Notice that the “Process Results Table” function, as mentioned in the
previous section, will average the results for blocks with the same
parameters stored in the tabular block summary file. This
means that if you are varying a certain parameter (e.g., level) across
blocks, but you don’t check the corresponding ``inSummary`` check box
(for each block), the value of the parameter will not be stored in the
tabular block summary file, and as a consequence the “Process
Results Table” function will not be able to sort the blocks according to
the “level” parameter, and will average the results across all blocks.
Not all is lost because the “level” parameter will be nonetheless
stored in the “block summary” plain text file, but you will need more work before
you can process your results with a statistical software package.

.. todo::

    Add some info on tabular full files
    

Plain Text Result Files
-------------------------

The "block summary" result files, as well as the "full" result files
have a header for each experimental block. The start of the header
is marked by a line of 54 asterixes, an example is given below:

::

   *******************************************************
   pychoacoustics version: 0.2.73; build date: 01-Mar-2014 09:45
   Experiment version: pychoacoustics.default_experiments.audiogram 0.2.73 01-Mar-2014 09:45
   Block Number: 1
   Block Position: 1
   Start: 01/03/2014 14:07

the header gives info on the software version, the experiment
version (if available), the block storage point (Block Number), 
the block presentation position (Block Position), and has a 
timestamp marking the date and time at which the block was started.

After the header, there is a "parameters section" listing the 
experimental parameters. The beginning and the end of this section
are marked by a line of 54 plus signs, a snippet of the parameters
section is shown below:

::

   +++++++++++++++++++++++++++++++++++++++++++++++++++++++

   Experiment Label: 
   Session Label: 
   Condition Label: 
   Experiment:    Audiogram
   Listener: L3     
   [ ... ]
   Response Light Duration (ms): 500
   ISI:           500

   Ear: Right
   Signal Type: Sinusoid
   Frequency (Hz):  1000
   Level (dB SPL):  50
   Duration (ms):  180
   Ramps (ms):  10
   +++++++++++++++++++++++++++++++++++++++++++++++++++++++

After the parameters section there is a "results section". 
The specific structure of this section
depends on the procedure (e.g. transformed up-down, or constant
1-interval 2-alternatives) used.
The specific structure of the result section for each type of
procedure will be illustrated later on. The result section ends
invariably with a timestamp marking the date and time at which the
experimental block was completed, and a further line indicating
how much time the listener took to complete the block of trials.

The "session summary" result files have a section listing the
parameters used for each experimental condition. After this
section, a summary statistic for each block of the given experimental
condition is presented, followed by a summary statistic for all the blocks.



.. todo::
   
   Add description of result files for the various paradigms.

Transformed Up-Down, Weighted Up-Down, and PEST Result Files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Block Summary
"""""""""""""

The results section of a transformed up-down procedure are shown below
(weighted up-down and PEST result files have the same structure):

::

   42.00 62.00 58.00 66.00 | 60.00 64.00 58.00 62.00 54.00 56.00 50.00 52.00 | 

   turnpointMean = 57.00, s.d. =  4.90 
   B1 = 30, B2 = 22

the first line lists the turnpoints; the first ``|`` sign separates 
the initial turnpoints, which are not included in the threshold estimate, 
from the other turnpoints. The second line shows the threshold estimate 
(``turnpointMean``) and its standard deviation. The final line lists the
number of times each button was pressed by the listener. In the above case
the listener pressed button one 30 times and button two 22 times. This may be useful
to detect any biases in button choice. The results above were collected using
an arithmetic procedure. When the results are obtained with a geometric procedure
the second line of the results section labels the threshold estimate as 
``geometric turnpointMean``, as shown in the example below:

::

   0.08  5.00  1.25 80.00 | 10.00 40.00 10.00 200.00 25.00 200.00  6.25 25.00 | 

   geometric turnpointMean = 29.82, s.d. =  3.75 
   B1 = 22, B2 = 40


Full Result Files
"""""""""""""""""

A snippet from a transformed up-down ``full`` result file is shown
below:

::

   50.0; 1; 
   50.0; 1; 
   46.0; 1; 
   46.0; 1; 
   42.0; 1; 
   42.0; 0; 
   46.0; 0; 
   50.0; 1; 

each row represents a trial, the first colum shows the value of the
adaptive difference for that trial (e.g. the level of the signal in
a signal detection task), while the second column indicates whether
the response was correct (``1``), or incorrect (``0``). Note that 
depending on the experiment, additional variables may be stored in
a ``full`` result file. For example, in the ``F0DL`` experiment, which
has an option to use either a fixed, or a roving F0, the F0 for the
trial is listed in the third column of the ``full`` result file, as shown
below:

::

   20.0; 1; 408.58891957189206 ;
   20.0; 1; 409.72312872085564 ;
   5.0; 1; 474.15423804320403 ;
   5.0; 1; 404.43567907073964 ;
   1.25; 1; 456.6493420827598 ;
   1.25; 1; 406.34270314673716 ;

Session Summary Files
"""""""""""""""""""""

The result section of a transformed up-down procedure are shown
below:

::

   57.00
   44.00

   Mean = 50.50 
   SE =  6.50 

the session included two blocks of trials, and the first two lines
list the threshold estimate for each of these blocks. The following
lines present the mean and the stadandard error of these threshold
estimates.

Table Block Summary Result Files
""""""""""""""""""""""""""""""""

The first two columns of a transformed up-down, weighted up-down or PEST
block summary table result file contain the threshold estimate for each block of trials,
and its standard deviation. The header of the column with the threshold
estimate is ``threshold_arithmetic`` if the procedure was arithmetic,
and ``threshold_geometric`` if the procedure was geometric.

Table Session Summary Result Files
""""""""""""""""""""""""""""""""""

The first two columns of a transformed up-down, weighted up-down or PEST
session summary table result file contain the across-blocks mean threshold estimate for each 
experimental condition, and its standard error. The header of the column with the threshold
estimate is ``threshold_arithmetic`` if the procedure was arithmetic,
and ``threshold_geometric`` if the procedure was geometric.


Transformed Up-Down, and Weighted Up-Down Interleaved Result Files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Constant m-Intervals n-Alternatives Result Files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Multiple Constants m-Intervals n-Alternatives Result Files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Constant 1-Intervals 2-Alternatives Result Files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Multiple Constants 1-Intervals 2-Alternatives Result Files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Constant 1-Pair Same/Different Result Files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Multiple Constants Odd One Out Result Files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _sec-log_results_files: 

Log Results Files
-----------------

``pychoacoustics`` automatically saves backup copies of the “block
summary” and “full” files in a backup folder. On Linux systems this
folder is located in

::

    ~/.local/share/data/pychoacoustics/data_backup

on Windows systems it is located in

::

    C:\\Users\username\.local\share\data\pychoacoustics\data_backup

where ``username`` is your account login name. A separate file is saved
for each block of trials that is run. These files are named according to
the date and time at which the blocks were started (the naming follows
the YY-MM-DD-HH-MM-SS scheme). Unlike other results files, that are
written only once a block of trials has been completed, these log
results files get written as soon as information is available (e.g., a
new line in the “full” results file is written at the end of each
trial).



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
the file where ``pychoacoustics`` has saved the data. A full listing of
these special strings is given in Table :ref:`tab-pycho_variables`

.. _tab-pycho_variables:

.. table:: `pychoacoustics` variables

   ==================   =================================

   **String**           **Variable**

   ``[resDir]``         Results file directory
   ``[resFile]``        Block summary results file
   ``[resFileFull]``    Full results file
   ``[resFileRes]``     Session summary results file
   ``[resTable]``       Block summary table results file
   ``[listener]``       Listener label
   ``[experimenter]``   Experimenter ID

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
