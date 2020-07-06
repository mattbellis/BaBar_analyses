import matplotlib.pylab as plt
import numpy as np
import sys
import pandas as pd
import seaborn as sns

import plotting_tools as pt

infilenames = sys.argv[1:]

dfs = []
for infilename in infilenames:

    if infilename.find('.csv')>=0:
        dfs.append(pd.read_csv(infilename))
    elif infilename.find('.h5')>=0:
        dfs.append(pd.read_hdf(infilename))


pt.make_all_plots(dfs,grid_of_plots=(4,4),xlabelfontsize=10,ignorePID=True,norm_hist=True)

#plot_params = pt.get_variable_parameters_for_plotting()
#plot_params['p3']['range'] = (2.0,3.0)
#pt.make_all_plots(dfs,specific_plots=['p3','cos(theta)'],grid_of_plots=(1,1),plot_params=plot_params,figsize=(4,3),norm_hist=True,infilenames=infilenames)

plt.show()
