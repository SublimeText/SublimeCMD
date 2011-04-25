==========
SublimeCMD
==========

A simple command processor for Sublime Text.


The Problem
===========

The Python console is very cumbersome to use for a number of common tasks. A
dedicated command processor for these tasks can improve the experience.


Feature Overview
================

- Commands to explore settings, commands and keybindings, and to run commands
  by name.
- Integration with PowershellUtils package (if available).
- Integration with UberSelection package (if available).


Getting Started
===============

* Install `SublimeCMD`_
* Install `AAAPackageDev`_ (dependency)
* Optionally install, `UberSelection`_
* Optionally install, `PowershellUtils`_

.. _SublimeCMD: https://bitbucket.org/guillermooo/sublimecmd/downloads/SublimeCMD.sublime-package
.. _AAAPackageDev: https://bitbucket.org/guillermooo/aaapackagedev/src
.. _UberSelection: https://bitbucket.org/guillermooo/uberselection/src
.. _PowershellUtils: https://bitbucket.org/guillermooo/powershellutils/src

If you're running a full installation, simply double click on the ``.sublime-package`` files.
If you're running a portable installation, perform an `installation by hand`_.

.. _installation by hand: http://sublimetext.info/docs/extensibility/packages.html#installation-of-packages-with-sublime-package-archives

Lastly, run ``sublime_cmd`` from the Python console or bind this command to a
key combination::

   view.run_command("sublime_cmd")


How to Use
==========

SublimeCMD understands the following types of commands:

* Intrinsic SublimeCMD commands
* UberSelection commands (see UberSelection docs)
* PowershellUtils commands (see PowershellUtils docs)

Type commands at the SublimeCMD prompt and press ``enter``.


Intrinsic Commands
==================

Syntax:

   - ``<COMMAND>[<MODIFIERS>] <ARGUMENTS>``

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


Powershell Commands
===================

Precede the command with ``!`` or ``r!``::

   ![datetime]"$(([datetime]::Now).year)/12/25"-(date)|%{ "Days left until Christmas: $($_.days)"}
   r!"$pwd"

``!``
   Runs the command and outputs results to a new buffer.

``r!``
   Runs the command and *reads* ouput into selected regions.


UberSelection Commands
======================

Type the command normally::

   ?^def ?,/^def /-1-V/football/;s/foo/bar/