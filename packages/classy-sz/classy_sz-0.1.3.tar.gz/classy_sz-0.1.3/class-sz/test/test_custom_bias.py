import classy_szfast
import classy_sz
from classy_sz import Class as Class_sz

path_to_class_sz = "/Users/boris/Work/CLASS-SZ/SO-SZ/class_sz/class-sz/"
path_to_class_sz_files =  path_to_class_sz+"class_sz_auxiliary_files/excludes/galaxies/"

cosmo_params = {
'omega_b': 0.022,
'omega_cdm':  0.122,
'H0': 67.5, 
'tau_reio': 0.0561,
'ln10^{10}A_s': 3.047,
'n_s': 0.965,
'k_pivot': 0.05, 
'N_ncdm': 1,
'N_ur': 2.0328,
'm_ncdm': 0.06 
}

class_sz = Class_sz()

class_sz.set(cosmo_params)



common_params = {

# here gal_gal_1h and gal_gal_2h correspond to the HOD calculation
# while gal_gal_hf is the linear bias calculation
# dndlnm ensures we can access the halo-function after computation
'output': 'gal_gal_1h,gal_gal_2h,gal_gal_hf,dndlnm',    

'galaxy_sample' : 'custom', # custom made galaxy sample
'full_path_to_dndz_gal':path_to_class_sz_files+'/dndz_quaia.txt', # redshift distribution of custom made galaxy sample

# pick redshift range
'z_min' : 0.005,
'z_max' : 3.0,
    
'has_b_custom1': 1, # do you want a cutom function for b(z)? yes: 1, no: 0
'array_b_custom1_n_z': 100, # precision parameters for z sampling of b(z)    
'non_linear' : 'hmcode', # non-linear model for matter P(k), e.g., 'hmcode' or 'halofit'
'effective_galaxy_bias': 2.,
# for the custom bias function we want: 
# b(z) = bquaia(z,bl) as defined above
# We code this in path_to_class_sz/python/classy_szfast/classy_szfast/custom_bias/custom_bias.py
    
    
# pick mass range (relevant for HOD prediction)
'M_min' : 1e11, 
'M_max' : 1e15,
    

    
# Other parameters relevant for HOD predictions
'mass function' : 'T08M200c', # halo mass function, e.g., Tinker et al 2008 defined at M200c
'concentration parameter' : 'B13', # halo concentration parameter  

# main HOD parameters controlling Nc, Ns
'sigma_log10M_HOD': 0.68,
'alpha_s_HOD':    1.30,
'M1_prime_HOD': 10**12.7, # msun/h
'M_min_HOD': 10**11.8, # msun/h
'M0_HOD' :0,
    
# these are not important (maybe for fine-tuning HOD)
'x_out_truncated_nfw_profile_satellite_galaxies':  1.,
'f_cen_HOD' : 1., 
'hm_consistency' : 0,
    
}

# if you need other cosmological parameters
# do: 
cosmo_params.update(
{
'omega_cdm':0.11,
}
)

class_sz.set(common_params)

class_sz.compute_class_szfast()

