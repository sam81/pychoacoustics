.. _sec-psychophysics:

*********
Paradigms
*********

.. todo::

   Give better description of the available paradigms.

.. _sec-paradigms:

Available Paradigms
===================


Transformed Up-Down
^^^^^^^^^^^^^^^^^^^

This paradigm implements the transformed up-down adaptive procedures described by
[Levitt1971]_. It can be used with :math:`n`-intervals, :math:`n`-alternatives forced
choice tasks, in which :math:`n-1` “standard” stimuli and a single
“comparison” stimulus are presented, each in a different temporal
interval. The order of the intervals is randomized from trial
to trial. The “comparison” stimulus usually differs from the “standard”
stimuli for a single characteristic (e.g. pitch or loudness), and the
listener has to tell in which temporal interval it was presented. A
classical example is the 2-intervals 2-alternatives forced-choice task.
Tasks that present a reference stimulus in the first interval, and
therefore have :math:`n` intervals and :math:`n-1` alternatives are also
supported (see [GrimaultEtAl2002]_ for an example of such tasks)

Transformed Up-Down Interleaved
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This paradigm implements the interleaved transformed up-down procedure described by [Jesteadt1980]_ .

Weighted Up-Down
^^^^^^^^^^^^^^^^

This paradigm implements the weighted up-down adaptive procedure
described by [Kaernbach1991]_.

Weighted Up-Down Interleaved
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This paradigm combines the interleaved procedure described by [Jesteadt1980]_ with the weighted up-down method described by [Kaernbach1991]_.

Constant m-Intervals n-Alternatives
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This paradigm implements a constant difference method for forced choice
tasks with :math:`m`-intervals and :math:`n`-alternatives. For example,
it can be used for running a 2-intervals, 2-alternatives forced-choice
frequency-discrimination task with a constant difference between the
stimuli in the standard and comparison intervals.

Constant 1-Interval 2-Alternatives
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This paradigm implements a constant difference method for tasks with a
single observation interval and two response alternatives, such as the
“Yes/No” signal detection task.

Constant 1-Pair Same/Different
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This paradigm implements a constant difference method for
“same/different” tasks with a single pair of stimuli to compare.

Multiple Constants 1-Pair Same/Different
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This paradigm implements a constant difference method for
“same/different” tasks with multiple pairs of stimuli to compare.

Multiple Constants ABX
^^^^^^^^^^^^^^^^^^^^^^

This paradigm implements a constant difference method for
“ABX” tasks with multiple pairs of stimuli to compare.

Odd One Out
^^^^^^^^^^^

This paradigm implements a three-alternatives oddity procedure (see
[VersfeldEtAl1996]_).

PEST
^^^^

This paradigm implements the PEST adaptive procedure described
by [TaylorAndCreelman1967]_. However, beware that support for 
this procedure in ``pychoacoustics`` is very experimental.
Its implementation has received very little testing.

PSI
^^^

This paradigm implements the PSI+ and PSI-marginal adaptive procedures described
by [Prins2013]_. 

UML
^^^

This paradigm implements the updated maximum likelihood (UML) adaptive procedure described
by [ShenAndRichards2012]_. 
