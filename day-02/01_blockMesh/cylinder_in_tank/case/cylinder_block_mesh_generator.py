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

# Generate mesh division dictonary
def get_mesh_division_scale(nd_bl, nd_nose, nd_tail, md_mid, nd_front, nd_back, nd_tb, scale_bl, scale_nose, scale_tail, scale_mid, scale_front, scale_back, scale_tb):

    mesh_dict = {}

    # number of division points of a specific edge
    mesh_dict['nd_bl'] = '{:d}'.format(nd_bl)      # boundary layer
    mesh_dict['nd_nose'] = '{:d}'.format(nd_nose)  # edge 12-19 and 12-13
    mesh_dict['nd_tail'] = '{:d}'.format(nd_tail)  # edge 16-17 and 16-15
    mesh_dict['nd_mid'] = '{:d}'.format(nd_mid)    # edge 16-17 and 16-15
    mesh_dict['nd_front'] = '{:d}'.format(nd_tail) # edge 11-10, 6-5, 23-22
    mesh_dict['nd_back'] = '{:d}'.format(nd_tail)  # edge 20-21, 8-9, 25-26
    mesh_dict['nd_tb'] = '{:d}'.format(nd_tb)      # edge bottom: 5-0, 6-1, 7-2, 8-3, 9-4, top: 22-27, 23-28, 24-29, 25-30, 26-31

    # scailing factor in edge direction
    mesh_dict['s_bl'] = '{:d}'.format(scale_bl)       # vertically in boundary layer
    mesh_dict['s_nose'] = '{:d}'.format(scale_nose)   # edge 12-13, 12-19
    mesh_dict['s_tail'] = '{:d}'.format(scale_tail)   # edge 16-17 and 16-15
    mesh_dict['s_mid'] = '{:.5f}'.format(scale_mid)   # edge 14-13 and 14-15 and opposite side
    mesh_dict['s_front'] = '{:d}'.format(scale_tail)  # edge 11-10, 6-5, 23-22
    mesh_dict['s_back'] = '{:d}'.format(scale_tail)   # edge 20-21, 8-9, 25-26
    mesh_dict['s_tb'] = '{:d}'.format(scale_tb)       # edge bottom: 5-0, 6-1, 7-2, 8-3, 9-4, top: 22-27, 23-28, 24-29, 25-30, 26-31

    return mesh_dict

# replace vriables in the template file
def replace_vars(fn_template, fn_mesh, database):

    # Load the template
    template = blockmesh_jinja_env.get_template(fn_template)
   
    # combine template and variables
    document = template.render(database)

    f = open(fn_mesh, 'w', encoding='utf-8')
    f.write(document)

# Main part

# geometry parameters
R1 = 1 # Inner radius
R2 = 2 # Outer radius
k1 = 2 # top-bottom scaling of R2
k2 = 1 # front scaling of R2
k3 = 5 # back scaling of R2

# mesh parameters
# 1. number of edge divisions
nd_bl = 20     # boundary layer direction
nd_nose = 40   # from tip to mid
nd_tail = 20   # from tail to mid
nd_mid = 10    # middle foil section
nd_front = 20  # front part, form nose to inlet
nd_back = 20   # back part , from tail to outlet
nd_tb = 20     # top-bottom part, from mid to TB

# 2. scaling factors for simplegrade
#
# Scale factor or grading is acalculateda as a ratio between the "first cell size"/"last cell size"
scale_bl = 4     # scale factor in BL
scale_nose = 5   # scale factor for nose part
scale_tail = 3   # scale fctor for tail part
scale_mid = 1/3  # scale factor for mid part
scale_front = 2  # scale factor of front part
scale_back = 2   # scale factor of back part
scale_tb = 2     # scale factor of top-bottom direction

# get dictionaroes for variables
vertices_dict = get_vertex_oordinates(R1,R2,k1,k2,k3)
mesh_dict = get_mesh_division_scale(nd_bl, nd_nose, nd_tail, nd_mid, nd_front, nd_back, nd_tb, scale_bl, scale_nose, scale_tail, scale_mid, scale_front, scale_back, scale_tb)

# join dictionaries and replace variables with values
bm_dict = {**vertices_dict, **mesh_dict}
replace_vars('constant/geometry/blockMeshDict_template', 'system/blockMeshDict', bm_dict)
