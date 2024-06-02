import os
import sys, getopt
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

# *** Generate data for boundary layer grading for turbulent model ***

def wall_distance(rho, mu, U, L, yPlus): # Calculation of the size for the size of first layer, based on Y+

    Re = rho * U * L / mu
    Cf = (2 * mat.log10(Re) - 0.65)**(-2.3)
    tau_w = Cf * 0.5 * rho * U**2
    uf = mat.sqrt(tau_w/rho)

    y = (yPlus * mu) / (rho * uf)

    return [Re, y]

# calculate number of layers to cover all BL thickness
def number_of_layers(h1, sf, Re, L):

    d = L * 0.37 * Re**(-1/5) # estimate of boundary layer thickness

    # estimate number of layers to cover BL delta
    # from equation H = h1 * (1 - sf**(N-1))/(1 - sf), describing total height of N layers with inflation scaling factor sf,
    # we derive N setting d = H
    N = mat.ceil(1 + mat.log(1 - d/h1*(1-sf))/mat.log(sf))

    H = h1 * (1 - sf**(N-1))/(1 - sf)

    #print('delta: {:.3e} m'.format(d))
    #print('H: {:.3e} m'.format(H))
    #print('N: {:d}'.format(N))

    return [int(N), d, H]

# Calculate BL height
def get_BL_total_height(h1, sf, N0, R):

    sr = sf**(N0-1)   # OF scale factor hn/h1
    h_last = h1 * sr # height of the last Nth layer
    H = h1 * (1 - sr)/(1 - sf) # total height of N layers

    if H > 0.2*R:
        print(' *** WARNING: H > R*0.2; N is too big. Calculating new N!')
        H = 0
        N = 1
        while H < 0.2*R:
            sr = sf**(N-1)   # OF scale factor hn/h1
            h_last = h1 * sr # height of the last Nth layer
            H = h1 * (1 - sr)/(1 - sf) # total height of N layers
            N += 1
        print('     -> old N={:d}, new N={:d}'.format(N0,N))
    else:
        N = N0

    return [h_last, H, N]

def geometry_dict(R):
    
    geometry_dict = {}
    geometry_dict['R'] = '{:.2f}'.format(R)
    geometry_dict['tb1_y1'] = '{:.2f}'.format(15*R)
    geometry_dict['tb1_y2'] = '{:.2f}'.format(15*R)
    geometry_dict['fr1_x'] = '{:.2f}'.format(10*R)
    geometry_dict['ba1_x'] = '{:.2f}'.format(50*R)
    geometry_dict['tb2_y1'] = '{:.2f}'.format(2*R)
    geometry_dict['tb2_y2'] = '{:.2f}'.format(2*R)
    geometry_dict['fr2_x'] = '{:.2f}'.format(2*R)
    geometry_dict['ba2_x1'] = '{:.2f}'.format(2*R)
    geometry_dict['ba2_x2'] = '{:.2f}'.format(20*R)
    geometry_dict['zEf'] = '{:.2e}'.format(R/2)
    
    return geometry_dict


def grading_dict(g1_fr, g1_ba, g2_fr, g2_ba, gC):
    
    grading_dict = {}
    grading_dict['g1_fr'] = '{:.5f}'.format(g1_fr)
    grading_dict['g1_ba'] = '{:.5f}'.format(g1_ba)
    grading_dict['g2_fr'] = '{:.5f}'.format(g2_fr)
    grading_dict['g2_ba'] = '{:.5f}'.format(g2_ba)
    grading_dict['gC'] = '{:.5f}'.format(gC)
    
    return grading_dict

def boundary_layer_dict(bl_h1, bl_H, bl_sf):

    bl_dict = {}
    bl_dict['bl_h1'] = '{:.2e}'.format(bl_h1)
    bl_dict['bl_H'] = '{:.2e}'.format(bl_H)
    bl_dict['bl_sf'] = '{:.2f}'.format(bl_sf)

    return bl_dict

