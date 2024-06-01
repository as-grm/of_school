#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 31 14:04:23 2022

@author: sandro
"""

def replaceItem(iter_lines, check_str, new_line):
    
    line_list = []
    
    while True:
        try:
            line = next(iter_lines)
        except StopIteration:
            return line_list

        if check_str in line:
            line_list.append(new_line)
            return line_list
        else:
            line_list.append(line.rstrip())
        
def replacePatches(fn):
    
    replaced = []
    
    fp = open(fn, 'r')
    fLines = fp.readlines()
    iter_lines = iter(fLines)
    
    line = next(iter_lines)
    while True:
        if 'cylinder' in line:
            replaced.append(line.rstrip())
            new_lines = replaceItem(iter_lines, 'type', '\t\ttype            wall;')
            replaced.extend(new_lines)
            new_lines = replaceItem(iter_lines, 'physicalType', '\t\tinGroups        1(wall);')
            replaced.extend(new_lines)
        elif 'top' in line:
            replaced.append(line.rstrip())
            new_lines = replaceItem(iter_lines, 'type', '\t\ttype            symmetry;')
            replaced.extend(new_lines)
            new_lines = replaceItem(iter_lines, 'physicalType', '\t\tinGroups        1(symmetry);')
            replaced.extend(new_lines)
        elif 'bottom' in line:
            replaced.append(line.rstrip())
            new_lines = replaceItem(iter_lines, 'type', '\t\ttype            symmetry;')
            replaced.extend(new_lines)
            new_lines = replaceItem(iter_lines, 'physicalType', '\t\tinGroups        1(symmetry);')
            replaced.extend(new_lines)
        elif 'defaultFaces' in line:
            replaced.append(line.rstrip())
            new_lines = replaceItem(iter_lines, 'type', '\t\ttype            empty;')
            replaced.extend(new_lines)
        else:
            replaced.append(line.rstrip())
        
        try:
            line = next(iter_lines)
        except StopIteration:
            return replaced
      
      
fn = 'constant/polyMesh/boundary'
file = replacePatches(fn)

for l in file:
    print(l)
