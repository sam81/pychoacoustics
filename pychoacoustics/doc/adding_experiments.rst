****************************
Writing your own Experiments
****************************

First Steps
===========

``pychoacoustics`` can be easily extended with new experiments written by users. User-written experiments need to reside in a Python package called ``labexp``, and this package needs to be in your Python path. No worries if you're not familiar with packaging Python software, we'll go through the process of adding a new experiment step by step.

First of all, you need to create a directory called ``pychoacoustics_exp`` inside your home directory, and a sub-directory called ``labexp`` inside the ``pychoacoustics_exp`` directory. If you don't know where your home directory is located you can find out from a Python shell with the following commands:

.. code-block:: python

   import os
   os.path.expanduser('~')

You can create the ``pychoacoustics_exp`` and ``labexp`` directories from a Python shell as shown below:

.. code-block:: python

   import os
   dirPath = os.path.expanduser('~/pychoacoustics_exp/labexp/')
   os.makedirs(dirPath)


Each user experiment will be  written in a single file contained in the ``labexp`` directory. Let’s imagine we want to create an experiment for a frequency discrimination task. We create a file named ``freq.py`` in the ``labexp`` directory. In addition to the experiment file we need an additional file that lists all the experiments contained in the ``labexp`` directory. This file must be named ``__init__.py``, and in our case it will have the following content:

.. code-block:: python
    
    __all__ = ["freq"]

here the variable ``__all__`` is simply a Python list with the
name of the experiment files. So, if one day we decide to write a new
experiment on, let’s say, level discrimination, in a file called
``lev.py`` we would simply add it to the list in ``__init__.py``:

.. code-block:: python
    
    __all__ = ["freq",
               "lev"]

For people familiar with packaging Python modules it should be clear
by now that the ``labexp`` folder is a Python package
containing various modules (the experiment files). If at some point we
want to remove an experiment from ``pychoacoustics``, for example
because it contains a bug that does not allow the program to start, we
can simply remove it from the list in ``__init__.py``.  Let’s go back
to the ``freq.py`` file. Here we need to define three functions. For our
example the names of these functions would be:

.. code-block:: python
    
    initialize_freq()
    select_default_parameters_freq()
    doTrial_freq()

basically the function names consist of a fixed prefix, followed by
the name of the experiment file. So, in the case of the level experiment
example, written in the file ``lev.py``, the three functions would be
called:


.. code-block:: python
    
    initialize_lev()
    select_default_parameters_lev()
    doTrial_lev()

we’ll look at each function in detail in the next section. Briefly, the
``initialize_`` function is used to set some general parameters and
options for our experiment; the ``select_default_parameters_`` function
lists all the widgets (text fields and choosers) of our experiment and
their default values; finally, the ``doTrial_`` function contains the code that
generates the sounds and plays them during the experiment.


Anatomy of a ``pychoacoustics`` experiment file
-----------------------------------------------

The ``initialize_`` function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``initialize_`` function of our frequency discrimination 
experiment is shown below:

.. code-block:: python
   :linenos:

    
    def initialize_freq(prm):
      exp_name = "Frequency Discrimination Demo"
      prm["experimentsChoices"].append(exp_name)
      prm[exp_name] = {}
      prm[exp_name]["paradigmChoices"] = ["Transformed Up-Down",
                                          "Weighted Up-Down",
                                          "UML",
                                          "PSI"]
    
      prm[exp_name]["opts"] = ["hasISIBox", "hasAlternativesChooser", 
                               "hasFeedback"]

      prm[exp_name]['defaultAdaptiveType'] = "Geometric"
      prm[exp_name]['defaultNIntervals'] = 2
      prm[exp_name]['defaultNAlternatives'] = 2
      prm[exp_name]["execString"] = "freq"
      prm[exp_name]["version"] = "1"

      return prm

When the function is called, it is passed a dictionary containing
various parameters through the ``prm`` argument. The function modifies 
this dictionary by adding the parameters of the experiment, and returns
the dictionary back to the main routine. 

Let's analyze the function for our experiment. On line 2
we give a label to the experiment, this can be anything we
want, except the label of an experiment already existing. On line 3
we add this experiment label to the list of “experimentsChoices”.
On line 4 we create a new sub-dictionary that has as a key the
experiment label. Next we list the paradigms that our experiment
supports by creating a ``paradigmChoices`` key and giving the names of
the supported paradigms as a list. The paradigms listed here must be
within the set of paradigms  supported by ``pychoacoustics`` (see
Section :ref:`sec-paradigms` for a description of the paradigms currently
supported). In the next line we set an ``opts`` key containing a list
of options. The full list of options that can be set here is described
in details in Section :ref:`sec-experiment_opts`. In brief, for our
experiment we want to have a widget to set the silent interval (ISI)
between presentation
intervals (``hasISIBox``), a widget to choose the number of response
alternatives (``hasAlternativesChooser``), and a widget to set the feedback
on or off for a given block of trials (``hasFeedback``).

In the next line we specify ``defaultAdaptiveType``, the default type of adaptive 
track that will be selected when the experiment is loaded, this could be 
either "Geometric", or "Arithmetic". Specifying a "defaultAdaptiveType" is
optional. The type of the adaptive procedure can in any case be changed
later by the experimenter in the control window.
In the next two lines we specify the default number of intervals, and the
default number of alternatives that will be used when the experiment is
loaded. Since we have inserted the "hasAlternativesChooser" option, the
number of intervals and alternatives can be later changed by the experimenter
using the appropriate choosers in the control window.
The next line of the ``initialize_`` function sets the
``execString`` of our experiment. This must be the name of our
experiment file, so in our case ``freq``.   
Finally, we give our experiment a version label. This is optional, but it can
be very useful as this version label will be stored in the result files when
the experiment is run. This makes it possible to track which version of the
experiment was used in a given session.

Before we proceed, a note on the use of a function called ``QApplication.translate``
is necessary. You may occasionally see this function in ``pychoacoustics`` experiment
files and in this manual. This function serves to translate strings from one language
to another. For the moment it doesn't really do much in ``pychoacoustics`` because
string translation is not currently functional for the control window, it is only functional for the
response box. This function takes three string arguments, and the text to be translated
is the middle argument. For example, in the ``initialize_`` function above, we could have
written ``QApplication.translate("", "Transformed Up-Down", "")`` instead of ``Transformed Up-Down``.
You don't need to use this function in your experiments. If you do, you need to import the ``QApplication``.
How to do this depends on which version of ``PyQt`` you're using, as shown below:

.. code-block:: python
		
   from PyQt4.QtGui import QApplication #if you're using PyQt4
   from PySide.QtGui import QApplication #if you're using PySide
   from PyQt5.QtWidgets import QApplication #if you're using PyQt5
		

The ``select_default_parameters_`` function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

All the widgets (text fields and choosers) needed for an experiment are 
defined in the ``select_default_parameters_`` function. For our frequency 
discrimination experiment, the function looks as follows:

