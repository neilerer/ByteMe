README.md

----------------
Date 21 Jun 2017
User: Otto
Subject: Overview

We will make extensive use of of Python in this project, including myriad packages; Anaconda will make coordination and maintenance of the packages clean, simple, and efficient.

To begin with you are using the basic Python 3.6 Anaconda package, with Django and Git installed; this is summer_project_{YourOS}_0_0.  Installation instructions are provided below.

In the course of your devleopment work, should you make use of a new package:
- upload a new .yml file (see below for instructions)
- include an entry into package_sources.txt (see file for examples and required formatting)
- and notify the group on Slack on the virtual_environment channel (this will allow a user to either update the virtual environment using the .yml file you have uploaded or, in the event it was created on a different OS, update their OS manually and upload a new .yml file for that OS)

After every installation and at the start of each day, it is recommended that you activate the current virtual environment and update all packages.

Note that there are sepearte .yml files, one for Apple OSs and one for Windows.  This reflect idiosyncratic package elements Anaconda uses for each OS.  Given our use of Python, however, the OS-related idiosyncrasies will not impact our project and ability to share work; we'll only need to put in a slighty higher level of work cataloguing new packages instad of sharing a common .yml file for updates.


-----------------
Date: 21 Jun 2017
User: Otto
Subject: How to install Anaconda

- https://docs.continuum.io/anaconda/install


-----------------
Date: 21 Jun 2017
User: Otto
Subject: Managing virtual environments

- https://conda.io/docs/using/envs.html#


-----------------
Date: 21 Jun 2017
User: Otto
Subject: Virtual environment naming conventions

- summer_project_{YourOS}_X_Y.yml
- summer_project will remain constance
- {YourOS} <-- Apple or Windows (possibly add Linux for server; might be OK with Apple)
- X <-- this number will increment if and only if a package is removed from a virtual environment or if we start a new virtual environment
- Y <-- this number will increment any time a package is added to the virtual environment