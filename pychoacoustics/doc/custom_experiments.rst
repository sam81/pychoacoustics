Designing Custom Experiments
============================

In order to add a new experiment to ``pychoacoustics``, create a directory in your home folder called ``pychoacoustics_exp``, inside this folder create a subfolder called ``labexp``. Each experiment is written in a single file contained in this folder. Let’s imagine we want to create an experiment for a frequency discrimination task. We create a file named ``freq.py`` in the ``labexp`` folder. In addition to the experiment file we need an additional file that lists all the experiments contained in the ``labexp`` directory. This file must be named ``__init__.py``, and in our case it will have the following content:

.. code-block:: python
    
    __all__ = ["freq"]

here the variable ``__all__`` is simply a python list with the
name of the experiment files. So, if one day we decide to write a new
experiment on, let’s say, level discrimination, in a file called
``lev.py`` we would simply add it to the list in ``__init__.py``:

.. code-block:: python
    
    __all__ = ["freq",
               "lev"]

For people familiar with packaging Python modules it should be clear
by now that the custom experiments folder is basically a Python package
containing various modules (the experiment files). If at some point we
want to remove an experiment from ``pychoacoustics``, for example
because it contains a bug that does not allow the program to start, we
can simply remove it from the list in ``__init__.py``.  Let’s go back
to the ``freq.py`` file. Here we need to define four functions. For our
example the names of these functions would be:

.. code-block:: python
    
    initialize_freq()
    select_default_parameters_freq()
    get_fields_to_hide_freq()
    doTrial_freq()

basically the function names consist of a fixed prefix, followed by
the name of the experiment file. So in the case of the level experiment
example, written in the file ``lev.py``, the four functions would be
called:


.. code-block:: python
    
    initialize_lev()
    select_default_parameters_lev()
    get_fields_to_hide_lev()
    doTrial_lev()

we’ll look at each function in details shortly. Briefly, the
``initialize_`` function is used to set some general parameters and
options for our experiment; the ``select_default_parameters_`` function
lists all the widgets (text fields and choosers) of our experiment and
their default values; the ``get_fields_to_hide_`` function is used to
dinamically hide or show certain widgets depending on the status of
other widgets; finally, the ``doTrial_`` function contains the code that
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
      prm[exp_name]["paradigmChoices"] = ["Adaptive",
                                          "Weighted Up/Down",
                                          "Constant m-Intervals n-Alternatives"]
    
      prm[exp_name]["opts"] = ["hasISIBox", "hasAlternativesChooser", 
                               "hasFeedback", "hasIntervalLights"]
        
      prm[exp_name]["execString"] = "freq"
      return prm

When the function is called, it is passed a dictionary containing
various parameters through the “prm” argument. The function receives
this dictionary of parameters and adds or modifies some of them. On line 2
we give a label to the experiment, this can be anything we
want, except the label of an experiment already existing. On line 3
we add this experiment label to the list of “experimentsChoices”.
On line 4 we create a new sub-dictionary that has as a key the
experiment label. Next we list the paradims that our experiment
supports by creating a “paradigmChoices” key and giving the names of
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
The penultimate line of the ``initialize_`` function sets the
“``execString``” of our experiment. This must be the name of our
experiment file, so in our case “``freq``”.   

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
      if paradigm == None:
          prm['paradigm'] = "Adaptive"
      else:
          prm['paradigm'] = paradigm
      prm['adType'] =  "Geometric"
      prm['field'] = field
      prm['fieldLabel'] = fieldLabel
      prm['chooser'] = chooser
      prm['chooserLabel'] = chooserLabel
      prm['chooserOptions'] =  chooserOptions
      prm['nIntervals'] = 2
      prm['nAlternatives'] = 2
    
      return prm