.. code-block:: python
   :linenos:

    
    def select_default_parameters_freq(parent, paradigm, par):
       
      field = []
      fieldLabel = []
      chooser = []
      chooserLabel = []
      chooserOptions = []

      fieldLabel.append("Frequency (Hz)")
      field.append(1000)
    
      fieldLabel.append("Difference (%)")
      field.append(20)
        
      fieldLabel.append("Level (dB SPL)")
      field.append(50)
       
      fieldLabel.append("Duration (ms)")
      field.append(180)
        
      fieldLabel.append("Ramps (ms)")
      field.append(10)
    
        
      chooserOptions.append(["Right",
                             "Left",
                             "Both"])
      chooserLabel.append("Ear:")
      chooser.append("Right")
      
      prm = {}
      prm['field'] = field
      prm['fieldLabel'] = fieldLabel
      prm['chooser'] = chooser
      prm['chooserLabel'] = chooserLabel
      prm['chooserOptions'] =  chooserOptions
    
      return prm

The ``select_default_parameters_`` function accepts three arguments, 
"parent" is simply a reference to the pychoacoustics application, 
"paradigm" is the paradigm with which the function has been called, 
while "par" is a variable that can hold some special values for 
initializing the function. The use of the "par" argument will be discussed 
later on when procedures with interleaved tracks will be described. For the
time being you should just know that the ``select_default_parameters_`` should
always have this argument.
From line three to line seven, we create a 
series of empty lists. The ``field`` and ``fieldLabel`` lists will hold 
the default values of our text field widgets, and their labels, respectively. 
The ``chooser`` and ``chooserLabel`` lists will likewise hold the default 
values of our chooser widgets, and their labels, while the ``chooserOptions`` 
list will hold  the possible values that our choosers can take. 
On lines 9 to 29 we populate these lists for our frequency discrimination experiment. 
From line 31 to line 36 we insert in a dictionary the
``field``, ``fieldLabel``, ``chooser``, ``chooserLabel`` and ``chooserOptions`` 
lists that we previously creaetd and populated. Finally, on line 38, the function returns
this dictionary.


The ``doTrial_`` function
^^^^^^^^^^^^^^^^^^^^^^^^^

The ``doTrial_`` function is called each time a trial is started, and 
is responsible for generating the sounds and presenting them to the 
listener. The ``doTrial_`` function for our frequency discrimination 
experiment is shown below:

.. code-block:: python
   :linenos:

   def doTrial_freq(parent):

      currBlock = 'b'+ str(parent.prm['currentBlock'])
       if parent.prm['startOfBlock'] == True:
           parent.prm['adaptiveParam'] = \
             parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Difference (%)")]
           parent.writeResultsHeader('log')

       frequency = \
         parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Frequency (Hz)")]
       level = \
         parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Level (dB SPL)")] 
       duration = \
         parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Duration (ms)")] 
       ramps = \
         parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Ramps (ms)")]
       channel = \
         parent.prm[currBlock]['chooser'][parent.prm['chooserLabel'].index("Ear:")]
       phase = 0

       correctFrequency = frequency + (frequency*parent.prm['adaptiveParam'])/100
       stimulusCorrect = pureTone(correctFrequency, phase, level, duration, 
                                  ramps, channel, parent.prm['sampRate'], 
                                  parent.prm['maxLevel'])
      
       stimulusIncorrect = []
       for i in range((parent.prm['nIntervals']-1)):
           thisSnd = pureTone(frequency, phase, level, duration, ramps, channel, 
                              parent.prm['sampRate'], parent.prm['maxLevel'])
           stimulusIncorrect.append(thisSnd)
       
       parent.playRandomisedIntervals(stimulusCorrect, stimulusIncorrect)

As you can see on the first line, the ``doTrial_`` function is passed 
as an argument its ``parent``. This is important because the parent contains 
a dictionary with the parameters for the current experiment (``parent.prm``). 
The parameters for each stored block of the experiment are stored 
in the ``parent.prm`` dictionary with keys starting with ``b`` followed by 
the block number. For example ``parent.prm['b3']`` contains the parameters 
for the third stored block. The current block number is stored in 
``parent.prm['currentBlock']``, and on line 3 we retrieve the dictionary 
key for the current block. On line 4 we start an ``if`` block that is executed 
only at the first trial of each block. In this block we retrieve the % frequency 
difference between the standard and the comparison stimuli for the first trial, 
and we store it in the ``parent.prm['adaptiveParam']`` variable. 
Since we're using an adaptive procedure, this variable will be automatically 
increased or decreased by ``pychoacoustics`` on successive trials on the bases 
of the responses given by the listener. On line 7 we tell ``pychoacoustics`` 
to write the header of the 'log' result files (see :ref:`sec-log_results_files`).

On lines 9-16 we read off the values of the text field widgets 
for the current block of trials. The values of these field widgets 
are stored in the list ``parent.prm[currBlock]['field']``, and we exploit 
the label of each text field widget to retrieve its index in the list. 
For example ``parent.prm['fieldLabel'].index("Frequency (Hz)")`` retrieves 
the index of the text widget that stores the frequency of the standard tone 
for the current block of trials. On line 18 we read off the value of the only 
chooser widget for the current block of trials. The values of chooser widgets 
are stored in the list ``parent.prm[currBlock]['chooser']``, and we exploit the 
label of each chooser widget to retrieve its index in the list as we did for 
text field widgets.


Our next step will be to generate the stimuli for the trial. 
In a `X`-Intervals task we have to generate `X` stimuli. In our case, 
the standard stimuli will have always the same frequency, we retrieved its value 
on lines 9-10 of our ``doTrial_`` function. If a listener presses the button 
corresponding to one of the the standard stimuli his response will be incorrect. 
For this reason we will store the standard stimuli in a list 
called ``stimulusIncorrect = []``. The comparison stimulus will be instead stored 
in a variable called ``stimulusCorrect``. The frequency of the comparison 
stimulus, which can vary from trial to trial, depending on the current value
of ``parent.prm['adaptiveParam']`` is computed on line 21. On lines 22-24  we 
generate the stimulus using the ``pureTone`` function that is available 
in the ``sndlib`` module. Note that in order to access this function you need
to import it by adding the following line at the top of the ``freq.py`` file 
where the experiment is stored:

.. code-block:: python

   from pychoacoustics.sndlib import pureTone

Note also that we need to pass the current samplig rate and the current maximum 
output level of our headphones (see :ref:`sec-edit_phones_dia`) to 
the ``pureTone`` function. Their values are stored respectively in the 
``parent.prm['sampRate']`` and ``parent.prm['maxLevel']`` variables. 
On lines 26-30 we generate and store the standard stimuli in the 
``stimulusIncorrect`` list. The number of standard stimuli to generate will 
be equal to the number of intervals minus one. The number of 
intervals is stored in the ``parent.prm['nIntervals']`` variable. Finally on line 
32 we call the ``parent.playRandomisedIntervals`` function to play the stimuli. 
This function requires two arguments, the correct stimulus, and a list containing 
the incorrect stimuli. That's it, our frequency discrimination experiment is ready 
and we can test it on ``pychoacoustics``.

Adding support for the Constant Paradigm
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

So far our frequency discrimination experiment supports only adaptive paradigms.

