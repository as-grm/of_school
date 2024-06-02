#!/bin/bash

path=$(pwd)

rm -rf *~
rm -rf slurm*

$path/cylinder_mesh/Allclean
$path/steady/Allclean
$path/transient/Allclean
