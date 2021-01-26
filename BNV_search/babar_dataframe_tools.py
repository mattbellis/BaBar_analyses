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
    #print(tot)

    mask = True
    for cut in failing:
        mask &= (df[cut]==0)
    for cut in passing:
        mask &= (df[cut]==1)

    tot = len(df[mask])
    #print(tot)

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

    elif child=='muon' or child=='electron':
        x = df['bnvlepp3']
        mask = (x>2.3) & (x<2.8)

    elif child=='nu':
        x = df['bnvlepp3']
        mask = (x>1.5) & (x<4.5)

    elif child=='neutron':
        x = df['bnvprotp3']
        mask = (x>0.0) & (x<4.0)


    return mask

################################################################################
def bnv_children_costh_mask(df,child='proton'):

    mask = None

    if child=='proton':
        x = df['bnvprotcosth']
        mask = (x>-0.92) & (x<1.0)

    elif child=='muon' or child=='electron':
        x = df['bnvlepcosth']
        mask = (x>-0.92) & (x<1.0)

    return mask

################################################################################
def decay_specific_cuts(df,decay='pmu'):

    mask = None
    extra_mask = None
    all_pid_mask = None

    if decay=='pmu' or decay=='pe':
        if decay=='pmu':
            all_pid_mask = pid_mask(df,particle='proton') & pid_mask(df,particle='muon')
        elif decay=='pe':
            all_pid_mask = pid_mask(df,particle='proton') & pid_mask(df,particle='electron') & (df['ne']==1)

        extra_mask = (df['bnvprotcosth']<0.75) & \
                     (df['bnvprotcosth']>-0.80) & \
                     (df['bnvlepcosth']<0.80) & \
                     (df['bnvlepcosth']>-0.70) & \
                     (df['np']==1) & \
                     (df['bnvprotp3']>2.40) & \
                     (df['bnvprotp3']<2.7) & \
                     (df['bnvlepp3']>2.40) & \
                     (df['bnvlepp3']<2.7) & \
                     (df['missingmass2']>-2.0) & \
                     (df['missingmassES']>-2.0) & \
                     (df['r2all']<0.7) & \
                     (df['r2']<0.8) & \
                     (df['sphericityall']<0.8) & \
                     (df['scalarmomsum']<11.0) & \
                     (df['scalarmomsum']>7.5) & \
                     (df['thrustmag']<0.95) & \
                     (df['thrustmagall']<0.95) & \
                     (df['tagbcandDeltaE']>-2.5) & \
                     (df['tagbcandDeltaE']<1.0) & \
                     (df['tagbcandMES']>5.1) 


    elif decay=='pnu':
        all_pid_mask = pid_mask(df,particle='proton') 

        extra_mask = (df['bnvprotcosth']<0.70) & \
                     (df['bnvprotcosth']>-0.85) & \
                     (df['bnvlepcosth']<0.90) & \
                     (df['bnvlepcosth']>-0.75) & \
                     (df['np']==1) & \
                     (df['bnvprotp3']>2.3) & \
                     (df['bnvprotp3']<2.7) & \
                     (df['bnvlepp3']>1.8) & \
                     (df['bnvlepp3']<4.0) & \
                     (df['missingE']>1.0) & \
                     (df['missingE']<5.0) & \
                     (df['missingmass2']<-3.0) & \
                     (df['missingmassES']<4.0) & \
                     (df['r2all']<0.6) & \
                     (df['r2']<0.7) & \
                     (df['sphericityall']<0.6) & \
                     (df['scalarmomsum']<8.5) & \
                     (df['scalarmomsum']>4.5) & \
                     (df['thrustmag']<0.95) & \
                     (df['thrustmagall']<0.90) & \
                     (df['bnvbcandDeltaE']>-2.75) & \
                     (df['bnvbcandDeltaE']<-2.4) & \
                     (df['bnvbcandMES']>5.1) & \
                     (df['tagbcandDeltaE']<1.0) & \
                     (df['tagbcandDeltaE']>-2.50) 

    elif decay=='nmu':#NEED TO FIGURE THIS OUT!
        all_pid_mask = pid_mask(df,particle='muon') 

        extra_mask = (df['bnvprotcosth']<0.75) & \
                     (df['bnvprotcosth']>-0.90) & \
                     (df['bnvprotp3']>0.5) & \
                     (df['tagbcandmass']>2.00) & \
                     (df['bnvbcandp3']<2.50) & \
                     (df['tagbcandp3']<2.50) & \
                     (df['missingE']>0.0) & \
                     (df['missingE']<5.0) & \
                     (df['missingmom']>0.5) & \
                     (df['missingmom']<4.0) & \
                     (df['r2all']<0.6) & \
                     (df['r2']<0.7) & \
                     (df['sphericityall']<0.6) & \
                     (df['scalarmomsum']<10.0) & \
                     (df['scalarmomsum']>4.0) & \
                     (df['thrustmag']<0.95) & \
                     (df['thrustmagall']<0.95) & \
                     (df['bnvbcandDeltaE']>-2.9) & \
                     (df['bnvbcandDeltaE']<-2.56) & \
                     (df['tagbcandDeltaE']<3.0) & \
                     (df['tagbcandDeltaE']>-3.00) & \
                     (df['bnvbcandMES']<7.5) & \
                     (df['bnvbcandMES']>-5.0) 
                     #(df['missingmass2']<-3.0) & \
                     #(df['missingmassES']<4.0) & \

    elif decay=='ne':#NEED TO FIGURE THIS OUT!
        all_pid_mask = pid_mask(df,particle='electron') 

        extra_mask = (df['bnvprotcosth']<0.70) & \
                     (df['bnvprotcosth']>-0.85) & \
                     (df['bnvlepcosth']<0.90) & \
                     (df['bnvlepcosth']>-0.75) & \
                     (df['np']==1) & \
                     (df['bnvprotp3']>2.3) & \
                     (df['bnvprotp3']<2.7) & \
                     (df['bnvlepp3']>1.8) & \
                     (df['bnvlepp3']<4.0) & \
                     (df['missingE']>1.0) & \
                     (df['missingE']<5.0) & \
                     (df['missingmass2']<-3.0) & \
                     (df['missingmassES']<4.0) & \
                     (df['r2all']<0.6) & \
                     (df['r2']<0.7) & \
                     (df['sphericityall']<0.6) & \
                     (df['scalarmomsum']<8.5) & \
                     (df['scalarmomsum']>4.5) & \
                     (df['thrustmag']<0.95) & \
                     (df['thrustmagall']<0.90) & \
                     (df['bnvbcandDeltaE']>-2.75) & \
                     (df['bnvbcandDeltaE']<-2.4) & \
                     (df['bnvbcandMES']>5.1) & \
                     (df['tagbcandDeltaE']<1.0) & \
                     (df['tagbcandDeltaE']>-2.50) 

    mask = all_pid_mask & extra_mask
    return mask