Adding support for the constant paradigm, in which the frequency difference 
between the standard and comparison stimuli is fixed across a block of trials 
is easy. All we need to do is add "Constant m-Intervals n-Alternatives" to the 
list of paradigms supported paradims in the ``initialize_`` function:

.. code-block:: python

   prm[exp_name]["paradigmChoices"] = ["Transformed Up-Down",
                                       "Weighted Up-Down",
                                       "UML",
                                       "PSI"
                                       "Constant m-Intervals n-Alternatives"]

Now our frequency discrimination task supports also the constant paradigm.

Showing/Hiding Widgets Dynamically
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Often you may want to write a single experiment that can handle a number 
of different experimental conditions. This usually leads to a growing number 
of widgets in the control window that can be distracting. 
To address this issue, in ``pychoacoustics`` it is possible to dinamically 
show or hide widgets depending on the value taken by chooser widgets. 
To do this, you need to write a function called ``get_fields_to_hide_`` 
that specifies the conditions upon which certain widgets are shown or hidden. 

For a practical example, let's extend the frequency discrimination experiment
described in the sections above so that it can handle not only conditions in
which the standard frequency is fixed, but also conditions in which the standard
frequency is roved from trial to trial within a specified frequency range. 
In the ``select_default_parameters_`` function of our frequency discrimination
experiment we had a text field for setting the standard frequency:

.. code-block:: python

      fieldLabel.append("Frequency (Hz)")
      field.append(1000)

now we'll add two additional text fields to set the frequency range for the
roved-frequency case:

.. code-block:: python

      fieldLabel.append("Frequency (Hz)")
      field.append(1000)

      fieldLabel.append("Min. Frequency (Hz)")
      field.append(250)

      fieldLabel.append("Max. Frequency (Hz)")
      field.append(4000)

we also add a chooser to control whether for the current block the standard frequency
should be fixed or roved:

.. code-block:: python

      chooserOptions.append(["Fixed",
                             "Roved"])
      chooserLabel.append("Standard Frequency:")
      chooser.append("Fixed")

The ``get_fields_to_hide_`` for this experiment is shown below:

.. code-block:: python
   :linenos:

   def get_fields_to_hide_freq(parent):
      if parent.chooser[parent.prm['chooserLabel'].index("Standard Frequency:")].currentText() == "Fixed":
         parent.fieldsToHide = [parent.prm['fieldLabel'].index("Min. Frequency (Hz)"),
                                parent.prm['fieldLabel'].index("Max. Frequency (Hz)")]
         parent.fieldsToShow = [parent.prm['fieldLabel'].index("Frequency (Hz)")]
      elif parent.chooser[parent.prm['chooserLabel'].index("Standard Frequency:")].currentText() == "Roved":
         parent.fieldsToHide = [parent.prm['fieldLabel'].index("Frequency (Hz)")]
         parent.fieldsToShow = [parent.prm['fieldLabel'].index("Min. Frequency (Hz)"),
                                parent.prm['fieldLabel'].index("Max. Frequency (Hz)")]

    
As for the other experiment functions that we have discussed before, 
the actual name is the concatenation of a prefix, in this case
``get_fields_to_hide_``, and the name of the experiment file, 
in this case ``freq``. As you can see on line 1, this function takes as an 
argument ``parent``, which contains the lists of widgets for the current experiment.
We need to tell the ``get_fields_to_hide_`` function that if the standard frequency 
is fixed, it should show only the ``Frequency (Hz)`` text field, and hide the 
``Min. Frequency (Hz)`` and ``Max. Frequency (Hz)`` text fields. Vice-versa, 
if the standard frequency is roved, it should show only the 
``Min. Frequency (Hz)`` and ``Max. Frequency (Hz)`` text fields, and hide the 
``Frequency (Hz)`` text field. On line 2 we start an ``if`` block which
will be executed if the value of the ``Standard Frequency`` chooser (retrieved 
by the ``currentText`` attribute), is set to ``Fixed``. Note how we exploit 
once again the ``chooserLabel`` to find the index of the chooser we want 
with ``parent.prm['chooserLabel'].index("Standard Frequency:")``. 
Next, we define two lists, one containing the indexes of the fields to hide 
``parent.fieldsToHide``, and one containing the indexes of the fields to show 
``parent.fieldsToShow``. Once more we exploit the ``fieldLabel`` to retrieve 
the indexes of the fields we want to get 
(e.g. ``parent.prm['fieldLabel'].index("Min. Frequency (Hz)")``).
From line 6 to line 9 we handle the case in which the standard frequency is 
roved. The logic of the code is the same as for the fixed standard frequency
case.

To complete the experiment we need to add a couple of lines to the ``doTrial_``
function to handle the case in which the standard frequency is roved.
The new function is shown below:

.. code-block:: python
   :linenos:

   def doTrial_freq2(parent):
      currBlock = 'b'+ str(parent.prm['currentBlock'])
      if parent.prm['startOfBlock'] == True:
         parent.prm['adaptiveParam'] = \
           parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Difference (%)")]
         parent.writeResultsHeader('log')

      frequency = \
        parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Frequency (Hz)")]
      minFrequency = \
        parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Min. Frequency (Hz)")]
      maxFrequency = \
        parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Max. Frequency (Hz)")]
      level = \
        parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Level (dB SPL)")] 
      duration = \
        parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Duration (ms)")] 
      ramps = \
        parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Ramps (ms)")]
      phase = 0
      channel = \
        parent.prm[currBlock]['chooser'][parent.prm['chooserLabel'].index("Ear:")]
      stdFreq = \
         parent.prm[currBlock]['chooser'][parent.prm['chooserLabel'].index("Standard Frequency:")]

      if stdFreq == "Roved":
         frequency = random.uniform(minFrequency, maxFrequency)
      correctFrequency = frequency + (frequency*parent.prm['adaptiveParam'])/100
      stimulusCorrect = pureTone(correctFrequency, phase, level, duration, 
                                 ramps, channel, parent.prm['sampRate'], 
                                 parent.prm['maxLevel'])
            
      stimulusIncorrect = []
      for i in range((parent.prm['nIntervals']-1)):
         thisSnd = pureTone(frequency, phase, level, duration, ramps, channel, 
                            parent.prm['sampRate'], parent.prm['maxLevel'])
         stimulusIncorrect.append(thisSnd)
      parent.playRandomisedIntervals(stimulusCorrect, stimulusIncorrect)
   

On lines 10-13 we read off the minimum and maximum frequency values for the roved-standard case. On line 23-24 we retrieve the
value of the ``Standard Frequency:`` chooser. On lines 26-27 we state that if the value of the standard frequency chooser 
is equal to ``Roved``, then the standard frequency for that trial should be drawn from a uniform distribution ranging
from ``minFrequency`` to ``maxFrequency``. The rest of the function is unchanged. Note that we're using the a Python module
called ``random`` on line 27, so we need to add ``import random`` at the top of our ``freq.py`` file.

It is also possible to show/hide choosers. Let's extend the frequency-discrimination experiment by allowing for the possibility 
that the standard frequency is roved on a log scale (which in fact would be a better choice given that frequency scaling in the auditory
system is approximately logarithmic). To do this, we first add a new chooser to set the roving scale:

