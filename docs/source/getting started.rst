=======
Getting Started
=======

Installation instructions and basic usage.

Prerequisites
----------------------------

- **Git CLI** - `Download Here <https://git-scm.com/downloads>`_
- **Heroku CLI** - `Download Here <https://devcenter.heroku.com/articles/heroku-cli#install-the-heroku-cli>`_
- **OS** - Linux, MacOS, Windows
- **Python Version** ≥ 3.6


PyPI
-------

You can install dash-tools from PyPI via pip.

.. code-block:: bash

    pip install dash-tools


Simple Usage
----------
Using dash-tools is similar to other popular command line clients for creating and deploying projects.

.. note::
    Some Windows users may need to run dashtools with ``.\dashtools`` in the following examples.


Creating a Project
**********************

Creating a new dash project is simple. Here we choose to name it "MyApp". Doing so will create a directory named "MyApp" in the current working directory.

.. code-block:: bash

    dashtools init MyApp


Deploying a Project
**********************

You can deploy any project containing an app.py file. Running the following command will create Procfile, requirements.txt, and runtime.txt if they are not found. Follow the on-screen prompts to complete the deployment to Heroku.

.. code-block:: bash
    
    dashtools heroku --deploy


Updating a deployed Project
************************************

Updating a deployed project is as easy as pushing changes to the remote Heroku repository. Using the following command from the project root will update the remote 'heroku' repository and restart the application.

.. code-block:: bash
    
    dashtools heroku --update


Running a Project
**********************

Running the app.py file is as simple as running the following command from the project root, or any directory above the app.py file.

.. code-block:: bash
    
    dashtools run


Dockerizing a Project
**********************

To create a Docker image for your project, run the following command in the project root with an image name.

.. code-block:: bash
    
    dashtools docker --init MyProjectImage


Learn More
----------

Check out the :doc:`Tutorials <tutorials/index>` page for more in-depth usage examples.