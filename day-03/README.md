# OpenFOAM school - 3. day

**Content**

Demonstration of simple industrial project - **foil design numerical analysis**. Numerical simulation of flow
around the **NACA00XX** foils.

1. Foil parameters that can be changed:
   - thickness $h$
   - angle of attack $\alpha$
   - inlet velocity $U_\infty$
2. Comparison of *BlockMesh* and *GMSH* mesh design
3. Review of OpenFOAM postprocessing tools
   - $y^+$
   - pressure $p$ distribution around foil
   - analysis of force coefficients:
     - $C_\text{L}$: lift coefficient
     - $C_\text{D}$: drag coefficient
     - $C_\text{m}$: pitch moment coefficient