.. code-block:: python

      chooserOptions.append(["Linear",
                             "Log"])
      chooserLabel.append("Roving Scale:")
      chooser.append("Linear")

Because this chooser is useful only when the standard frequency is roved, we'll tell the ``get_fields_to_hide_`` function to show/hide
it depending on the value of the ``Standard Frequency`` chooser. The new ``get_fields_to_hide_`` function is shown below:

.. code-block:: python
   :linenos:

   def get_fields_to_hide_freq(parent):
      if parent.chooser[parent.prm['chooserLabel'].index("Standard Frequency:")].currentText() == "Fixed":
         parent.fieldsToHide = [parent.prm['fieldLabel'].index("Min. Frequency (Hz)"),
                                parent.prm['fieldLabel'].index("Max. Frequency (Hz)")]
         parent.fieldsToShow = [parent.prm['fieldLabel'].index("Frequency (Hz)")]
	 parent.choosersToHide = [parent.prm['chooserLabel'].index("Roving Scale:")]
      elif parent.chooser[parent.prm['chooserLabel'].index("Standard Frequency:")].currentText() == "Roved":
         parent.fieldsToHide = [parent.prm['fieldLabel'].index("Frequency (Hz)")]
         parent.fieldsToShow = [parent.prm['fieldLabel'].index("Min. Frequency (Hz)"),
                                parent.prm['fieldLabel'].index("Max. Frequency (Hz)")]
	 parent.choosersToShow = [parent.prm['chooserLabel'].index("Roving Scale:")]

We've just added two lines. Line 6 gets executed if the ``Standard Frequency`` chooser is set to ``Fixed``,
and adds the ``Roving Scale`` chooser to the ``parent.choosersToHide`` list.  Line 11 gets executed 
if the ``Standard Frequency`` chooser is set to ``Roved``, and adds the ``Roving Scale`` chooser to the ``parent.choosersToShow`` list.

Finally, we need to add/modify a couple of lines of the ``doTrial_`` function. 
First of all we need to read off the value of the new ``Roving Scale`` chooser:

.. code-block:: python
      
    rovingScale = \
      parent.prm[currBlock]['chooser'][parent.prm['chooserLabel'].index("Roving Scale:")]

second, we need to set the standard frequency depending on whether it is drawn from a linear or a logarithmic distribution:

.. code-block:: python

     if stdFreq == "Roved":
        if rovingScale == "Linear":
           frequency = random.uniform(minFrequency, maxFrequency)
        elif rovingScale == "Log":
           frequency = 10**(random.uniform(log10(minFrequency), log10(maxFrequency)))

Note that we're using the ``log10`` function from numpy here, so we need to add ``from numpy import log10``
at the top of our ``freq.py`` file.


Writing a "Constant 1-Interval 2-Alternatives" Paradigm Experiment
===================================================================

In the next paragraphs we'll see an example of an experiment using the  
"Constant 1-Interval 2-Alternatives" paradigm. The experiment a is simple "Yes/No" signal
detection task. On each trial the listener is presented with a single interval which may
or may not contain a pure tone, and s/he has to tell if the tone was present or not.

The ``initialize_`` function for the signal detection experiment is shown below, since the
general framework for writing an experiment is the same as for the adaptive paradigm, 
only the differences from an adaptive-paradigm experiment will be highlited.

.. code-block:: python
   :linenos:

   def initialize_sig_detect(prm):
      exp_name = "Signal Detection Demo"
      prm["experimentsChoices"].append(exp_name)
      prm[exp_name] = {}
      prm[exp_name]["paradigmChoices"] = ["Constant 1-Interval 2-Alternatives"]
      prm[exp_name]["opts"] = ["hasFeedback"]
      prm[exp_name]["buttonLabels"] = ["Yes", "No"]
      prm[exp_name]['defaultNIntervals'] = 1
      prm[exp_name]['defaultNAlternatives'] = 2
    
      prm[exp_name]["execString"] = "sig_detect"
      return prm

On line 5 we list the available paradigms for the experiment, in this case the 
only paradigm possible is ``Constant 1-Interval 2-Alternatives``. On line 7 we 
insert ``hasFeedback`` to the list of experiment options, so that feedback can 
be provided at the end of each trial. Since we'll have a single observation 
interval we don't add the ``hasISIBox`` option, because we don't need to have a 
silent inteval between observation intervals. On line 7, we set the labels for 
the buttons, which represent the two response alternatives: "Yes" or "No". 
On line 8 and line 9 we set the number of intervals and the number of 
response alternatives. 

The ``select_default_parameters_`` function for the signal detection 
experiment is shown below:

.. code-block:: python
   :linenos:

   def select_default_parameters_sig_detect(parent, par):
   
      field = []
      fieldLabel = []
      chooser = []
      chooserLabel = []
      chooserOptions = []

      fieldLabel.append(parent.tr("Frequency (Hz)"))
      field.append(1000)
    
      fieldLabel.append(parent.tr("Duration (ms)"))
      field.append(2)
    
      fieldLabel.append(parent.tr("Ramps (ms)"))
      field.append(4)

      fieldLabel.append(parent.tr("Level (dB SPL)"))
      field.append(30)
    
      chooserOptions.append([parent.tr("Right"), parent.tr("Left"), parent.tr("Both")])
      chooserLabel.append(parent.tr("Channel:"))
      chooser.append(parent.tr("Both"))
        
      prm = {}
      prm['field'] = field
      prm['fieldLabel'] = fieldLabel
      prm['chooser'] = chooser
      prm['chooserLabel'] = chooserLabel
      prm['chooserOptions'] =  chooserOptions

      return prm

there is nothing really new here compared to experiments with adaptive 
paradigms that we have seen before. We initialize the text fields that we need
in order to set the frequency duration and level of the signal. We also 
initialize a chooser to set the channels on which the signal should be presented.

The ``doTrial_`` function for the signal detection task is shown below:

.. code-block:: python
   :linenos:

   def doTrial_sig_detect(parent):
  
      currBlock = 'b'+ str(parent.prm['currentBlock'])
      if parent.prm['startOfBlock'] == True:
          parent.writeResultsHeader('log')
          parent.prm['conditions'] = ["Yes","No"]

      parent.currentCondition = random.choice(parent.prm['conditions'])
      if parent.currentCondition == 'Yes':
          parent.correctButton = 1
      elif parent.currentCondition == 'No':
          parent.correctButton = 2

      freq    = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Frequency (Hz)")]
      dur     = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Duration (ms)")]
      ramps   = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Ramps (ms)")]
      lev     = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Level (dB SPL)")]
      phase   = 0
      channel = parent.prm[currBlock]['chooser'][parent.prm['chooserLabel'].index(parent.tr("Channel:"))]
   
      if parent.currentCondition == 'No':
          lev = -200
      sig = pureTone(freq, phase, lev, dur, ramps, channel, parent.prm['sampRate'], parent.prm['maxLevel'])

 
      parent.playSequentialIntervals([sig])
   

