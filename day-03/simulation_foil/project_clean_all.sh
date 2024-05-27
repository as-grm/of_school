#!/bin/bash

path=$(pwd)

rm -rf *~

cd $path/foil_block_mesh
bash ./clean_all.sh

cd $path/foil_gmsh_mesh
bash ./clean_all.sh

cd $path
