
import numpy as np
from classy_sz import Class as Class_sz
import os
import time


cosmo_params_with_sigma_8 = {'H0': 67.36, 'ns': 0.9649, 
                             'Omega_b': 0.04, 
                             'omega_cdm': 0.1407, 'sigma8': 0.8, 'tau': 0.0544}



classy_sz = Class_sz()
classy_sz.set(cosmo_params_with_sigma_8)
classy_sz.set(
{'output': 'pCl lCl lCl',}
)
classy_sz.compute_class_szfast()

print('sigma8:',classy_sz.sigma8())
print('A_s:',classy_sz.get_current_derived_parameters(['A_s']))
print('m_ncdm_in_eV:',classy_sz.get_current_derived_parameters(['m_ncdm_in_eV']))

