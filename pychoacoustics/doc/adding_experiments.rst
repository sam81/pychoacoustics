*****************************
Writing your own Experiments
*****************************

First Steps
==============

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

we’ll look at each function in details shortly. Briefly, the
``initialize_`` function is used to set some general parameters and
options for our experiment; the ``select_default_parameters_`` function
lists all the widgets (text fields and choosers) of our experiment and
their default values; finally, the ``doTrial_`` function contains the code that
generates the sounds and plays them during the experiment. 

The ``initialize_`` function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

 The ``initialize_`` function of our frequency discrimination experiment looks like this:

.. code-block:: python
   :linenos:

    
    def initialize_freq(prm):
      exp_name = "Frequency Discrimination Demo"
      prm["experimentsChoices"].append(exp_name)
      prm[exp_name] = {}
      prm[exp_name]["paradigmChoices"] = ["Transformed Up/Down",
                                          "Weighted Up/Down"]
    
      prm[exp_name]["opts"] = ["hasISIBox", "hasAlternativesChooser", 
                               "hasFeedback", "hasIntervalLights"]

      prm[exp_name]['defaultAdaptiveType'] = "Geometric"
      prm[exp_name]['defaultNIntervals'] = 2
      prm[exp_name]['defaultNAlternatives'] = 2
      prm[exp_name]["execString"] = "freq"
      prm[exp_name]["version"] = "1"

      return prm

When the function is called, it is passed a dictionary containing
various parameters through the ``prm`` argument. The function receives
this dictionary of parameters and adds or modifies some of them. On line 2
we give a label to the experiment, this can be anything we
want, except the label of an experiment already existing. On line 3
we add this experiment label to the list of “experimentsChoices”.
On line 4 we create a new sub-dictionary that has as a key the
experiment label. Next we list the paradims that our experiment
supports by creating a ``paradigmChoices`` key and giving the names of
the supported paradigms as a list. The paradims listed here must be
within the set of paradims  supported by ``pychoacoustics`` (see
Section :ref:`sec-paradigms` for a description of the paradigms currently
supported). In the next line we set an ``opts`` key containing a list
of options. The full list of options that can be set here is described
in details in Section :ref:`sec-experiment_opts`. In brief, for our
experiment we want to have a widget to set the ISI between presentation
intervals (``hasISIBox``), a widget to choose the number of response
alternatives (``hasAlternativesChooser``), a widget to set the feedback
on or off for a given block of trials (``hasFeedback``), and finally we
want lights to mark the observation intervals (``hasIntervalLights``).
Next, we specify ``defaultAdaptiveType``, the default type of adaptive 
track that will be selected when the experiment is loaded, this could be 
either "Geometric", or "Arithmetic". It can be later changed by the experimenter
in the control window.
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

The ``select_default_parameters_`` function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

 The ``select_default_parameters_`` function is the function in which you define all the widgets (text fields and choosers) needed for your experiment. For our frequency discrimination experiment, the function looks as follows:

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
initializing the function. The use of the "par" argument is discussed 
in Section :ref:`sec-par`.  From line three to line seven, we create a 
series of empty lists. The ``field`` and ``fieldLabel`` lists will hold 
the default values of our text field widgets, and their labels, respectively. 
The ``chooser`` and ``chooserLabel`` lists will likewise hold the default 
values of our chooser widgets, and their labels, while the ``chooserOptions`` 
list will hold  the possible values that our choosers can take. 
On lines 9 to 29 we populate these lists for our frequency discrimination experiment. 
From line 31 to line 36 we insert in the dictionary the
``field``, ``fieldLabel``, ``chooser``, ``chooserLabel`` and ``chooserOptions`` 
lists that we previously creaetd and populated. 


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
           parent.prm['adaptiveDifference'] = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Difference (%)")]
           parent.writeResultsHeader('log')

       frequency = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Frequency (Hz)")]
       level = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Level (dB SPL)")] 
       duration = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Duration (ms)")] 
       ramps = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Ramps (ms)")]
       channel = parent.prm[currBlock]['chooser'][parent.prm['chooserLabel'].index("Ear:")]
       phase = 0

       correctFrequency = frequency + (frequency*parent.prm['adaptiveDifference'])/100
       stimulusCorrect = pureTone(correctFrequency, phase, level, duration, ramps, channel, parent.prm['sampRate'], parent.prm['maxLevel'])
      
       stimulusIncorrect = []
       for i in range((parent.prm['nIntervals']-1)):
           thisSnd = pureTone(frequency, phase, level, duration, ramps, channel, parent.prm['sampRate'], parent.prm['maxLevel'])
           stimulusIncorrect.append(thisSnd)
       
       parent.playRandomisedIntervals(stimulusCorrect, stimulusIncorrect)

