import matplotlib.pylab as plt
import numpy as np
import sys
import pandas as pd
import seaborn as sns

import plotting_tools as pt

infilename = sys.argv[1]

df = None

if infilename.find('.csv'):
    df = pd.read_csv(infilename)
elif infilename.find('.h5'):
    df = pd.read_hdf(infilename)

#pt.make_all_plots(df,grid_of_plots=(4,4))

plot_params = pt.get_variable_parameters_for_plotting()
plot_params['p3']['range'] = (2.0,3.0)
pt.make_all_plots(df,specific_plots=['p3','cos(theta)'],grid_of_plots=(1,1),plot_params=plot_params)

plt.show()
