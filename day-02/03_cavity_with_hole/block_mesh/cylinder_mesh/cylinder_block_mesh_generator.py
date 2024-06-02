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

# calculate vertex position based on geometry parametes
def get_vertex_oordinates(R1,R2,k1,k2,k3):

    # calculation of main geomtry parameters
    a1 = (R1 + R2)/2
    a2 = k1 * R2
    b1 = k2 * R2
    b2 = mat.sqrt(R2**2 - a1**2)
    b3 = b2
    b4 = k3 * R2
    h = 0.1 * R2

    vv = [] # vertex is of dict type [name : [x,y,z]]
    # lower line
    vv.append(['v0',[-(b1+b2),-(a1+a2),0]]) 
    vv.append(['v1',[-b2,-(a1+a2),0]]) 
    vv.append(['v2',[0,-(a1+a2),0]])
    vv.append(['v3',[b3,-(a1+a2),0]]) 
    vv.append(['v4',[b3+b4,-(a1+a2),0]])
    
    # next upper line
    vv.append(['v5',[-(b1+b2),-a1,0]])
    vv.append(['v6',[-b2,-a1,0]])
    vv.append(['v7',[0,-R2,0]])
    vv.append(['v8',[b3,-a1,0]])
    vv.append(['v9',[b3+b4,-a1,0]])

    # central line + inner circle
    vv.append(['v10',[-(b1+b2),0,0]])
    vv.append(['v11',[-R2,0,0]])
    vv.append(['v12',[-R1,0,0]])
    # inner circle - start
    vv.append(['v13',[-R1*mat.sin(mat.pi/4),-R1*mat.sin(mat.pi/4),0]])
    vv.append(['v14',[0,-R1,0]])
    vv.append(['v15',[R1*mat.sin(mat.pi/4),-R1*mat.sin(mat.pi/4),0]])
    vv.append(['v16',[R1,0,0]])
    vv.append(['v17',[R1*mat.sin(mat.pi/4),R1*mat.sin(mat.pi/4),0]])
    vv.append(['v18',[0,R1,0]])
    vv.append(['v19',[-R1*mat.sin(mat.pi/4),R1*mat.sin(mat.pi/4),0]])
    # inner circle - end
    vv.append(['v20',[R2,0,0]])
    vv.append(['v21',[b3+b4,0,0]])

    # next upper line
    vv.append(['v22',[-(b1+b2),a1,0]])
    vv.append(['v23',[-b2,a1,0]])
    vv.append(['v24',[0,R2,0]])
    vv.append(['v25',[b3,a1,0]])
    vv.append(['v26',[b3+b4,a1,0]])

    # lower line
    vv.append(['v27',[-(b1+b2),(a1+a2),0]]) 
    vv.append(['v28',[-b2,(a1+a2),0]]) 
    vv.append(['v29',[0,(a1+a2),0]])
    vv.append(['v30',[b3,(a1+a2),0]]) 
    vv.append(['v31',[b3+b4,(a1+a2),0]])

    vv_h = []
    i = 32
    for vi in vv:
        vp = [vi[1][0],vi[1][1],h]
        vs = 'v{:d}'.format(i)
        vv_h.append([vs,vp])
        i +=1

    for vi in vv_h:
        vv.append(vi)

    vv_dict = {}
    for vi in vv:
        vv_dict[vi[0]] = '({:.5f} {:.5f} {:.5f})\t// {:s}'.format(vi[1][0],vi[1][1],vi[1][2],vi[0])
        
    return vv_dict


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


# Set grading for BL in OF format
def get_OF_grading(bl_H, bl_sr, bl_hN, bl_N, L, h_last, N):

    p_bl = mat.ceil(bl_H/L * 100)  # percent of total length
    sf_2 = h_last/bl_hN            # OF grading factor for zone over BL

    str = ' (({:.3f} {:d} {:.3f})'.format(p_bl, bl_N, bl_sr)
    str += ' ({:.3f} {:d} {:.3f}))'.format(100-p_bl, N-bl_N, sf_2)

    return str

