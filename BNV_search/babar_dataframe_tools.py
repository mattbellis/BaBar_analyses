import pandas as pd
import numpy as np


################################################################################
def pid_mask(df,particle='muon'):

    failing,passing = [],[]
    if particle=='muon':
        failing = ['muIsTightKMProton','muIsTightKMKaon','muIsTightKMElectron']
        #passing = ['muIsBDTTightMuon', 'muIsBDTVeryTightMuon', 'muIsBDTTightMuonFakeRate', 'muIsBDTVeryTightMuonFakeRate']
        passing = ['muIsBDTTightMuonFakeRate']
    elif particle=='proton':
        failing = ['protonIsTightKMKaon','protonIsTightKMPion','protonIsTightKMElectron'] #,'TightBDTKaon']
        passing = ['protonIsTightKMProton']
    elif particle =='electron':
        failing = []
        passing = ['eIsTightKMElectron', 'eIsVeryTightKMElectron']


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


################################################################################
def blinding_mask(df):

    x = df['bnvbcandMES']
    y = df['bnvbcandDeltaE']

    mask = (x>5.265) & (y>-0.12) & (y<0.12)

    return mask

################################################################################
def side_bands_mask(df,region='DeltaEmES'):

    x = df['bnvbcandMES']
    y = df['bnvbcandDeltaE']

    maskA = (x>5.265) & (y>0.12) & (y<0.2)
    maskB = (x>5.265) & (y<-0.12) & (y>-0.2)

    mask = (maskA) & (maskB)

    return mask
