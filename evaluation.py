import os
import re

filename = 'ecoli-200.txt'

node_list = []
ecoil = []

with open(filename, 'rt') as file:
    for line in file:
        node_list.append(line)
        if re.findall(r"NC_000913.3.*", line):
            ecoil.append(line)

print('SGA overlap -m 200:')
print('total number of reads in graph: ' + str(len(node_list)))
print('total number of E-coil reads in graph: ' + str(len(ecoil)))
print('accuracy: ' + str(len(ecoil)/len(node_list)))