For experiments using the "Constant 1-Interval 2-Alternatives" paradigm
it is necessary to list the experimental conditions in the ``doTrial_``
function. We do this on line 6. On line 8, we bind the response buttons
to the correct response. Since the button number 1 is the "Yes" button, we 
say that in the case of a signal trial (``parent.currentCondition == "Yes"``)
the correct button to press is the button number 1, otherwise the correct button to press is the button number 2.

On lines 14-23 we read off the values of the text fields and generate the
sound to play (signal or silence) according to the experimental condition. 
Finally, on line 25 we use the ``parent.playSequentialIntervals`` function to
present the sound to the listener. This function accepts as an argument a
list of sounds to play sequentially. In our case we have only a single
sound to insert in the list. More details on the ``playSequentialIntervals``
function are provided in Section :ref:`sec-play_sound_functions`.


Writing an experiment for the Transformed Up-Down Interleaved, Weighted Up-Down Interleaved, and Multiple Constants m-Intervals n-Alternatives Paradigms
========================================================================================================================================================

This section will walk you through an example of an experiment that can be
used with the transformed up-down interleaved and weighted up-down interleaved
paradigms. These paradigms are simple extensions of the transformed up-down and
weighted up-down paradigms in which multiple independent adaptive tracks are
run simultaneously and are randomly interleaved in a single block of trials.

Because experiments that support
the transformed up-down interleaved and weighted up-down interleaved
paradigms can be easily modified to support also the multiple constants m-intervals n-alternatives
paradigm, this paradigm will be also added in our example experiment. This paradigm is a simple
extension of the constant m-intervals n-alternatives paradigm, in which rather than having a single
constant difference between the standard and comparison tones, multiple constant differences are
tested in a single block of trials.

The example experiment that we'll look at is a simple signal detection in quiet experiment, that could be used
to measure an audiogram. For this reason it is called "Demo Audiogram Multiple Frequencies" (it can be
found in the file ``audiogram_mf.py`` in the ``default_experiments`` folder). The experiment can
be used to setup a virtually unlimited number of adaptive tracks, and each track can be used to track the signal-detection
threshold for a specific frequency.

As for the multiple constants procedure, the experiment could be similarly used to measure percent correct performance
for tones of different frequencies presented at the same level. However, a more interesting possibility is to use the
experiment to measure percent correct performance for the same frequency at different fixed levels. This could then be
used to derive a psychometric function relating percent correct performance to signal level.

The ``initialize_`` function of the experiment is shown below:

.. code-block:: python
   :linenos:
   
   def initialize_audiogram_mf(prm):
      exp_name = QApplication.translate("","Demo Audiogram Multiple Frequencies","")
      prm["experimentsChoices"].append(exp_name)
      prm[exp_name] = {}
      prm[exp_name]["paradigmChoices"] = [QApplication.translate("","Transformed Up-Down Interleaved",""),
                                        QApplication.translate("","Weighted Up-Down Interleaved",""),
                                        QApplication.translate("","Multiple Constants m-Intervals n-Alternatives","")]
                                                                                                   
                                                                                                   
      prm[exp_name]["opts"] = ["hasISIBox", "hasAlternativesChooser", "hasFeedback",
                             "hasNTracksChooser"]
      prm[exp_name]['defaultAdaptiveType'] = QApplication.translate("","Arithmetic","")
      prm[exp_name]['defaultNIntervals'] = 2
      prm[exp_name]['defaultNAlternatives'] = 2
      prm[exp_name]['defaultNTracks'] = 4
    
      prm[exp_name]["execString"] = "audiogram_mf"
      prm[exp_name]["version"] = "1"
    
    return prm
   
the first part of the function doesn't need much explanation if you've follwed the previous examples.
The experiments ``opts`` has a new item ``hasNTracksChooser``. This option allows the user to dynamically
change the number of adaptive tracks to be used (or the number of constant differences to measure for the
multiple constants paradigm). Besides this, the only new thing compared to previous examples is that
we also specify the default number of tracks with ``prm[exp_name]['defaultNTracks'] = 4``.

The ``select_default_parameters_`` for the "Demo Audiogram Multiple Frequencies" experiment is shown
below:
    
.. code-block:: python
   :linenos:
      
   def select_default_parameters_audiogram_mf(parent, par):
   
      nDifferences = par['nDifferences']
   
      field = []
      fieldLabel = []
      chooser = []
      chooserLabel = []
      chooserOptions = []

      for i in range(nDifferences):
         fieldLabel.append(parent.tr("Frequency (Hz) " + str(i+1)))
         field.append(1000+1000*i)
         fieldLabel.append(QApplication.translate("","Level (dB SPL) " + str(i+1),""))
         field.append(50)
    
      fieldLabel.append(QApplication.translate("","Bandwidth (Hz)",""))
      field.append(10)
    
      fieldLabel.append(QApplication.translate("","Duration (ms)",""))
      field.append(180)
    
      fieldLabel.append(QApplication.translate("","Ramps (ms)",""))
      field.append(10)

    
      chooserOptions.append([QApplication.translate("","Right",""),
                           QApplication.translate("","Left",""),
                           QApplication.translate("","Both","")])
      chooserLabel.append(QApplication.translate("","Ear:",""))
      chooser.append(QApplication.translate("","Right",""))
      chooserOptions.append([QApplication.translate("","Sinusoid",""),
                           QApplication.translate("","Narrowband Noise","")])
      chooserLabel.append(QApplication.translate("","Type:",""))
      chooser.append(QApplication.translate("","Sinusoid",""))

      prm = {}
      prm['field'] = field
      prm['fieldLabel'] = fieldLabel
      prm['chooser'] = chooser
      prm['chooserLabel'] = chooserLabel
      prm['chooserOptions'] =  chooserOptions

      return prm

The transformed/weighted up-down interleaved paradigms can be run with any
number of adaptive tracks. Similarly, the multiple constants m-intervals
n-alternatives procedure can be run with any number of constant differences
between the standard and comparison intervals. All the user has to do is
select the desired number of adaptive tracks, or constant differences
from the appropriate chooser in the ``pychoacoustics`` control window.
``select_default_parameters_`` function, however, needs to know how
many tracks or how many constant differences are being run in order to set
up the necessary fields storing the experimental variables.
The ``par`` argument that is always passed to the ``select_default_parameters_``
function has the purpose of passing additional parameters to dinamycally modify
the behavior of the function in cases like this.

In the case of paradigms with interleaved tracks, or multiple constant differences
the ``par`` argument has a key called ``nDifferences`` that specifies the
number of tracks or constant differences. For the current experiment we
retieve this value on line 3. Then, on lines 11-15 we set up a for loop
in which we add a field to store the frequency and level of the tones for
each adaptive track. The rest of the function is similar to previous examples,
so it will not be discussed further.

The ``get_fields_to_hide_`` function for the "Demo Audiogram Multiple Frequencies"
experiment is shown in the code block below. Again, nothing new here.
      
