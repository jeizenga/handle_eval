#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 18:14:58 2019

@author: Jordan
"""

import sys
import os
import random
import gzip
import subprocess

if __name__ == "__main__":
    
    test_dir = sys.argv[1]
    out_dir = sys.argv[2]
    min_mut_prob = float(sys.argv[3])
    max_mut_prob = float(sys.argv[4])
    
    assert(0.0 <= min_mut_prob and min_mut_prob <= max_mut_prob and max_mut_prob <= 1.0)
    
    for file_name in os.listdir(test_dir):
        if not file_name.endswith(".gfa") or file_name.endswith(".gfa.gz"):
            continue
        
        is_gzipped = file_name.endswith(".gz")
        
        out_file_name = file_name[:file_name.index(".gfa")] + ".mutilated.gfa"        
        
        mut_prob = random.uniform(min_mut_prob, max_mut_prob)
        
        in_file = None
        if is_gzipped:
            in_file = gzip.open(os.path.join(test_dir, file_name))
        else:
            in_file = open(os.path.join(test_dir, file_name))
        
        with open(os.path.join(out_dir, out_file_name), "w") as out:
            for line in in_file:
                if (not (line.startswith("L") or line.startswith("E"))) or random.random() > mut_prob:
                    out.write(line)
                    
        if is_gzipped:
            subprocess.check_call(["gzip", os.path.join(out_dir, out_file_name)])
                    