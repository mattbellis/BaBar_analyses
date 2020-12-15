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

    # ne
    mask = (df['r2all']>0.05) \
         & (df['r2all']<0.75) \
         & (df['scalarmomsum']>5) \
         & (df['scalarmomsum']<9) \
         & (df['thrustmag']>0.65) \
         & (df['thrustmag']<0.92) \
         & (df['thrustmagall']>0.60) \
         & (df['thrustmagall']<0.92) \

    return mask


################################################################################
def blinding_mask(df):

    x = df['bnvbcandMES']
    y = df['bnvbcandDeltaE']

    mask = (x>5.265) & (y>-0.12) & (y<0.12)

    return mask

################################################################################
def side_bands_mask(df,region='DeltaEmES'):

    mask = None

    if region=='DeltaEmES':

        x = df['bnvbcandMES']
        y = df['bnvbcandDeltaE']

        maskA = (x>5.265) & (y>0.12) & (y<0.2)
        maskB = (x>5.265) & (y<-0.12) & (y>-0.2)

        mask = (maskA) & (maskB)

    elif region=='protonp3':

        x = df['bnvprotp3']

        maskA = (x>2.0) & (x<2.3)
        maskB = (x>2.8) & (x<3.1)

        mask = (maskA) | (maskB)

    return mask

################################################################################
def bnv_children_momentum_mask(df,child='proton'):

    mask = None

    if child=='proton':

        x = df['bnvprotp3']

        mask = (x>2.3) & (x<2.8)

    elif child=='muon' or child=='electron' or child=='nu':

        x = df['bnvlepp3']

        mask = (x>2.3) & (x<2.8)


    return mask
