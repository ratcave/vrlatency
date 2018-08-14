Tutorial 2: Display Latency
===========================

Measurements of display latency using VRLatency is not limited to Virtual Reality systems,
and you can measure the latency of pretty much any display, as long as you can have the display
to shine some light on the device. Let's go through this process in this tutorial.

Generally the flow of measuring the latency is as follow:
    - Connect to Arduino
    - Define the experiment
    - Run the experiment
    - Save the data

In case you want to visualize the data:
    - Read the (saved) data
    - Compute the latencies
    - Visualize

Connect to Arduino
++++++++++++++++++

.. note:: Make sure you have already installed arduino drivers on your system. you can check this by going to Device Manager on your system and check whether your system has recognized the connected Arduino(s).

To connect to the Arduino we need to know which USB PORT is the device connected to. Although
one can check that in Device Manager, VRLatency provides a quick way of getting a list of all the
Arduinos that are connected to your system.
::
    import vrlatency as vrl

    vrl.Arduino.find_all()

Once you have the list of Arduino devices connected to your PC (including the USB PORT number), you can
connect the the device as follow:
::
    myarduino = vrl.Arduino.from_experiment_type(experiment_type='Display',
                                                 port='COM9',
                                                 baudrate=250000)

Once the above code is ran, we have a Serial Channel object with which data can be streamed between Arduino
and Python. Besides the USB PORT, we also need to define the communication BAUDRATE as well as the type of
experiments we are planning to run - in this case "Display".

.. note:: Baudrate usually takes values such as 300, 600, ..., 9600, 14400, ..., 115200. However, any baudrate chosen in your Python script must agree with the baudrate settings in the Arduino code.
