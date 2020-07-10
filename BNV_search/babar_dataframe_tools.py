import pandas as pd
import numpy as np


################################################################################
def pid_mask(df,particle='muon'):

    failing,passing = [],[]
    if particle=='muon':
        failing = ['muIsTightKMProton','muIsTightKMKaon','muIsTightKMElectron']
        #passing = ['muIsBDTTightMuon', 'muIsBDTVeryTightMuon', 'muIsBDTTightMuonFakeRate', 'muIsBDTVeryTightMuonFakeRate']
        passing = ['muIsBDTTightMuonFakeRate']
    if particle=='proton':
        failing = ['protonIsTightKMKaon','protonIsTightKMPion','protonIsTightKMElectron'] #,'TightBDTKaon']
        passing = ['protonIsTightKMProton']


    tot = len(df)
    print(tot)

    mask = True
    for cut in failing:
        mask &= (df[cut]==0)
    for cut in passing:
        mask &= (df[cut]==1)

    tot = len(df[mask])
    print(tot)

    return mask

################################################################################
def shape_mask(df):

    mask = (df['r2all']>0.2) \
         & (df['r2all']<0.9) \
         & (df['thrustmag']>0.65) \
         & (df['thrustmag']<0.9) \
         & (df['thrustmagall']>0.72) \
         & (df['thrustmagall']<0.85) \

    return mask