As you can see on the first line the ``doTrial_`` function is passed 
as an argument its ``parent``. This is important because the parent contains 
a dictionary with the parameters for the current experiment (``parent.prm``). 
The parameters for each stored block of the experiment are stored 
in the ``parent.prm`` dictionary with keys starting with ``b`` followed by 
the block number. For example ``parent.prm['b3']`` contains the parameters 
for the third stored block. The current block number is stored in 
``parent.prm['currentBlock']``, and on line 3 we retrieve the dictionary 
key for the current block. On line 4 we start an if block that is executed 
only at the first trial of each block. In this block we retrieve the % frequency 
difference between the standard and the comparison stimuli for the first trial, 
and we store it in the ``parent.prm['adaptiveDifference']`` variable. Since we're 
using an adaptive procedure, this variable will be automatically increased or decreased 
by ``pychoacoustics`` on successive trials on the bases of the responses 
given by the listener. On line 6 we tell ``pychoacoustics`` to write the header of the 'log' result files (see :ref:`sec-log_results_files`).

On lines 8-11 we read off the values of the text field widgets for the current block of trials. The values of these field widgets are stored in the list ``parent.prm[currBlock]['field']``, and we exploit the label of each text field widget to retrieve its index in the list. For example ``parent.prm['fieldLabel'].index("Frequency (Hz)")`` retrieves the index of the text widget that stores the frequency of the standard tone for the current block of trials. On line 12 we read off the value of the only chooser widget for the current block of trials. The values of chooser widgets are stored in the list ``parent.prm[currBlock]['chooser']``, and we exploit the label of each chooser widget to retrieve its index in the list as we did for text field widgets.


Our next step will be to generate the stimuli for the trial. In a `X`-Intervals task we have to generate `X` stimuli. The standard stimuli will have in our case always the same frequency, we retrieved its value on line 8 of our ``doTrial_`` function. If a listener presses the button corresponding to one of the the standard stimuli his response will be incorrect. For this reason we will store the standard stimuli in a list called ``stimulusIncorrect = []``. The comparison stimulus will be instead stored in a variable called ``stimulusCorrect``. The frequency of the comparison stimulus, which can vary from trial to trial, depending on the current value of ``parent.prm['adaptiveDifference']`` is computed on line 15. On line 16 we generate the stimulus using the ``pureTone`` function that is available in the ``sndlib`` module. Note that we need to pass the current samplig rate and the current maximum output level of our headphones (see :ref:`sec-edit_phones_dia`) to the ``pureTone`` function. Their values are stored respectively in the ``parent.prm['sampRate']`` and ``parent.prm['maxLevel']`` variables. On lines 18-21 we generate and store the standard stimuli in the ``stimulusIncorrect`` list. The number of standard stimuli to generate will be equal to the number of intervals minus one. The number of intervals is stored in the ``parent.prm['nIntervals']`` variable. Finally on line 23 we call the ``parent.playRandomisedIntervals`` function to play the stimuli. This function requires two arguments, the correct stimulus, and a list containing the incorrect stimuli. That's it, our frequency discrimination experiment is ready and we can test it on ``pychoacoustics``.

Adding support for the Constant Paradigm
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

