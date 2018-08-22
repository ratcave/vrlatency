Introduction
============

VRLatency is a simple python package that helps the process of measuring the latency of any projector-based virtual
reality (VR) system.

Latency
+++++++

Before moving forward, let us talk about latency. **Total latency** is the processing delay between a detected movement
and the virtual reality (VR) system’s response. In the context of real-time applications of VR, latency limits
support for fast interaction between the user and the system resulting in reduced VR immersion. In a projector-based
VR system, there are three main components:
    - **Tracking system** that tracks the position of the object of interest
    - **Graphics system** that, based on the information provided by the tracking system, renders a new image
    - **Display (or projector)** that displays the image sent from the Graphics engine

Unfortunately, all of these components introduce latency to our system to some extent. VRLatency is meant to ease the
process of measuring the latency of the different components of such system, which consequently help the process of
diagnostic and troubleshooting of the system to maximize performance. It has three default experiment types available,
measuring the latency for the following parts of the VR system:
    - Display (or projector)
    - Tracking
    - Total

In the following sections, I am going to describe these three different latencies in greater detail, including possible data and visualization you could get using VRLatency package.

Display Latency
+++++++++++++++

Display latency is the time it takes for the graphics system and the display to project a new image on the screen (this
is a subjective name which represents any kind of surface that the image is possibly projected on).

Tracking Latency
++++++++++++++++

Tracking latency is the time it takes for the tracking system to report the position.

Total Latency
+++++++++++++

Total latency = Tracking Latency + Display latency
