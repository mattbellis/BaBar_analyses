import numpy as np
import matplotlib.pylab as plt
import uproot 
import awkward as ak

import sys

infilenames = sys.argv[1:]

masses_pn = []
masses_pp = []
masses_nn = []

for infilename in infilenames:
    print(infilename)
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
    a_eq = events['eq'].array()

    a_protone = events['protone'].array()
    a_protonpx = events['protonpx'].array()
    a_protonpy = events['protonpy'].array()
    a_protonpz = events['protonpz'].array()
    a_protonq = events['protonq'].array()

    for ee,epx,epy,epz,eq,pe,ppx,ppy,ppz,pq  in zip(a_ee,a_epx,a_epy,a_epz,a_eq,a_protone,a_protonpx,a_protonpy,a_protonpz,a_protonq):
        #print(ee,epx,epy,epz)
        #print(pe,ppx,ppy,ppz)
        ne = len(ee)
        nprot = len(pe)
        #print(ne,nprot)
        for i in range(ne):
            e0,px0,py0,pz0,q0 = ee[i],epx[i],epy[i],epz[i],eq[i]
            for j in range(nprot):
                e1,px1,py1,pz1,q1 = pe[j],ppx[j],ppy[j],ppz[j],pq[j]
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
                if q0*q1<0:
                    masses_pn.append(m)
                elif q0*q1>0 and q0>0:
                    masses_pp.append(m)
                elif q0*q1>0 and q0<0:
                    masses_nn.append(m)

print("# masses pn: ",len(masses_pn))
print("# masses nn: ",len(masses_nn))
print("# masses pp: ",len(masses_pp))
np.savetxt('ep_masses_pn.dat',np.array(masses_pn))
np.savetxt('ep_masses_nn.dat',np.array(masses_nn))
np.savetxt('ep_masses_pp.dat',np.array(masses_pp))
#plt.hist(masses,bins=200)
#plt.show()