So far our frequency discrimination experiment supports only two paradigms, "Adaptive" and "Weighted Up/Down" (which is just a variant of the adaptive paradigm).
Adding support for the constant paradigm, in which the frequency difference between the standard and comparison stimuli is fixed across a block of trials is easy.
All we need to do is add "Constant m-Intervals n-Alternatives" to the list of paradigms supported paradims in the ``initialize_`` function:

.. code-block:: python

   prm[exp_name]["paradigmChoices"] = ["Adaptive",
                                       "Weighted Up/Down",
                                       "Constant m-Intervals n-Alternatives"]

Now our frequency discrimination task supports also the constant paradigm.

Showing/Hiding Widgets Dynamically
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Often you may want to write a single experiment that can handle a number 
of different experimental conditions. This usually leads to a growing number 
of widgets in the experiment user interface that can be distracting. 
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

    
As for the other experiment functions we have discussed before, the actual name is the concatenation of a prefix, in this case
``get_fields_to_hide_``, and the name of the experiment file, in this case ``freq``.
As you can see on line 1, this function takes as an argument ``parent``, which contains the lists of widgets for the current experiment.
We need to tell the ``get_fields_to_hide_`` function that if the standard frequency is fixed, it should
show only the ``Frequency (Hz)`` text field, and hide the ``Min. Frequency (Hz)`` and ``Max. Frequency (Hz)``
text fields. Vice-versa, if the standard frequency is roved, it should show only the ``Min. Frequency (Hz)`` 
and ``Max. Frequency (Hz)`` text fields, and hide the ``Frequency (Hz)`` text field. On line 2 we start an if block which
will be executed if the value, retrieved by the ``currentText`` attribute, of the ``Standard Frequency`` chooser is
set to ``Fixed``. Note how we exploit once again the ``chooserLabel`` to find the index of the chooser we want 
with ``parent.prm['chooserLabel'].index("Standard Frequency:")``. Next, we define two lists, one containing the indexes
of the fields to hide ``parent.fieldsToHide``, and one containing the indexes of the fields to show ``parent.fieldsToShow``.
Once more we exploit the ``fieldLabel`` to retrieve the indexes of the fields we want to get (e.g. ``parent.prm['fieldLabel'].index("Min. Frequency (Hz)")``).
From line 6 to line 9 we handle the case in which the standard frequency is roved. The logic of the code is the same as for the fixed standard frequency
case.

To complete the experiment we need to add a couple of lines to the ``doTrial_`` function to handle the case in which the standard frequency is roved.
The new function is shown below:

.. code-block:: python
   :linenos:

   def doTrial_freq2(parent):
      currBlock = 'b'+ str(parent.prm['currentBlock'])
      if parent.prm['startOfBlock'] == True:
         parent.prm['adaptiveDifference'] = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Difference (%)")]
         parent.writeResultsHeader('log')

      frequency = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Frequency (Hz)")]
      minFrequency = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Min. Frequency (Hz)")]
      maxFrequency = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Max. Frequency (Hz)")]
      level = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Level (dB SPL)")] 
      duration = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Duration (ms)")] 
      ramps = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Ramps (ms)")]
      phase = 0
      channel = parent.prm[currBlock]['chooser'][parent.prm['chooserLabel'].index("Ear:")]
      stdFreq = parent.prm[currBlock]['chooser'][parent.prm['chooserLabel'].index("Standard Frequency:")]

      if stdFreq == "Roved":
         frequency = random.uniform(minFrequency, maxFrequency)
      correctFrequency = frequency + (frequency*parent.prm['adaptiveDifference'])/100
      stimulusCorrect = pureTone(correctFrequency, phase, level, duration, ramps, channel, parent.prm['sampRate'], parent.prm['maxLevel'])
            
      stimulusIncorrect = []
      for i in range((parent.prm['nIntervals']-1)):
         thisSnd = pureTone(frequency, phase, level, duration, ramps, channel, parent.prm['sampRate'], parent.prm['maxLevel'])
         stimulusIncorrect.append(thisSnd)
      parent.playRandomisedIntervals(stimulusCorrect, stimulusIncorrect)
   

