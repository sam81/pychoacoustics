.. _sec-psychophysics:

**************
Psychophysics
**************

.. _sec-paradigms:

Available Paradigms
-------------------

Adaptive
^^^^^^^^

This paradigm implements the “up/down” adaptive procedures described by
[Levitt1971]_. It can be used with :math:`n`-intervals, :math:`n`-alternatives forced
choice tasks, in which :math:`n-1` “standard” stimuli and a single
“comparison” stimulus are presented, each in a different temporal
interval. The order of the temporal intervals is randomized from trial
to trial. The “comparison” stimulus usually differs from the “standard”
stimuli for a single characteristic (e.g. pitch or loudness), and the
listener has to tell in which temporal interval it was presented. A
classical example is the 2-intervals 2-alternatives forced-choice task.
Tasks that present a reference stimulus in the first interval, and
therefore have :math:`n` intervals and :math:`n-1` alternatives are also
supported (see [GrimaultEtAl2002]_ for an example of such tasks)

Adaptive Interleaved
^^^^^^^^^^^^^^^^^^^^

This paradigm implements the interleaved adaptive procedure described by [Jesteadt1980]_ .

Weighted Up/Down
^^^^^^^^^^^^^^^^

This paradigm implements the weighted up/down adaptive procedure
described by [Kaernbach1991]_.

Weighted Up/Down Interleaved
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This paradigm combines the interleaved adaptive procedure described by [Jesteadt1980]_ with the weighted up/down method described by [Kaernbach1991]_.

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


