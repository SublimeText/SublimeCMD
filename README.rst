SublimeCMD
==========

A simple command processor for Sublime Text.


The Problem
***********

The Python console is very cumbersome to use for a number of common tasks. A
dedicated command processor for these task can improve the experience.


Feature Overview
****************

   - Commands to explore settings, commands and keybindings, and to run commands
     conveniently by name.
   - Integration with PowershellUtils package (if available).
   - Integration with UberSelection package (if available).


Getting Started
***************

Download the following items:

   * \ `Latest release`_ of SublimeCMD.
   * Optionally (recommended), `AAAPackageDev`_.
   * Optionally, `UberSelection`_.
   * Optionally, `PowershellUtils`_.

.. _Latest release: https://bitbucket.org/guillermooo/sublimecmd/downloads/SublimeCMD.sublime-package
.. _AAAPackageDev: https://bitbucket.org/guillermooo/aaapackagedev/src
.. _UberSelection: https://bitbucket.org/guillermooo/uberselection/src
.. _PowershellUtils: https://bitbucket.org/guillermooo/powershellutils/src

SublimeCMD will eventually depend on AAAPackageDev, so it is recommended that
you install that package too.

Now install all downloaded ``.sublime-package``\ s:

   - If you're running a full installation, simply double click on the file.
   - If you're running a portable installation, perform a `manual installation`_.

.. _manual installation: http://sublimetext.info/docs/extensibility/packages.html#installation-of-packages-with-sublime-package-archives

Lastly, run ``sublime_cmd`` from the Python console or bind this command to a
key combination.


How to Use
**********

SublimeCMD understands the following types of commands:

   * Intrinsic SublimeCMD commands.
   * UberSelection commands (see UberSelection docs).
   * PowershellUtils commands (see PowershellUtils docs).

Type commands at the SublimeCMD prompt and press ``enter``.


Intrinsic Commands
******************

Syntax:

   - ``<COMMAND>[<MODIFIER>] <ARGUMENTS>``

At the moment, an argument is always required, even if it's ignored. Some
arguments may be simple patterns like ``hell? world`` or ``hell? w*``.

``run``
   Runs or searches commands depending on the modifiers.

``set``
   Sets or searches settings depending on the modifiers.

Modifiers
---------

``?``
   Performs a query based on the argument.

``!``
   Generally forces verbose output from queries. If combined with query, must
   always precede ``?``.

``:w|a``
   Applies command to window or application. By default, commands are applied
   to the current view.


Examples
--------

::

   set word_wrap False

This command modifies the setting for the view in the current session.

::
   
   set? word_wrap

This command shows the setting's value in the status bar.

::

   set!? w*

This command plots all declared values for all settings beggining with ``w`` in
the order they are applied.

::

   run:w increase_font_size

This command runs the given argument as a window command.

::

   run!? .

This command shows all found commands. Note the argument is ignored.