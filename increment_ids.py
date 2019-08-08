#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 11:45:09 2019

@author: Jordan
"""

import os
import sys
import gzip

if __name__ == "__main__":
    
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]

    for file_name in os.listdir(input_dir):
        
        in_file_path = os.path.join(input_dir, file_name)
        out_file_path = os.path.join(output_dir, file_name)      
        
        in_file = None
        if file_name.endswith(".gfa"):
            in_file = open(in_file_path)
            out_file = open(out_file_path, "w")
        elif file_name.endswith(".gfa.gz"):
            in_file = gzip.open(in_file_path)
            out_file = gzip.open(out_file_path, "wt")
        else:
            continue
        
        parsed_header = False
        header = next(in_file)
        if type(header) == bytes:
            header = header.decode("utf-8")
        if header.startswith("H"):
            version = header.strip().split()[1]
            if version == "VN:Z:1.0":
                parsed_header = True
        
        if not parsed_header:
            out_file.close()
            os.remove(out_file_path)
            continue
            
        out_file.write(header)
        for line in in_file:
            if type(line) == bytes:
                line = line.decode("utf-8")
                
            line = line.strip()
                
            if line.startswith("S"):
                tokens = line.split("\t")
                tokens[1] = str(int(tokens[1]) + 1)
            elif line.startswith("L"):
                tokens = line.split("\t")
                tokens[1] = str(int(tokens[1]) + 1)
                tokens[3] = str(int(tokens[3]) + 1)
            elif line.startswith("P"):
                tokens = line.split("\t")
                path_tokens = tokens[2].split(",")
                for i in range(len(path_tokens)):
                    path_tokens[i] = str(int(path_tokens[i][:-1]) + 1) + path_tokens[i][-1]
                tokens[2] = ",".join(path_tokens)
            else:
                tokens = [line]
                
            print("\t".join(tokens), file = out_file)