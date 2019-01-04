"""
    Database of test data
"""

options = {
    # Bare substrate
    '30889': dict(sc='REF_M_30889', db='30886', path='/SNS/REF_M/IPTS-21391/nexus/REF_M_30889.nxs.h5',
                  ref='/SNS/users/m2d/git/reflectivity_ui/test/notebooks/data/REF_M_30889+30890_Specular_Off_Off_v2_TOF_40.dat',
                  #refcst='/SNS/users/m2d/MR/reflectivity_30889.txt',
                  refcst='/SNS/users/m2d/git/reflectivity_ui/test/notebooks/data/REF_M_30889+30890_Specular_Off_Off_CSTQ_v2_TOF_40.dat',
                  peak_pos=157.5, peak=[149,167], bck=[47,105], beam=[75,161], tof=[13537,43265.4], scale=2.8379),

    '30886': dict(sc='REF_M_30886', db='30886', path='/SNS/REF_M/IPTS-21391/nexus/REF_M_30886.nxs.h5',
                  peak=[203,223], bck=[4,103], beam=[78,180]),

    '30887': dict(sc='REF_M_30887', db='30887', path='/SNS/REF_M/IPTS-21391/nexus/REF_M_30887.nxs.h5',
                  peak=[202,222], bck=[51,88], beam=[80,178]),

    '30891': dict(sc='REF_M_30891', db='30887', path='/SNS/REF_M/IPTS-21391/nexus/REF_M_30891.nxs.h5',
                  ref='/SNS/users/m2d/MR/REF_M_30891_Specular_Off_Off.dat',
                  #refcst='/SNS/users/m2d/MR/REF_M_30889+30890+30891_Specular_Off_Off_CSTQ.dat',
                  refcst='/SNS/users/m2d/MR/REF_M_30891_Specular_Off_Off_CSTQ.dat',
                  peak_pos=161.5, peak=[154,170], bck=[92,109], beam=[74,164], tof=[13537,43265.4], scale=1.0),
    '30806': dict(sc='REF_M_30806', db='30794', path='/SNS/REF_M/IPTS-21391/nexus/REF_M_30806.nxs.h5',
                  ref='/SNS/users/m2d/MR/REF_M_30806_Specular_Off_Off.dat',
                  refcst='/SNS/users/m2d/MR/REF_M_30806_Specular_Off_Off_CSTQ.dat',
                  peak_pos=186.5, peak=[180,194], bck=[23,105], beam=[69,168], tof=[13537,43265.4], scale=1.0),
    '30794': dict(sc='REF_M_30794', db='30794', path='/SNS/REF_M/IPTS-21391/nexus/REF_M_30794.nxs.h5',
                  peak=[202,216], bck=[5,105], beam=[71,175]),

    '30906': dict(sc='REF_M_30906', db='30796', path='/SNS/REF_M/IPTS-21391/nexus/REF_M_30906.nxs.h5',
                  ref='/SNS/users/m2d/MR/REF_M_30906_Specular_On_Off.dat',
                  refcst='/SNS/users/m2d/MR/REF_M_30906_Specular_On_Off_CSTQ.dat',
                  #ref='/SNS/users/m2d/MR/REF_M_30906_Specular_Off_Off.dat',
                  #refcst='/SNS/users/m2d/MR/REF_M_30906_Specular_Off_Off_CSTQ.dat',
                  peak_pos=154.5, peak=[148,162], bck=[5,105], beam=[75,156], tof=[13537,43265.4], scale=1.0),
    '30796': dict(sc='REF_M_30796', db='30796', path='/SNS/REF_M/IPTS-21391/nexus/REF_M_30796.nxs.h5',
                  peak=[202,218], bck=[94,104], beam=[82,177]),

}

def retrieve(run):
    return options[run], options[options[run]['db']]


