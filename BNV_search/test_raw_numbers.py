import numpy as np
import matplotlib.pylab as plt

from raw_event_numbers_and_cross_section import *

ren = raw_event_numbers

tot = 0
for key in ren["data"].keys():
    tot += ren["data"][key]["raw"]

print(tot,tot/1e9)

bkg = [1235, 1237, 1005, 998, 3429, 3981, 2400]
tot = 0
for sp in bkg:
    key = "{0}".format(sp)
    xsec = ren["MC"][key]["xsec"]
    raw = ren["MC"][key]["raw"]
    print("{0:4s} {1:4.2f} {2:-9.2f} {3:6.2f} {4:6.2f}".format(key, xsec, xsec*intlumi, raw/1e6, (raw/1e6)/(xsec*intlumi)))
    tot += xsec
print(tot)