def velocity_dict(v):

    v_dict = {}
    v_dict['v_start'] = '( {:.5f} 0 0 )'.format(v)

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
def main(argv):

    geo_template_file = 'constant/geometry/gmsh_template.geo'
    U_template_file = '0.org/U_template'

    try:
        opts, args = getopt.getopt(argv,'h,U:R:Y:',['help','velocity=','radius=','yPlus='])
        if len(opts) < 3:
            print('Usage: cylinder_gmsh_generator.py -U <velocity in [m/s]> -R <cylinder radius in [m]> -Y <Y+ parameter>')
            exit(0)
    except getopt.GetoptError:
        print('cylinder_gmsh_generator.py -U <velocity in [m/s]> -R <cylinder radius in [m]> -Y <Y+ parameter>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h','--help'):
            print ('Usage: cylinder_gmsh_generator.py -U <velocity in [m/s]> -R <cylinder radius in [m]> -Y <Y+ parameter>')
            sys.exit()
        elif opt in ('-U', '--velocity'):
            inp_U = float(arg)
        elif opt in ('-R', '--radius'):
            inp_R = float(arg)
        elif opt in ('-Y', '--yPlus'):
            inp_yP = float(arg)


    # geometry dictionary
    R = inp_R
    geo_dict = geometry_dict(R)

    # boundary layer dictionary
    # neede parameters for turbulent layer calculation
    #
    rho = 1000     # density [kg/m3]
    mu = 1e-3      # dynamic viscosity [Pa s]
    U = inp_U      # freestream velocity [m/s]
    L = inp_R      # length scale in flow [m]; length of surface
    yPlus = inp_yP # desidered y+


    # height of first BL
    #
    bl_sf = 1.2   # inflation scaling factor
    [Re, bl_h1] = wall_distance(rho, mu, U, L, yPlus)
    [bl_N0, delta, H_calculated] = number_of_layers(bl_h1, bl_sf, Re, L) # number of layers, BL delta, mesh delta
    # last layer height and total height of the BL layer
    [bl_hN, bl_H, bl_N] = get_BL_total_height(bl_h1, bl_sf, bl_N0, R)
    bl_dict = boundary_layer_dict(bl_h1, bl_H, bl_sf)

    # geometry grading dictionary
    # g2_fr = 40*bl_hN # kw-SST
    g2_fr = 10*bl_hN # kw-SST-SAS
    g2_ba = 5*g2_fr
    g1_fr = 5*g2_fr
    g1_ba = 2*g1_fr
    gC = bl_hN
    grad_dict = grading_dict(g1_fr, g1_ba, g2_fr, g2_ba, gC)

    # join dictionaries and replace variables with values
    gmsh_dict = {**geo_dict, **grad_dict, **bl_dict}
    replace_vars(geo_template_file, 'gmsh.geo', gmsh_dict)

    vel_dict = velocity_dict(U)
    replace_vars(U_template_file, '0.org/U', vel_dict)

    print('*******************************')
    print('*** GMSH geometry generator ***')
    print('*******************************')
    print()
    print('* Input parameters:')
    print('   ->     Inlet velocity: {:.2e} m/s'.format(inp_U))
    print('   ->    Cylinder radius: {:.2e} m'.format(inp_R))
    print('   ->            Density: {:.1f} kg/m3'.format(rho))
    print('   ->  Dynamic viscosity: {:.3e} Pa s'.format(mu))
    print('   ->             Y plus: {:.1f}'.format(yPlus))
    print('   ->              delta: {:.3e} m'.format(delta))
    print('   ->   BL thickness (H): {:.3e} m'.format(H_calculated))
    print('   ->       calculated N: {:d}'.format(bl_N0))
    print()
    print('* GMSH boundary layer parameters:')
    print('   ->      Re: {:.2e}'.format(Re))
    print('   ->      sf: {:.2f}'.format(bl_sf))
    print('   ->       N: {:d}'.format(bl_N))
    print('   -> first h: {:.5e} m'.format(bl_h1))
    print('   ->  last h: {:.5e} m'.format(bl_hN))
    print('   -> total H: {:.5e} m'.format(bl_H))
    print()
    print('-------------------------------------')
    print('Results written to gmsh.geo file!')
    print()

if __name__ == "__main__":
   main(sys.argv[1:])