# set the OF output string for BL grading
def get_OF_grading_string(rho, mu, U, L, yPlus, bl_sf, R, R2):

    # BL mesh data calculation
    [Re, bl_h1] = wall_distance(rho, mu, U, L, yPlus)
    [bl_N0, delta, H_calculated] = number_of_layers(bl_h1, bl_sf, Re, L) # number of layers, BL delta, mesh delta
    # last layer height and total height of the BL layer
    [bl_hN, bl_H, bl_N] = get_BL_total_height(bl_h1, bl_sf, bl_N0, R)

    # find number of cells in second part of the block (above the BL layer)
    sf2 = 1.1
    N2 = mat.ceil(1 + mat.log(1 - (R2-R)/bl_hN*(1 - sf2))/mat.log(sf2))

    # get OF multi grading for boundary layer direction
    N_side = bl_N + N2     # numeber of cells for block in BL direction
    bl_sr = bl_hN/bl_h1 # scaling factor in BL wall zone
    bl_g_str = get_OF_grading(bl_H, bl_sr, bl_hN, bl_N, R2-R, 0.1*R, N_side)

    return [delta, H_calculated, bl_N0, Re, bl_sf, bl_N, bl_h1, bl_hN, bl_H, N_side, bl_g_str]


# Generate mesh division dictonary
def get_mesh_division_scale(nd_bl, nd_nose, nd_tail, nd_mid, nd_front, nd_back, nd_tb, scale_bl, scale_nose, scale_tail, scale_mid, scale_front, scale_back, scale_tb):

    mesh_dict = {}

    # number of division points of a specific edge
    mesh_dict['nd_bl'] = '{:d}'.format(nd_bl)      # boundary layer
    mesh_dict['nd_nose'] = '{:d}'.format(nd_nose)  # edge 12-19 and 12-13
    mesh_dict['nd_tail'] = '{:d}'.format(nd_tail)  # edge 16-17 and 16-15
    mesh_dict['nd_mid'] = '{:d}'.format(nd_mid)    # edge 16-17 and 16-15
    mesh_dict['nd_front'] = '{:d}'.format(nd_front) # edge 11-10, 6-5, 23-22
    mesh_dict['nd_back'] = '{:d}'.format(nd_back)  # edge 20-21, 8-9, 25-26
    mesh_dict['nd_tb'] = '{:d}'.format(nd_tb)      # edge bottom: 5-0, 6-1, 7-2, 8-3, 9-4, top: 22-27, 23-28, 24-29, 25-30, 26-31

    # scailing factor in edge direction
    mesh_dict['s_bl'] = '{:s}'.format(scale_bl)       # vertically in boundary layer
    mesh_dict['s_nose'] = '{:.2f}'.format(scale_nose)   # edge 12-13, 12-19
    mesh_dict['s_tail'] = '{:.2f}'.format(scale_tail)   # edge 16-17 and 16-15
    mesh_dict['s_mid'] = '{:.2f}'.format(scale_mid)   # edge 14-13 and 14-15 and opposite side
    mesh_dict['s_front'] = '{:.2f}'.format(scale_front)  # edge 11-10, 6-5, 23-22
    mesh_dict['s_back'] = '{:.2f}'.format(scale_back)   # edge 20-21, 8-9, 25-26
    mesh_dict['s_tb'] = '{:.2f}'.format(scale_tb)       # edge bottom: 5-0, 6-1, 7-2, 8-3, 9-4, top: 22-27, 23-28, 24-29, 25-30, 26-31

    return mesh_dict

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


