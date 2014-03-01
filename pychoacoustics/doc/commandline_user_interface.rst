.. _sec-cmd_user_interface:

****************************
Command Line User Interface
****************************

In order to automate certain tasks, or perform some advanced operations,
``pychoacoustics`` can be called from the command line with a number of
command line options. The list of possible command line options is shown below:

-  ``-h, --help`` Show help message.

-  ``-f, --file FILE`` Load parameters file ``FILE``.

-  ``-r, --results FILE`` Save the results to file ``FILE``.

-  ``-l, --listener LISTENER`` Set listener label to ``LISTENER``.

-  ``-s, --session SESSION`` Set session label to ``SESSION``.

-  ``-c, --conceal`` Hide Control and Parameters Windows.

-  ``-p, --progbar`` Show the progress bar.

-  ``-b, --blockprogbar`` Show the progress bar.

-  ``-q, --quit`` Quit after finished.

-  ``-a, --autostart`` Automatically start the first stored block.

-  ``-k, --reset`` Reset block positions.

-  ``-z, --seed`` Set random seed.

-  ``-x, --recursion-depth`` Set the maximum recursion depth (this
   overrides the maximum recursion depth set in the preferences window).

-  ``-g, --graphicssystem`` sets the backend to be used for on-screen
   widgets and QPixmaps. Available options are raster and opengl.

-  ``-d, --display`` This option is only valid for X11 and sets the X
   display (default is $DISPLAY).

each command line option has a short (single dash, one letter) and long
(double dash, one word) form, for example to show the help message, you
can use either of the two following commands:

::

    $ pychoacoustics -h
    $ pychoacoustics --help
