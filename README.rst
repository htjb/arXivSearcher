=========================================
arXivSearcher: arXiv Terminal Search Tool
=========================================

:arXivSearcher: arXiv Terminal Search Tool
:Author: Harry Thomas Jones Bevins
:Version: 2.0.0
:Homepage: https://github.com/htjb/arXivSearcher

App for searching arXiv from the terminal and with MCP.

Search arXiv from the terminal
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

The results will be printed to the terminal and the most recent
article will be the last one printed. 

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

  from arXivSearcher.search import searcher

  searcher('string to search', date_limited=False, max_results=50)

An example search using the terminal is shown below.

.. image:: https://github.com/htjb/arXivSearcher/blob/main/images/example.png
  :width: 400
  :align: center
  :alt: Example Search Result

MCP
~~~

arXivSearcher can also be used with MCP. To use it with MCP you need to
add the following to your MCP configuration file. For example if you are 
using claude you would add it to "mcpServers" in your 
"claude_desktop_config.json" file.

```
"arXiv": {
      "command": "/path/to/python",
      "args": [
        "/path/to/arXivSearcher/arXivSearcher/search.py"]
  }
```

Licence
-------

The software is free to use on the MIT open source license.

Contributing
------------

While the code is in pre-release suggestions for features and existing bug fixes
are welcome. Please raise an issue to discuss any pull requests.
