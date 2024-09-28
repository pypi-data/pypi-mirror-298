
import numpy as np
from classy_sz import Class as Class_sz
import os
import time


cosmo_params_with_sigma_8 = {
'Omega_b': 0.05,
'omega_c':  0.11933,
'H0': 67.66, # use H0 because this is what is used by the emulators and to avoid any ambiguity when comparing with camb. 
'tau_reio': 0.0561,
'sigma8': 0.8118,
'n_s': 0.9665,
'm_ncdm': 0.02,

}


classy_sz = Class_sz()
classy_sz.set(cosmo_params_with_sigma_8)
classy_sz.set({
'output':'tCl,lCl,pCl',
'skip_chi':0,
'skip_hubble':0,     
'cosmo_model': 1   
})


start_time = time.time()
classy_sz.compute_class_szfast()
print("Execution time: {:.5f} seconds".format(time.time() - start_time))

# print('sigma8:',classy_sz.sigma8())
# print('A_s:',classy_sz.get_current_derived_parameters(['A_s']))
# print('m_ncdm_in_eV:',classy_sz.get_current_derived_parameters(['m_ncdm_in_eV']))

print('DA',classy_sz.angular_distance(1.))
print('Hubble',classy_sz.Hubble(1.))


classy_sz = Class_sz()
classy_sz.set(cosmo_params_with_sigma_8)
classy_sz.set({
'output':'tCl,lCl,pCl',
'skip_chi':0,
'skip_hubble':0,     
'cosmo_model': 6   
})
start_time = time.time()
classy_sz.compute_class_szfast()
print("Execution time: {:.5f} seconds".format(time.time() - start_time))

print('DA',classy_sz.angular_distance(1.))
print('Hubble',classy_sz.Hubble(1.))