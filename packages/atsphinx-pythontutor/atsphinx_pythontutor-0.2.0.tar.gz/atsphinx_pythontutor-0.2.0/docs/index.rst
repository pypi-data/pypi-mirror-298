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
      :alt: Example to render key and value of list

      user_info = {"user_name": "Taro", "last_name": "Yamada"}
      for key in user_info:
          print(key)
          print(user_info[key])

.. pythontutor::
   :width: 800
   :height: 500
   :alt: Example to render key and value of list

   user_info = {"user_name": "Taro", "last_name": "Yamada"}
   for key in user_info:
       print(key)
       print(user_info[key])

Directive
=========

.. rst:directive:: pythontutor

   .. rst:directive:option:: width
      :type: int

      Width of iframe content.
      Default value is ``800``.

   .. rst:directive:option:: height
      :type: int

      Height of iframe content.
      Default value is ``500``.

   .. rst:directive:option:: alt
      :type: str | None

      If this is set non-empty string, append text link to pythontutor that runs same code into top of iframe.
