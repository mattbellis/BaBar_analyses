import myPIDselector
from myPIDselector import *

eps = PIDselector("pi")

eps.SetBits(4500)

eps.PrintSelectors()
eps.PrintBits()

print(eps.IsSelectorSet("LooseKMPionSelectionLooseGLHPionSelection"))
print(eps.IsSelectorSet("TightKMPionSelectionTightGLHPionSelection"))
print(eps.IsSelectorSet("PidRoyPionSelectionNotKaon"))
