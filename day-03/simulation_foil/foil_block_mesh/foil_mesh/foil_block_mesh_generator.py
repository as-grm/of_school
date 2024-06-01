import os
import math as mat
import numpy as np

import jinja2

# Tell jinja what to look for in the template
blockmesh_jinja_env = jinja2.Environment(
    variable_start_string=r"\VAR{",
    variable_end_string=r"}",
    comment_start_string=r"\#{",
    comment_end_string="}",
    loader=jinja2.FileSystemLoader(os.path.abspath(".")),
)

def foil_profile(x,t):

    # NACA simmetric 4 digit 00XX
    y = 5*t*( 0.2969*mat.sqrt(x) - 0.1260*x - 0.3516*x**2 + 0.2843*x**3 - 0.1015*x**4)

    return y


def spline_arc_format(arc_pts,h):

    #pts = np.transpose(arc_pts)
    txt = ''
    for p in arc_pts:
        txt += '\t\t({:.5f} {:.5f} {:s})\n'.format(p[0],p[1],h)

    return txt


def foil_profile_data(t,N,a):
    # t - maximum thickness
    # N - number of control points

    xp = np.linspace(0,1,N)
    #model = 'linear'
    model ='exp'

    if model == 'linear':
        x = xp
    else:
        x = np.flip(np.exp(a*xp)-1)
        x = x/np.max(x)
    
    y = np.zeros(N-2)
    for i in range(1,N-1):
       y[i-1] = foil_profile(x[i],t)
    
    return [x[1:N-1],y]


def foil_spline_dict(t,N,a=5):
    
    [x,y] = foil_profile_data(t,N,a)
    # print('x:', x)
    # print('y:', y)
    
    uRp = np.transpose([x, y]) 
    lDp = np.transpose(np.flip(np.array([x, -y]),1)) 
    
    uRf_txt = spline_arc_format(uRp,'0')
    uRb_txt = spline_arc_format(uRp,'$dh')
    lDf_txt = spline_arc_format(lDp,'0')
    lDb_txt = spline_arc_format(lDp,'$dh')
    
    foil_dict = {}
    foil_dict['upperCurveRfront'] = uRf_txt
    foil_dict['upperCurveRback'] = uRb_txt
    foil_dict['lowerCurveDfront'] = lDf_txt
    foil_dict['lowerCurveDback'] = lDb_txt

    return foil_dict


def domain_dict(f_x, tb_y, b_x, fi):
    
    domain_dict = {}
    domain_dict['x_front'] = '{:d}'.format(f_x)
    domain_dict['y_tb'] = '{:d}'.format(tb_y)
    domain_dict['x_back'] = '{:d}'.format(b_x)
    domain_dict['y_back'] = '{:.5f}'.format(b_x * mat.tan(fi/180*mat.pi))
    
    return domain_dict


def velocity_dict(v,fi):
    
    vX = v * mat.cos(fi/180*mat.pi)
    vY = v * mat.sin(fi/180*mat.pi)
    
    v_dict = {}
    v_dict['v_start'] = '( {:.5f} {:.5f} 0 )'.format(vX,vY)
    
    return v_dict

# replace vriables in the template file
def replace_vars(fn_template, fn_mesh, database):

    # Load the template
    template = blockmesh_jinja_env.get_template(fn_template)
   
    # combine template and variables
    document = template.render(database)

    f = open(fn_mesh, 'w', encoding='utf-8')
    f.write(document)


# *****************
# *** Main part ***
# *****************

# domain geometry
front_x = 11      # fron distance from nose    
top_bottom_y = 12 # top bottom distance from centerline
back_x = 21       # back point from nose

# foil profile dictionary
profile_dict = foil_spline_dict(t, N)
# domain dictionary
domain_dict = domain_dict(front_x, top_bottom_y, back_x, fi)

# join dictionaries and replace variables with values
bm_dict = {**profile_dict, **domain_dict}
replace_vars('constant/geometry/blockmeshdict_template', 'system/blockMeshDict', bm_dict)


# Freestream Velocity with angle
v = 10 # [m/s]
vel_dict = velocity_dict(v, fi)
replace_vars('0.org/U_template', '0.org/U', vel_dict)
