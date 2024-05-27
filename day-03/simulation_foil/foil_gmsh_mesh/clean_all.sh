#!/bin/bash

path=$(pwd)

rm -rf *~

cd $path/foil_mesh
bash ./Allclean

cd $path/steady
bash ./Allclean

cd $path/transient
bash ./Allclean

cd $path
