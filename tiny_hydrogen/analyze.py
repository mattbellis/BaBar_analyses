import numpy as np
import matplotlib.pylab as plt
import uproot 
import awkward as ak

import sys

infilenames = sys.argv[1:]

masses = []
for infilename in infilenames:
    f = uproot.open(infilename)

    #print(f.keys())

    events = f['Tskim']

    #print(events.keys())

    #print(len(events))

    #exit()

    a_ee = events['ee'].array()
    a_epx = events['epx'].array()
    a_epy = events['epy'].array()
    a_epz = events['epz'].array()

    a_protone = events['protone'].array()
    a_protonpx = events['protonpx'].array()
    a_protonpy = events['protonpy'].array()
    a_protonpz = events['protonpz'].array()

    for ee,epx,epy,epz,pe,ppx,ppy,ppz  in zip(a_ee,a_epx,a_epy,a_epz,a_protone,a_protonpx,a_protonpy,a_protonpz):
        #print(ee,epx,epy,epz)
        #print(pe,ppx,ppy,ppz)
        ne = len(ee)
        nprot = len(pe)
        #print(ne,nprot)
        for i in range(ne):
            e0,px0,py0,pz0 = ee[i],epx[i],epy[i],epz[i]
            for j in range(nprot):
                e1,px1,py1,pz1 = pe[j],ppx[j],ppy[j],ppz[j]
                mtemp0 = np.sqrt(e0*e0 - (px0*px0 + py0*py0 + pz0*pz0))
                mtemp1 = np.sqrt(e1*e1 - (px1*px1 + py1*py1 + pz1*pz1))
                #print(mtemp0,mtemp1)

                e = e0+e1
                px = px0+px1
                py = py0+py1
                pz = pz0+pz1

                m2 = e*e - (px*px + py*py + pz*pz)

                m = -999
                if m2>=0:
                    m = np.sqrt(m2)
                else:
                    m = -np.sqrt(abs(m2))

                if m<0.98:
                    print(m)
                masses.append(m)

print("# masses: ",len(masses))
plt.hist(masses,bins=200)
plt.show()
