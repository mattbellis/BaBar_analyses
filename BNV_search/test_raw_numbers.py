import numpy as np
import matplotlib.pylab as plt

from raw_event_numbers_and_cross_section import *

ren = raw_event_numbers

tot = 0
for key in ren["DATA"].keys():
    tot += ren["DATA"][key]["raw"]

print(tot,tot/1e9)

bkg = [1235, 1237, 1005, 998, 3429, 3981, 2400]
tot = 0
scales = {}
print("Mode   x-sec    # expected (million)   # generate (million)  generate/expected   scaling factor")
for sp in bkg:
    key = f"{sp}"
    xsec = ren["MC"][key]["xsec"]
    raw = ren["MC"][key]["raw"]
    gen_div_expec = (raw/1e6)/(xsec*intlumi)
    scale = 1/gen_div_expec 
    print(f"{key:4s}    {xsec:4.2f} {xsec*intlumi:-9.2f}                  {raw/1e6:6.2f}                    {gen_div_expec:6.2f}        {scale:0.2f}")
    scales[key] = scale
    tot += xsec
print(tot)


print()
for sp in bkg:
    key = f"{sp}"
    #print(f"{key:6s}  {scales[key]:8.2f}       {scales[key]/scales['1005']:6.2f}  ")
    print(f"{key:6s}  {scales[key]:8.2f}       {scales[key]/scales['1235']:6.2f}  ")

