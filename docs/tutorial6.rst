Tutorial 6: Custom Experiment
===============================

So far we covered all the default experiment types (i.e., Display, Tracking, and Total) available
in VRLatency. But, what if we
want to design our own experiment? In this tutorial, we go through designing custom experiments.
Up until now all we cared about was our Python script; however, to design our own experiment,
we also must write our own Arduino code.

Experiment Description
++++++++++++++++++++++

Our new experiment is going to measure the ??

Arduino
+++++++

Define the sensor analog pins on Arduino:

.. code-block:: c++

    int analogPin_Left = 0;
    int analogPin_Right = 1;

Define some variables to keep track of during the experiment:

.. code-block:: c++

    bool led_state = 0;
    int trial = 0;
    int i = 0;

Complete Arduino Code
---------------------


Python
++++++

.. code-block:: python

    import vrlatency as vrl

Complete Python Code
--------------------
