import numpy as np
import matplotlib.pylab as plt

from raw_event_numbers_and_cross_section import *
from selection_numbers import *

ren = raw_event_numbers
en = event_numbers

tot = 0
for key in ren["DATA"].keys():
    tot += ren["DATA"][key]["raw"]

print(tot,tot/1e9)

#bkg = [1235, 1237, 1005, 998, 3429, 3981, 2400]
bkg = list(en['MC'].keys())

tot = 0
for sp in bkg:
    key = "{0}".format(sp)
    xsec = ren["MC"][key]["xsec"]
    raw = ren["MC"][key]["raw"]
    skim = en['MC'][key]["skim"]

    print("{0:4s} {1:4.2f} {2:-9.2f} {3:6.2f} {4:6.2f} {5:6.8f}".format(key, xsec, xsec*intlumi, raw/1e6, (raw/1e6)/(xsec*intlumi), skim/raw))
    tot += xsec
print(tot)
