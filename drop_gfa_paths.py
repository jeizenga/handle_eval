#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 18:57:54 2019

@author: Jordan
"""

import sys
import os
import gzip
import subprocess

if __name__ == "__main__":
    
    test_dir = sys.argv[1]
    out_dir = sys.argv[2]  
    
    for file_name in os.listdir(test_dir):
        if not file_name.endswith(".gfa") or file_name.endswith(".gfa.gz"):
            continue
        
        is_gzipped = file_name.endswith(".gz")        
        
        out_file_name = file_name[:file_name.index(".gfa")] + ".nopaths.gfa"      
        
        found_paths = False  
        
        in_file = None
        if is_gzipped:
            in_file = gzip.open(os.path.join(test_dir, file_name))
        else:
            in_file = open(os.path.join(test_dir, file_name))
        
        with open(os.path.join(out_dir, out_file_name), "w") as out:
            for line in in_file:
                if not (line.startswith("P") or line.startswith("O")):
                    out.write(line)
                else:
                    found_paths = True
        
        if not found_paths:
            os.remove(os.path.join(out_dir, out_file_name))
        elif is_gzipped:
            subprocess.check_call(["gzip", os.path.join(out_dir, out_file_name)])