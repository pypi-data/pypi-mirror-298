====================
atsphinx-pythontutor
====================

.. toctree::
   :hidden:

   changes

Overview
========

This is Sphinx-extension to embed iframe content of `PythonTutor <https://pythontutor.com>`_.

It is useful to explain code behavior as tutorial document of python in Sphinx doc.

Installation
============

.. code:: console

   pip install atsphinx-pythontutor

Usage
=====

Set extension into your ``conf.py`` of document.

.. code:: python

   extensions = [
       ...,
       "atsphinx.pythontutor",
   ]


Write content into your document by ``pythontutor`` directive.

.. code:: rst

   .. pythontutor::

      # Write your code

Example
=======

.. code:: rst

   .. pythontutor::
      :width: 800
      :height: 500

      user_info = {"user_name": "Taro", "last_name": "Yamada"}
      for key in user_info:
          print(key)
          print(user_info[key])

.. pythontutor::
   :width: 800
   :height: 500

   user_info = {"user_name": "Taro", "last_name": "Yamada"}
   for key in user_info:
       print(key)
       print(user_info[key])