The ``select_default_parameters_`` function accepts three arguments, “parent” is simply a reference to the pychoacoustics application, “paradigm” is the paradigm with which the function has been called, while “par” is a variable that can hold some special values for initializing the function. The use of the
“par” argument is discussed in Section :ref:`sec-par`.  From line three to line seven, we create a series of empty lists. The ``field`` and ``fieldLabel`` lists will hold the default values of our text field widgets, and their labels, respectively. The ``chooser`` and ``chooserLabel`` lists will likewise hold the default values of our chooser widgets, and their labels, while the ``chooserOptions`` list will hold  the possible values that our choosers can take. On lines 9 to 29 we populate these lists for our frequency discrimination experiment. The last lines of our ``select_default_parameters_`` function are
used to set some additional parameters. On line 31 we create a dictionary to hold the parameters. On lines 32–35 we set a default paradigm for our experiment if ``None`` has been passed to our function. On line 36 ``adType`` sets the default type of the adaptive procedure, this could be either ``Geometric``, or ``Arithmetic``. From line 37 to line 41 we insert in the dictionary the
``field``, ``fieldLabel``, ``chooser``, ``chooserLabel`` and ``chooserOptions`` lists that we previously creaetd and populated. Finally, on lines 42-43, we give the default number of response intervals and response alternatives. 


The ``get_fields_to_hide_`` function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  The purpose of the ``get_fields_to_hide_`` function is to dinamically show or hide certain widgets depending on the status of other widgets. This function must be defined, but is not essential to a ``pychoacoustics`` experiment, so if you want to read all the essential information first, you can simply define the function as follows:

.. code-block:: python

    
    def get_fields_to_hide_freq(parent):
      pass

and move on to read about the next function, otherwise, read on. 
Let’s suppose that you  want to set up a frequency discrimination
experiment in which the frequency of the  standard stimulus may be
either fixed, or change from trial to trial. You start by writing an
experiment with a single “Frequency” text field for the fixed stimulus
frequency case. You then add two additional fields called “Min.
Frequency” and “Max Frequency” to set the range of frequencies in the
roving frequency case. Finally, you create a chooser to decide whether
an experiment is to be run with a fixed or roving frequency. The code
for creating these widgets is shown below:   

The ``doTrial_`` function
^^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: python
   :linenos:

   def doTrial_freq(parent):

      currBlock = 'b'+ str(parent.prm['currentBlock'])
       if parent.prm['startOfBlock'] == True:
           parent.prm['additional_parameters_to_write'] = {}
           parent.prm['adaptiveDifference'] = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Difference (%)")]
           parent.prm['conditions'] = [str(parent.prm['adaptiveDifference'])]

           parent.writeResultsHeader('log')
       parent.currentCondition = parent.prm['conditions'][0]

       frequency = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Frequency (Hz)")]
       level = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Level (dB SPL)")] 
       duration = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Duration (ms)")] 
       ramps = parent.prm[currBlock]['field'][parent.prm['fieldLabel'].index("Ramps (ms)")]
       phase = 0
       channel = parent.prm[currBlock]['chooser'][parent.prm['chooserLabel'].index("Ear:")]
    
       correctFrequency = frequency + (frequency*parent.prm['adaptiveDifference'])/100
       parent.stimulusCorrect = pureTone(correctFrequency, phase, level, duration, ramps, channel, parent.prm['sampRate'], parent.prm['maxLevel'])
      
       parent.stimulusIncorrect = []
       for i in range((parent.prm['nIntervals']-1)):
           thisSnd = pureTone(frequency, phase, level, duration, ramps, channel, parent.prm['sampRate'], parent.prm['maxLevel'])
           parent.stimulusIncorrect.append(thisSnd)
       
       parent.playRandomisedIntervals(parent.stimulusCorrect, parent.stimulusIncorrect)


.. _sec-experiment_opts: 

The Experiment “opts”
^^^^^^^^^^^^^^^^^^^^^

-  ``hasISIBox``

-  ``hasAlternativesChooser``

-  ``hasFeedback``

-  ``hasIntervalLights``

-  ``hasPreTrialInterval``

 
.. _sec-par:

Using ``par``
^^^^^^^^^^^^^

.. _sec-simulations:

Simulations
-----------

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
