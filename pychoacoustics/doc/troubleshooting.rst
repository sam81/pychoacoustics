****************
Troubleshooting
****************

The computer crashed in the middle of an experimental session
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``pychoacoustics`` saves the results at the end of each block, therefore
only the results from the last uncompleted block will be lost, the
results of completed blocks will not be lost. If you have an experiment
with many different blocks presented in random order it may be difficult
to see which blocks the listener had already completed and set
``pychoacoustics`` to run only the blocks that were not run. To address
this issue ``pychoacoustics`` keeps a copy of the parameters, including
the block presentation order after shuffling, in a file called
``.tmp_prm.prm`` (this is a hidden file on Linux systems). Therefore,
after the crash you can simply load this parameters file and move to the
block position that the listener was running when the computer crashed
to resume the experiment.

A second function of the ``.tmp_prm.prm`` file is to keep a copy of
parameters that were stored in memory, but not saved to a file. If your
computer crashed while you were setting up a parameters for an
experiment that were not yet saved (or were only partially saved) to a
file, you can retrieve them after the crash by loading the
``.tmp_prm.prm`` file. One important thing to keep in mind is that the
``.tmp_prm.prm`` will be overwritten as soon as new parameters are
stored in memory by a ``pychoacoustics`` instance opened in the same
directory. Therefore it is advisable to make a copy of the
``.tmp_prm.prm`` file renaming it to avoid accidentally loosing its
contents after the crash.
