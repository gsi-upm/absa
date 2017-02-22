Aspy plugin
===========

This is a `Senpy <https://github.com/gsi-upm/senpy>`__  plugin for aspect-based sentiment analysis.

Installation
-----------

Firstly you have to install
`Docker <https://docs.docker.com/engine/installation/>`__ and Docker
Compose. This can be easily installed with
`pip <https://pip.pypa.io/en/stable/installing/>`__:

.. code:: bash

   $ pip install docker-compose

Now, clone the repository into your local system

.. code:: bash

   $ git clone http://github.com/gsi-upm/absa

   Use Docker Compose to build the application:

.. code:: bash

   $ cd absa/aspy
   $ docker-compose build
   $ docker-compose up

And that's all. A senpy server with aspy plugin is available at localhost:5000



Known issues
------------

The deployment of this plugin is under construction. Have some bugs but it will be fixed coming soon.

.. image:: http://gsi.dit.upm.es/images/stories/logos/gsi.png
   :alt: GSI Logo
      