On lines 8-9 we read off the minimum and maximum frequency values for the roved-standard case. On line 15 we retrieve the
value of the ``Standard Frequency:`` chooser. On lines 17-18 we state that if the value of the standard frequency chooser 
is equal to ``Roved``, then the standard frequency for that trial should be drawn from a uniform distribution ranging
from ``minFrequency`` to ``maxFrequency``. The rest of the function is unchanged. Note that we're using the a Python module
called ``random`` on line 18, so we need to add ``import random`` at the top of our ``freq.py`` file.

It is also possible to show/hide choosers. Let's extend the frequency-discrimination experiment by allowing for the possibility 
that the standard frequency is roved on a log scale (which in fact would be a better choice given the frequency scaling in the auditory
system). To do this, we first add a new chooser to set the roving scale:

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
and adds the ``Roving Scale`` chooser to the ``parent.choosersToHide`` list.  Line 11 instead gets executed 
if the ``Standard Frequency`` chooser is set to ``Roved``, and adds the ``Roving Scale`` chooser to the ``parent.choosersToShow`` list.

Finally, we need to add/modify a couple of lines to the ``doTrial_`` function. 
First of all we need to read off the value of the new ``Roving Scale`` chooser:

.. code-block:: python
      
    rovingScale = parent.prm[currBlock]['chooser'][parent.prm['chooserLabel'].index("Roving Scale:")]

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
"Constant 1-Interval 2-Alternatives" paradigm. The experiment is simple "Yes/No" signal
detection task. On each trial the listener is presented with a single interval which may
or may not contain a sinusoid, and s/he has to tell if the signal was present or not.

The ``initialize_`` function for the signal detection experiment is shown below, since the
general framework for writing an experiment is the same, only the differences from an adaptive-paradigm
experiment will be highlited.

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

On line 5 we list the available paradigms for the experiment, in this case the only paradigm possible is ``Constant 1-Interval 2-Alternatives``. On line 7 we insert ``hasFeedback`` to the list of experiment options, so that feedback can be provided at the end of each trial. Since we'll have a single observation interval we don't add the ``hasISIBox`` option, because we don't need to have a silent inteval between observation intervals. On line 7, we set the labels for the buttons, which represent the two response alternatives: "Yes" or "No". On line 8 and line 9 we set the number of intervals and the number of response alternatives. 

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
paradigms that we have seen before. We set the text fields that we need
to set the frequency duration and level of the signal. We also set
a chooser to set the channels on which the signal should be presented.

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
   

For experiments using the "Constant 1-Interval 2-Alternatives" paradigm,
it is necessary to list the experimental conditions in the ``doTrial_``
finction. We do this on line 6. On line 8, we bind the response buttons
to the correct response. Since the button number 1 is the "Yes" button, we 
say that in the case of a signal trial (``parent.currentCondition == "Yes"``)
the correct button to press is the button number 1, otherwise the correct button to press is the button number 2.

On lines 14-23 we read off the values of the text fields and generates the
sound to play (signal or silence) according to the experimental condition. 
Finally, on line 25 we use the ``parent.playSequentialIntervals`` function to
present the sound to the listener. This function accepts as an argument a
list of sounds to play sequentially. In our case we have only a single
sound to insert in the list. More details on the ``playSequentialIntervals``
function are provided in Section XY.

.. _sec-experiment_opts: 

The Experiment “opts”
^^^^^^^^^^^^^^^^^^^^^

-  ``hasISIBox``

-  ``hasAlternativesChooser``

-  ``hasFeedback``

-  ``hasIntervalLights``

-  ``hasPreTrialInterval``

-  ``hasAltReps``

 
.. _sec-par:

Using ``par``
^^^^^^^^^^^^^



.. _sec-simulations:

Simulations
=============

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