.. code-block:: python
   :linenos:
      
   def get_fields_to_hide_audiogram_mf(parent):
      if parent.chooser[parent.prm['chooserLabel'].index(QApplication.translate("","Type:",""))].currentText() == QApplication.translate("","Sinusoid",""):
         parent.fieldsToHide = [parent.prm['fieldLabel'].index(QApplication.translate("","Bandwidth (Hz)",""))]
      else:
         parent.fieldsToShow = [parent.prm['fieldLabel'].index(QApplication.translate("","Bandwidth (Hz)",""))]

The ``doTrial_`` function for the "Demo Audiogram Multiple Frequencies" experiment
is shown below:	 

.. code-block:: python
   :linenos:
   
   def doTrial_audiogram_mf(parent):
      currBlock = 'b'+ str(parent.prm['currentBlock'])
      nDifferences = parent.prm['nDifferences']
      if parent.prm['startOfBlock'] == True:
         parent.prm['additional_parameters_to_write'] = {}
         parent.prm['conditions'] = []
         parent.prm['adaptiveParam'] = []
         for i in range(nDifferences):
            parent.prm['conditions'].append(str(parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(QApplication.translate("","Frequency (Hz) " + str(i+1),""))]))
            parent.prm['adaptiveParam'].append(parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(QApplication.translate("","Level (dB SPL) " + str(i+1),""))])
         parent.writeResultsHeader('log')

      frequency = []
      for i in range(nDifferences):
         frequency.append(parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(QApplication.translate("","Frequency (Hz) " + str(i+1),""))])

      parent.currentCondition = parent.prm['conditions'][parent.prm['currentDifference']] #this is necessary for counting correct/total trials
      correctLevel = parent.prm['adaptiveParam'][parent.prm['currentDifference']]
    
      currentFrequency = frequency[parent.prm['currentDifference']]
      bandwidth = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(QApplication.translate("","Bandwidth (Hz)",""))] 
      phase = 0
    
      incorrectLevel = -200
      duration = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(QApplication.translate("","Duration (ms)",""))] 
      ramps = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index(QApplication.translate("","Ramps (ms)",""))] 
      channel = parent.prm[currBlock]['chooser'][parent.prm['chooserLabel'].index(QApplication.translate("","Ear:",""))]
      sndType = parent.prm[currBlock]['chooser'][parent.prm['chooserLabel'].index(QApplication.translate("","Type:",""))]

      if sndType == QApplication.translate("","Narrowband Noise",""):
         if bandwidth > 0:
            parent.stimulusCorrect = steepNoise(currentFrequency-(bandwidth/2), currentFrequency+(bandwidth/2), correctLevel - (10*log10(bandwidth)),
                                                duration, ramps, channel, parent.prm['sampRate'], parent.prm['maxLevel'])
         else:
            parent.stimulusCorrect = pureTone(currentFrequency, phase, correctLevel, duration, ramps, channel, parent.prm['sampRate'], parent.prm['maxLevel'])
      elif sndType == QApplication.translate("","Sinusoid",""):
         parent.stimulusCorrect = pureTone(currentFrequency, phase, correctLevel, duration, ramps, channel, parent.prm['sampRate'], parent.prm['maxLevel'])
      
            
      parent.stimulusIncorrect = []
      for i in range((parent.prm['nIntervals']-1)):
         thisSnd = pureTone(currentFrequency, phase, incorrectLevel, duration, ramps, channel, parent.prm['sampRate'], parent.prm['maxLevel'])
         parent.stimulusIncorrect.append(thisSnd)
      parent.playRandomisedIntervals(parent.stimulusCorrect, parent.stimulusIncorrect)


note that on line 3 we retrieve the number of adaptive tracks (for adaptive interleaved
paradigms), or the number of constant differences (for multiple constant paradigms) that
we're currently running. This parameter is stored in the ``parent.prm`` dictionary.

At the start of a block of trials (cfr. line 4) we set up a number of parameters.
Among these there are two in particular that need some explanation. The
``parent.prm['adaptiveParam'] on line 7 is a list that is populated in the for loop
starting on line 9 with the initial values of the parameter that is adaptively varying
for each track. The ``parent.prm['conditions'] on the other hand is a parameter
that is used only when the experiment is run with the multiple constants m-intervals
n-alternatives paradigm. It's a list of labels for each "condition" that is being
run in the experiment, that is for each constant difference that is being tested.

On lines 13-15 we retrieve the frequencies of the tones used for each track or
constant difference.

On line 17 we retrieve the label of the current condition and store it in the
``parent.currentCondition`` variable. Thisvariable will be used by ``pychoacoustics``
for keeping count of the correct and total number of trials for each constant
difference when using the multiple constants paradigm. Note how the
``parent.prm['currentDifference']`` variable is used for this purpose. This variable
is the index to the current track or current cosnatnt difference that is being
currently tested. This variable is set outside of the ``doTrial_`` function,
(a random track or constant difference is chosen for each trial) but
we can retrieve its value through the ``parent`` handle.

On line 18 we make use of the ``parent.prm['currentDifference']`` variable again, this
time to retrieve the level of the comparison stimulus for the track or constant difference
that is run on the current trial. The rest of the function is not different from
the ``doTrial_`` functions used in transformed/weighted up-down paradigms with
non-interleaved tracks, and should be easy to follow if you've followed the previous
examples.


Writing a matching experiment using interleaved adaptive tracks
---------------------------------------------------------------

The transformed up-down and weighted up-down interleaved procedures can be used
to write matching experiments. As described by [Jesteadt1980]_, two interleaved
adaptive tracks can be used to target points on the psychometric function that
are symmetric around the 50% point (e.g. 71% and 29%), and then average the
threshold in each track in order to estimate the point of subjective equality.
For example, in a level-matching experiment one track could target the point
at which the listener judges the comparison tone to be louder than the standard
tone 71% of the time, while the other track targets the point at which the listener
judges the comparison tone to be louder than the standard 29% of the time (or equivalently,
softer than the standard 71% of the time).

In this section we'll show how to write in ``pychoacoustics`` a level-matching
experiment similar to the one described by [Jesteadt1980]_. This experiment is
one of the default experiments available in ``pychoacoustics``, and is called
``Demo Level Matching``.

The ``initialize_`` function of the experiment is shown in the code block below.

.. code-block:: python
   :linenos:

   def initialize_lev_match(prm):
      exp_name = "Demo Level Matching"
      prm["experimentsChoices"].append(exp_name)
      prm[exp_name] = {}
      prm[exp_name]["paradigmChoices"] = ["Transformed Up-Down Interleaved",
                                          "Weighted Up-Down Interleaved"]

      prm[exp_name]["opts"] = ["hasISIBox", "hasAlternativesChooser"]
      prm[exp_name]['defaultAdaptiveType'] = QApplication.translate("","Arithmetic","")
      prm[exp_name]['defaultNIntervals'] = 2
      prm[exp_name]['defaultNAlternatives'] = 2
      prm[exp_name]['defaultNTracks'] = 2
      prm[exp_name]["execString"] = "lev_match"

