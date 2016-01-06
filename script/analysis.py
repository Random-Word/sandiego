#!/usr/bin/env python3

import numpy as np
import pandas as pd
import lasagne
import nolearn as nl
import os
import scipy as sp
import multiprocessing
import pickle

SELECTED_CITIES = ['Singapore', 'Sydney', 'Melbourne', 'Tokyo', 'Osaka',
        'Paris', 'Madrid', 'Barcelona', 'Rome', 'Venice',
        'San Francisco', 'New York', 'Stockholm', 'Johannesburg', 'Honolulu',
        'Cape Town', 'Sao Paulo', 'Buenos Aires', 'Bangkok', 'Ankara',
        'Seoul', 'Busan', 'Phnom Penh', 'Palermo', 'Athens', 'Vienna',
        'Prague', 'Warsaw', 'Taipei']


def load_imgs(root, filenames):
    data = np.zeros((len(filenames), 640, 640, 3))
    labels = np.zeros((len(filenames)))
    results = list()
    for i, f in enumerate(filenames):
        labels[i] = SELECTED_CITIES.index(f.split('_')[0])
        results.append(pool.apply_async(sp.ndimage.imread, [root+os.sep+f]))
    for i, r in enumerate(results):
        data[i,...] = r.get()
    np.save("/mnt/data/"+root.split('/')[-1]+"_Data", data)
    np.save("/mnt/data/"+root.split('/')[-1]+"_Labels", labels)
    print(data.shape)
    print(labels.shape)

pool = multiprocessing.Pool(multiprocessing.cpu_count())

for root, _, filenames in os.walk('../imgs/Cities/'):
    if len(filenames) > 0:
        print(root)
        load_imgs(root, filenames)


