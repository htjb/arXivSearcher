=========================================
arXivSearcher: arXiv Terminal Search Tool
=========================================

:globalemu: arXiv Terminal Search Tool
:Author: Harry Thomas Jones Bevins
:Version: 1.0.0-beta.0
:Homepage: https://github.com/htjb/arXivSearcher
:Documentation:

App for searching arXiv from the terminal.

Search arXiv from the terminal
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Warning: The code is a minimal working example of a larger goal (see To Do list
below) and is still in development.

With arXivSearcher you can currently search arXiv from the terminal for specific
phrases and get relevant articles returned.

To install from source run

.. code:: bash

  git clone https://github.com/htjb/arXivSearcher
  cd arXivSearcher
  python setup.py install --user

You can then perform searches from the terminal by entering the following

.. code:: bash

  arXivSearcher 'string to search'

The most recent article will be the last one printed.
By default the results will not be date limited and only the 5 most recent articles
containing the searched phrase will be returned. You can increase the number
of returned articles by setting the flag ``-mr`` like so

.. code:: bash

  arXivSearcher 'string to search' -mr 50

and you can then limit the returned articles to articles either published
or updated on the date that the search was performed with the ``-dl`` flag e.g.

.. code:: bash

  arXivSearcher 'string to search' -mr 50 -dl

Alternatively you can call the function directly in a python script like so

.. code:: python

  from scraper.search import searcher

  searcher('string to search', date_limited=False, max_results=50)

An example search using the terminal is shown below.

.. image:: https://github.com/htjb/arXivSearcher/raw/master/images/example.png
  :width: 400
  :align: center
  :alt: Example Search Result

To Do:
~~~~~~
- make the search options broader e.g. author ect rather than just strings
- add code to optionally email results to user (written just needs formatting
  as part of the module)
- config file/cron job for daily update on a given search?

Documentation
-------------

Under development.

Licence
-------

The software is free to use on the MIT open source license.

Contributing
------------

While the code is in pre-release suggestions for features and existing bug fixes
are welcome. Please raise an issue to discuss any pull requests.