among the ``paradigmChoices`` we include the "Transformed Up-Down Interleaved",
and the "Weighted Up-Down Interleaved". The experiment has just two experiment ``opts``:
one to add an ISI box, the other one to add an alternatives chooser (we'll probably want to
run this experiment only with two intervals, and two alternatives, so in principle we could
do without the alternative chooser, but currently, for technical reasons the ``hasAlternativesChooser``
option has to be added with the "Transformed Up-Down Interleaved", and the "Weighted Up-Down Interleaved"
paradigms). Besides specifying the default number of intervals and alternatives,
we also specify the default number of interleaved tracks using the ``defaultNTracks`` key. Because we
have not added a ``hasNTracksChooser`` in the experiment the default number of tracks specified here
will be the default and only possible number of tracks in the experiment.

The ``select_default_parameters_`` function is shown below:

.. code-block:: python
   :linenos:
      
   def select_default_parameters_lev_match(parent, par):
   
      field = []
      fieldLabel = []
      chooser = []
      chooserLabel = []
      chooserOptions = []

      fieldLabel.append("Starting Level Track 1 (dB SPL)")
      field.append(75)

      fieldLabel.append("Starting Level Track 2 (dB SPL)")
      field.append(55)

      fieldLabel.append(parent.tr("Frequency Standard Tone (Hz)"))
      field.append(1000)

      fieldLabel.append(parent.tr("Frequency Comparison Tone (Hz)"))
      field.append(250)

      fieldLabel.append(parent.tr("Level Standard Tone (dB SPL)"))
      field.append(65)

      fieldLabel.append(parent.tr("Duration (ms)"))
      field.append(180)
    
      fieldLabel.append(parent.tr("Ramps (ms)"))
      field.append(10)

      chooserOptions.append(["Right", "Left", "Both"])
      chooserLabel.append(QApplication.translate("","Ear:",""))
      chooser.append(QApplication.translate("","Both",""))

    
      prm = {}
      prm['field'] = field
      prm['fieldLabel'] = fieldLabel
      prm['chooser'] = chooser
      prm['chooserLabel'] = chooserLabel
      prm['chooserOptions'] =  chooserOptions

      return prm

the first two fields will be used to set the starting level of the comparison tone in each track.
The next two fields will be used to set the frequencies of the standard and comparison tone. The
next field will be used to set the level of the standard tone which will be fixed throughout a block
of trials. The last two fields will be used to set the duration of the tone (excluding the ramps),
and the duration of its onset and offset ramps. The only chooser will be used to set the ear to
which the tones will be presented.


The ``doTrial_`` function for the level matching experiment is shown below:

