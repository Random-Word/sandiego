#!/usr/bin/env python3

import numpy as np
import pandas as pd
import lasagne
import nolearn as nl
import os
import scipy as sp
import multiprocessing as mp
import pickle

sp.ndimage.imread

def load_imgs(filenames):
    data = np.zeros((len(filenames), 640, 640, 3))
    for f in filenames:
        results.append(pool.apply_async(sp.ndimage.imread, f))
    for i, r in enumerate(results):
        data[i,...] = results.get()
    return data

output = dict()
pool = multiprocessing.Pool(multiprocessing.cpu_count())

for root, _, filenames in os.walk('../imgs/Cities/'):
    if len(filenames) > 0:
        print(root)
        output[root] = load_imgs(filenames, root)

pickle.dump(output, "Output")