# ********************
# *** Main program ***
# ********************
def main(argv):

    try:
        opts, args = getopt.getopt(argv, 'U:R:Y:', ['velocity=', 'radius=', 'yPlus='])
        if len(opts) < 3:
            print('USAGE: cylinder_block_mesh_generator.py  -U <velocity in [m/s]> -R <cylinder radius in [m]> -Y <Y+ parameter>')
            exit(0)
    except getopt.GetoptError:
        print('USAGE: cylinder_block_mesh_generator.py -U <velocity in [m/s]> -R <cylinder radius in [m]> -Y <Y+ parameter>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h': # help block
            print('USAGE: cylinder_block_mesh_generator.py -U <velocity in [m/s]> -R <cylinder radius in [m]> -Y <Y+ parameter>')
            sys.exit()
        elif opt in ('-U', '--velocity'):
            inp_U = float(arg)
        elif opt in ('-R', '--radius'):
            inp_R = float(arg)
        elif opt in ('-Y', '--yPlus'):
            inp_yP = float(arg)

    # BL calculation data
    rho = 1000     # density [kg/m3]
    mu = 1e-3      # dynamic viscosity [Pa s]
    U = inp_U      # freestream velocity [m/s]
    L = inp_R      # length scale in flow [m]; length of surface
    yPlus = inp_yP # desidered y+
    bl_sf = 1.2

    # geometry parameters
    R  = L   # Inner radius
    R2 = 4*L # Outer radius
    k1 = 3   # top-bottom scaling of R2
    k2 = 3   # front scaling of R2
    k3 = 10  # back scaling of R2

    # OF block mesh grading string and BL calculated data
    [delta, H_calculated, bl_N0, Re, bl_sf, bl_N, bl_h1, bl_hN, bl_H, N_side, bl_g_str] = get_OF_grading_string(rho, mu, U, L, yPlus, bl_sf, R, R2)

    print()
    print('*************************************************')
    print('*** BlockMesh geometry generator - calculated ***')
    print('*************************************************')
    print()
    print('* Input parameters:')
    print('   ->     Inlet velocity: {:.2e} m/s'.format(U))
    print('   ->    Cylinder radius: {:.2e} m'.format(L))
    print('   ->            Density: {:.1f} kg/m3'.format(rho))
    print('   ->  Dynamic viscosity: {:.3e} Pa s'.format(mu))
    print('   ->             Y plus: {:.1f}'.format(yPlus))
    print('   ->              delta: {:.3e} m'.format(delta))
    print('   ->   BL thickness (H): {:.3e} m'.format(H_calculated))
    print('   ->       calculated N: {:d}'.format(bl_N0))
    print()
    print('* Blockesh boundary layer parameters:')
    print('   ->      Re: {:.2e}'.format(Re))
    print('   ->      sf: {:.2f}'.format(bl_sf))
    print('   ->    bl_N: {:d}'.format(bl_N))
    print('   -> first h: {:.5e} m'.format(bl_h1))
    print('   ->  last h: {:.5e} m'.format(bl_hN))
    print('   -> total H: {:.5e} m'.format(bl_H))
    print('   ->       N: {:d}'.format(N_side))
    print()

    # number of divions cels
    nd_bl = N_side # boundary layer direction
    nd_nose = 10   # from tip to mid
    nd_tail = 10   # from tail to mid
    nd_mid = 10    # middle foil section
    nd_front = 20  # front part, form nose to inlet
    nd_back = 40   # back part , from tail to outlet
    nd_tb = 20     # top-bottom part, from mid to TB

    # scaling factors
    scale_bl = bl_g_str # scale factor in BL
    scale_nose = 1      # scale factor for nose part
    scale_tail = 1      # scale fctor for tail part
    scale_mid = 1       # scale factor for mid part
    scale_front = 2     # scale factor of front part
    scale_back = 5      # scale factor of back part
    scale_tb = 4        # scale factor of top-bottom direction


    # get dictionaroes for variables
    vertices_dict = get_vertex_oordinates(R,R2,k1,k2,k3)
    mesh_dict = get_mesh_division_scale(nd_bl, nd_nose, nd_tail, nd_mid, nd_front, nd_back, nd_tb, scale_bl, scale_nose, scale_tail, scale_mid, scale_front, scale_back, scale_tb)

    # join dictionaries and replace variables with values
    bm_dict = {**vertices_dict, **mesh_dict}
    replace_vars('constant/geometry/blockmeshdict_template', 'system/blockMeshDict', bm_dict)

    vel_dict = velocity_dict(U)
    replace_vars('0.org/U_template', '0.org/U', vel_dict)

if __name__ == "__main__":
   main(sys.argv[1:])
