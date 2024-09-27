


import CoolProp
import CoolProp.CoolProp as CP

def relative_humedity(prop1,prop2):

    rh=CP.HAProps('R', 'T', prop1,  'D', prop2,'P', 101.325)
    return rh

