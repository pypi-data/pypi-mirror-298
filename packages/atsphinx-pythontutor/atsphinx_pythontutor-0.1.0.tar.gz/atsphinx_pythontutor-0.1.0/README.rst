====================
atsphinx-pythontutor
====================

Embedding iframe from https://pythontutor.com

Getting started
===============

.. code:: console

   pip install atsphinx-pythontutor

Usage
=====

1. Register your ``conf.py``.

.. code:: python

   extensions = [
       ...,
       "atsphinx.pythontutor",
   ]


2. Write ``pythontutor`` directive into your doc.

.. code:: rst

   .. pythontutor::
      :width: 800

      items = ["a", "b", "c"]

      for item in items:
          print(item.upper())
