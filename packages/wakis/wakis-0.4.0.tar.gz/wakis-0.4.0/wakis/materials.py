# copyright ################################# #
# This file is part of the wakis Package.     #
# Copyright (c) CERN, 2024.                   #
# ########################################### #

'''
Material library dictionary

Format (non-conductive):
{
    'material key' : [eps_r, mu_r],
}

Format (conductive):
{
    'material key' : [eps_r, mu_r, sigma[S/m]],
}

! Note:
* 'material key' in lower case only
* eps = eps_r*eps_0 and mu = mu_r*mu_0
'''

import numpy as np
from scipy.constants import c as c_light, epsilon_0 as eps_0, mu_0 as mu_0

material_lib = {
    'pec' : [np.inf, 1.],

    'vacuum' : [1.0, 1.0],

    'dielectric' : [10., 1.0],
    
    'metal' : [10, 1.0, 10],
}