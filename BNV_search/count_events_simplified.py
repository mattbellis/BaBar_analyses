import numpy as np

import plotting_tools as pt

import pandas as pd

import sys


infilenames = sys.argv[1:]


for infilename in infilenames:
    sptag = pt.get_sptag(infilenames[0])
    df = pd.read_hdf(infilename)
    size = len(df)

    print(f"{infilename:30s} {sptag[0]:6s} {size}")

