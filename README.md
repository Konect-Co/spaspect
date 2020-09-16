# SpaSpect

## Overview

Video footage analysis technology. Monitors social distancing and face covering wearing (CCTV, webcam, security camera). Generates real-time and aggregate analytics.
 Click here to see it in action: [https://www.youtube.com/watch?v=I-m6U5SxnrY](https://www.youtube.com/watch?v=I-m6U5SxnrY)

![web app pic](pic.png)

## Features

- Customizable dashboard for users
  - Displays real-time and aggregate analytics
  - Comes with 3D map and overhead map for better visual perspective
- Predictive modeling: predicts scale of COVID-19 spread in certain areas
- Tracking
- Tracing feature: draws line following individuals on 3D map

### Realtime Analytics

Real-time analytics include the number of unmasked individuals, undistanced individuals, and total number of individuals.

### Aggregate Analytics

Aggregate analytics include people vs time graph, distance distribution curve, crosslocation, etc (long term).

## Impact

During the COVID-19 pandemic, social distancing and face covering are two cardinal measures to prevent the spread of this virus. Problematically, the public is breaching the COVID-19 regulations and local governments and cities have no effective way of making such observations.

### Use Cases

- Local governments can use to strategize enforcement
- Businesses can use to see how they&#39;re doing in terms of reopening
- Can be used in universities during reopening process

# Dependencies

## Python (core)

The following dependencies are needed for successful run:

- Python 3([https://www.python.org/downloads/](https://www.python.org/downloads/))
- Tensorflow 2.0.0 or higher([https://www.tensorflow.org/install](https://www.tensorflow.org/install))
- Opencv(cv2) 4.4.0([https://www.learnopencv.com/install-opencv-4-on-ubuntu-18-04/](https://www.learnopencv.com/install-opencv-4-on-ubuntu-18-04/))
- Numpy 1.19.0([https://pypi.org/project/numpy/](https://pypi.org/project/numpy/))

## C++ (core_cpp)

- cppunit

	- Follow steps at https://freedesktop.org/wiki/Software/cppunit/.

	- Then move <cpp_unit>/include/cppunit to /usr/local/include/cppunit.

	- Also move <cpp_unit>/src/cppunit to /usr/local/src/cppunit

- numcpp

	- Follow installation steps at https://dpilger26.github.io/NumCpp/doxygen/html/md__c_1__github__num_cpp_docs_markdown__installation.html

# How to Run

## Frontend visualization dashboard

Navigate to &quot;visualization&quot; directory

Run: node Server.js

## For real-time and aggregate analysis

Navigate to &quot;core&quot; directory

Run: python3 core.py

# Owner

Developed and owned by @Konect.

NOT OPEN SOURCE

# License

Copyright © 2020, Konect.
