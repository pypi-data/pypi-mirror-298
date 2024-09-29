from classy_sz import Class
Mclass_sz = Class()
class_sz_cosmo_params = {
 # 'Omega_b': 0.049,
 'omega_b': 0.049*(67.11/100.)**2,
 'Omega_cdm': 0.2685,
 'H0': 67.11,
 'sigma8': 0.834,
 'n_s': 0.9624}


# Mclass_sz.set(class_sz_cosmo_params) 
Mclass_sz.set({


'output': 'tSZ_1h,tSZ_2h',
'non_linear':'hmcode',
'pressure profile':'B12',
'delta for electron pressure':'200c',
"concentration parameter":"D08",
"ell_min" : 2,
"ell_max" : 9725,
'dell': 0,
'dlogell': 0.1,
    
'M_min' : 4.9e11, # got from will on 24/05/24
'M_max' : 2.2e15,# got from will on 24/05/24

'z_min': 0.03,
'z_max': 4.,# got from will on 24/05/24
    
    
# 'n_z_pressure_profile': 500,
# 'n_m_pressure_profile' : 500,
# 'n_l_pressure_profile' : 500,
    
'l_min_gas_pressure_profile' :  1.e-2,
'l_max_gas_pressure_profile' :  5.e4,    

'pressure_profile_epsrel':1e-4,
'pressure_profile_epsabs':1e-100,
    

    
    
'hm_consistency' : 0,
    

'use_fft_for_profiles_transform' : 1,
'x_min_gas_pressure_fftw' : 1e-5,
'x_max_gas_pressure_fftw' : 1e5,
'N_samp_fftw' : 8192,
    
    
# 'ndim_masses' : 500,
# 'ndim_redshifts' :100,
'redshift_epsrel': 1e-6,
'redshift_epsabs': 1e-100,
'mass_epsrel':1e-6,
'mass_epsabs':1e-100,    
    

'truncate_gas_pressure_wrt_rvir' : 1,
'x_outSZ': 2.,
'mass function' : 'T08M200c',
# 'T10_alpha_fixed' : 1,
    
    
'P_k_max_h/Mpc': 10.,
'k_per_decade_class_sz':80.,
'k_min_for_pk_class_sz':1e-4,
'k_max_for_pk_class_sz': 10*0.7, 

})
Mclass_sz.compute()
# Mclass_sz.compute_class_szfast()

cl_sz = Mclass_sz.cl_sz()
print(cl_sz)
