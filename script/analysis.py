#!/usr/bin/env python3

import numpy
import pandas
import lasagne
import nolearn
import os

for root, dirnames, filenames in os.walk('../imgs'):
    print(dirnames)
    print(filenames)