.. code-block:: python
   :linenos:

   def doTrial_lev_match(parent):
      currBlock = 'b'+ str(parent.prm['currentBlock'])
      if parent.prm['startOfBlock'] == True:
         parent.prm['adaptiveParam'] = []
         parent.prm['adaptiveParam'].append(parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Starting Level Track 1 (dB SPL)")])
         parent.prm['adaptiveParam'].append(parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Starting Level Track 2 (dB SPL)")])
         parent.writeResultsHeader('log')


  
     standardFrequency = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Frequency Standard Tone (Hz)")]
     comparisonFrequency = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Frequency Comparison Tone (Hz)")]
     standardLevel = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Level Standard Tone (dB SPL)")]
     duration = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Duration (ms)")] 
     ramps = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Ramps (ms)")]
     phase = 0
     channel = parent.prm[currBlock]['chooser'][parent.prm['chooserLabel'].index("Ear:")]

     comparisonLevel = parent.prm['adaptiveParam'][parent.prm['currentDifference']]

     comparisonTone = pureTone(comparisonFrequency, phase, comparisonLevel, duration, ramps,
                               channel, parent.prm['sampRate'], parent.prm['maxLevel'])

     standardToneList = []
     for i in range((parent.prm['nIntervals']-1)):
        thisSnd = pureTone(standardFrequency, phase, standardLevel, duration, ramps, channel,
                           parent.prm['sampRate'], parent.prm['maxLevel'])
        standardToneList.append(thisSnd)
     parent.playRandomisedIntervals(comparisonTone, standardToneList)

The adaptive parameter for an experiment with interleaved tracks is not a single number, but a list
containing the values of the adaptive parameter for each track. Therefore,
on line 4 we create the list, and on lines 5 and 6 we populate
this list with the initial values of each of the adaptive tracks.

From lines 11 to 17 we retrieve the values of all the fields and choosers. Nothing new here.
On line 19 we retrieve the value of the adaptive parameter (which in this case is the level
of the comparison tone) for the current trial. To do this, we refer to a key in the ``parent.prm``
dictionary called ``currentDifference``. This key holds the index of the track which
has been randomly selected by ``pychoacoustics`` for the current trial.

From line 21 to 28 we prepare the stimuli to be presented in the standard and comparison intervals.
We then pass these stimuli as arguments to the ``playRandomisedIntervals`` functions. This experiment is ready to be run.

The up-down rules of the two adaptive tracks need to be set up
appropriately to run the matching experiment. Let's,
take as an example the experiment described in [Jesteadt1980]_ in
which we wish to determine the intensity of a 250-Hz tone required
to match the loudness of a 1000-Hz tone presented at 40 dB SPL.
In the ``pychoacoustics`` control window, after having selected
the ``Demo Level Matching`` experiment, we set the frequency of
the standard tone to 1000 Hz, and the frequency of the comparison
tone to 250 Hz. We also set the level of the standard tone to 40 dB SPL.
We then set the upper, and lower tracks to 60 and 30 dB SPL, two values
that should bracket the point of subjective equality.

The task for the
listener is an objective one: s/he will have to tell on each trial
which tone was louder. For track 1, we set the rule down to 2, and the
rule up to 1. For track 2 instead, we set the rule down to 1, and the
rule up to 2. In this way, track 1 will target the point in the
psychometric function at which the listener judges the comparison
tone to be louder than the standard 70.7% of the time. Track 2 will
target instead the point in the psychometric function at which the
listener judges the comparison tone to be louder than the standard
29.3% of the time. For track 1, when the listener chooses the *comparison*
interval twice in a row the level of the 250-Hz tone (the comparison tone)
is decreased, while each time s/he chooses the standard interval the level of the
250-Hz tone is increased.
For track 2, when the listener chooses the *standard*
interval twice in a row the level of the 250-Hz tone is increased, while each
time the listener chooses the level of the 250-Hz tone is decreased.
For both tracks "correct" responses move the track down. There are no
correct or incorrect responses in a subjective task like this. The ``Corr. Resp. Move Track X`` (down or up) choosers are not named appropriately for this task.
They should be named something like "when the comparison interval is chosen
track X moves" down or up. However, since the underlying code for adaptive
interleaved paradigms is the same for objective and subjective tasks,
for simplicity and ease of maintenance of the underlying code they are called
``Corr. Resp. Move Track X`` (down or up). 
.

Writing a "Constant 1-Pair Same/Different" Paradigm Experiment
==============================================================

.. todo::
  
   Describe of to write experiments for the "Constant 1-Pair Same/Different" paradigm.

Writing an "Odd One Out" Paradigm Experiment
============================================

.. todo::
  
   Describe of to write experiments for the "Odd One Out" paradigm.
   

.. _sec-experiment_opts: 

The Experiment “opts”
=====================

-  **``hasAlternativesChooser``** This option adds two chooser widgets, one to dynamically
   change the number of observation intervals (labelled "Intervals"), and one to dinamically 
   change the number of response alternatives (labelled "Alternatives). 
   This option is generally used in adaptive paradigms
   ("Transformed Up-Down", "Weighted Up-Down", as well as their interleaved versions). 
   The number of response alternatives that can be choosen from the widget can be either
   equal to the number of observation intervals, or to the number of observation intervals
   minus one. In the latter case the standard stimulus is presented in the first interval, 
   as a reference, with no corresponding response alternative, see [GrimaultEtAl2002]_ 
   for an example of this :math:`n`-intervals, :math:`n-1` alternatives presentation
   mode. The selected number of intervals and alternatives can be accessed in the experiment
   file through the ``parent.prm['nIntervals']``, and ``parent.prm['nAlternatives']`` variables
   respectively.


-  **``hasAltReps``** This option can be used to change the way in which the 
   stimuli are presented in the "Transformed Up-Down" paradigm or 
   other adaptive paradigms. In these paradigms, normally there is an 
   observation interval containing the target stimulus (comparison interval), 
   and one or more other intervals containing the non-target stimuli (standard 
   intervals). An alternative way to present the stimuli is to have an alternation
   of the target and non-target stimuli (e.g. ABAB) in the comparison interval,
   and a repetition of the non-target stimulus in the standard interval (AAAA)
   [KingEtAl2013]_. If the ``hasAltReps`` option is enabled, there will be two
   additional text boxes, ``Alternated (AB) Reps.`` and ``Alternated (AB) Reps. ISI (ms)``.
   The first text box controls the number of times the alternated target and non-target
   stimuli should be repeated, a value of zero corresponds to no alternation, that is
   only a single stimulus (either the target, or the non target) is presented in each interval.
   If the value is one, a single alternation will occur (AB), if the value is two, two alternations
   occur (ABAB), and so on. The second text box controls the ISI between the stimuli
   presented within an interval. The selected number of alternated repetitions, 
   and the ISI between alternating stimuli can be accessed in the experiment file
   through the ``parent.prm['altReps']``, and ``parent.prm['altRepsISI']`` variables
   respectively. The setup of the alternated repetitions must be done within each
   experiment file.

-  **``hasFeedback``** This option controls whether the "Response Light" chooser has
   a "Feedback" option or not. You may want to enable this option for all "objective"
   experiments that have a clear "correct" response. You may want to disable this option
   for "subjective" experiments, such as matching experiments, in which there is no
   "correct" response.

-  **``hasISIBox``** If this option is enabled, a box labelled ``ISI (ms)`` is
   added. This is generally used to set the silent period between observation 
   intervals in the "Transformed Up-Down" and similar adaptive procedures. 
   Its value can be accessed in the experiment file through the 
   ``parent.prm['isi']`` variable. However, normally this should not be
   necessary because the ``playRandomisedIntervals`` function automatically
   uses this value to set the silent period between observation intervals.

-  **``hasNDifferencesChooser``** This option is useful in the 
   "Multiple Constants 1-Interval 2-Alternatives Paradigm" to dinamically
   change the number of experimental conditions. For example, if you have
   a signal detection experiment in which a fixed number of signals (with
   a constant amplitude) can occur, this option allows to choose the
   number of conditions dinamically. If this option is enabled, a chooser
   labelled ``No. Alternatives`` is added. The value selected can be accessed
   through the ``par['nDifferences']`` variable in the 
   ``select_default_parameters_`` function, and through the 
   ``parent.prm['nDifferences']`` variable in the ``doTrial`` function.

-  **``hasNTracksChooser``** This option can be used to dinamically change
   the number of tracks in interleaved adaptive paradigms (e.g. "Transformed
   Up-Down Interleaved). If enabled, a ``No. Tracks`` chooser is added.
   The value selected can be accessed
   through the ``par['nDifferences']`` variable in the 
   ``select_default_parameters_`` function, and through the 
   ``parent.prm['nDifferences']`` variable in the ``doTrial`` function.

-  **``hasPrecursorInterval``** If this option is enabled, a chooser controlling whether
   a precursor interval should be presented or not is added. This chooser is labelled
   ``Precursor Interval``. If this option is enabled, and the chooser is set to "Yes",
   then a ``precursorStim`` sound needs to be passed to the ``playRandomisedIntervals``
   function. This sound will be presented before each observation interval. 

-  **``hasPostcursorInterval``** If this option is enabled, a chooser controlling whether
   a postcursor interval should be presented or not is added. This chooser is labelled
   ``Postcursor Interval``. If this option is enabled, and the chooser is set to "Yes",
   then a ``postcursorStim`` sound needs to be passed to the ``playRandomisedIntervals``
   function. This sound will be presented after each observation interval.

-  **``hasPreTrialInterval``** If this option is enabled, a chooser controlling whether
   a pre-trial interval should be presented or not is added. This chooser is labelled
   ``Pre-Trial Interval``. If this option is enabled, and the chooser is set to "Yes",
   then a ``preTrialStim`` sound needs to be passed to the ``playRandomisedIntervals``
   function. This sound will be presented at the beginning of each trial. 


.. _sec-play_sound_functions:


The Play Sound Functions
========================

.. todo::
  
   Illustrate the functions to play sounds

.. _sec-simulations:


Simulations
===========

 ``pychoacoustics`` is not designed to run simulations in itself, however it provides a hook to redirect the control flow to an auditory model that you need to specify yourself in the experiment file.  You can retrieve the current response mode from the experiment file with:

.. code-block:: python
   :linenos:

    
    parent.prm['allBlocks']['responseMode']

so, in the experiment file, after the creation of the stimuli for the trial you can redirect the control flow of the program depending on the response mode:

.. code-block:: python
   :linenos:

    
    if parent.prm['allBlocks']['responseMode'] != "Simulated Listener":
       #we are not in simulation mode, play the stimuli for the listener
       parent.playSoundSequence(sndSeq, ISIs)
    if parent.prm['allBlocks']['responseMode'] == "Simulated Listener":
       #we are in simulation mode
       #pass the stimuli to an auditory model and decision device
       #---
       #Here you specify your model, pychoacoustics doesn't do it for you!
       # at the end your simulated listener arrives to a response that is
       # either correct or incorrect
       #---
       parent.prm['trialRunning'] = False 
       #this is needed for technical reasons (if the 'trialRunning'
       #flag were set to 'True' pychoacoustics would not process
       #the response.
       #
       #let's suppose that at the end of the simulation you store the
       #response in a variable called 'resp', that can take as values 
       #either the string 'Correct' or the string 'Incorrect'.
       #You can then proceed to let pychoacoustics process the response:
       #
       if resp == 'Correct':
          parent.sortResponse(parent.correctButton) 
       elif resp == 'Incorrect':
          #list all the possible 'incorrect' buttons
          inc_buttons = numpy.delete(numpy.arange(
                                     self.prm['nAlternatives'])+1, 
                                     self.correctButton-1))
          #choose one of the incorrect buttons
          parent.sortResponse(random.choice(inc_buttons))
