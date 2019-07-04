.. Ada documentation master file, created by
   sphinx-quickstart on Thu Jul  4 07:14:11 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Ada's documentation!
===============================
Ada is a framework for creating executable scripts. Visual Effects pipelines require passing alot of dataaround various applications, manipulating that data with nodes and creating outputs which are used in other applications. Ada allows you to write an application specific execution framework that
passes an input context (protobuf) into a DCC along with a template scripts containing nodes with executable instructions on it (in Nuke this takes the form of a Ada tab on each node).
Users are able to setup a script, publish it (which saves out information about the execution order of the node graph) and run a cli or gui (todo) which gives them options for inputs, outputs, and any other attributes the creator decided to expose for manipulation. An Ada template becomes a node with inputs, outputs and attributes which is then executed.

Ada |release|
=================

Ada is a framework for creating executable scripts, written in Python.

Highlights include:
 * Applications all use the same structure for passing context data
 * Includes a simple CLI tool to (re)generate your data and modify it
 * Fully working Nuke implementation with examples
 * Simple to intergrate into your studio

Ready to get started? Check out the :doc:`Quickstart<quickstart>` guide.


Why the name "Ada"?
-----------------------

It sounds nice - she's a baker, a pioneer of computing, and it sounds like it aiding you in your work!

Source code
-----------

You can access the source code at: https://github.com/dveight/ada

How to get help, contribute, or provide feedback
------------------------------------------------

See our :doc:`feedback and contribution submission guidelines <contribute>`.

Documentation
-------------

.. toctree::
   :maxdepth: 2
