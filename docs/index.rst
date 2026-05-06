https://github.com/philippkosarev/acd

acd
===

A Python library and CLI for reading and writing Assetto Corsa Data (.acd) files.


Installation
------------

To install the in-development version you can run the following:

.. code-block::

  pip install git+https://github.com/philippkosarev/acd.git

.. note::

  A stable version should be coming soon.


Examples
--------

Here is a simple example that reads a .acd file and prints the contents of the first file in it:

.. code-block::

  import acd
  data = acd.read_file('./data.acd')
  keys = list(data.keys())
  first_key = keys[0]
  print(data[first_key])


Here is another example that writes a pre-defined dictionary to a .acd file:

.. code-block::

  import acd
  data = {
    'example-filename.txt': 'Hello from the example-filename.txt!',
  }
  acd.write_file(data, './data.acd')


API
---

.. automodule:: acd
  :imported-members:
