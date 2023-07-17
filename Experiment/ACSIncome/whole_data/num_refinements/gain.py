import csv
import numpy as np


input_path = r'num_refinements.csv'
input_file = open(input_path, "r")

Lines = input_file.readlines()
num_refinements_bl = list()
num_refinements_ps = list()
x_list = list()

count = 0
# Strips the newline character
for line in Lines:
    count += 1
    if line == '\n':
        continue
    if count < 2:
        continue
    if count > 8:
        break
    items = line.strip().split(',')
    x_list.append(items[0])
    num_refinements_ps.append(float(items[1]))
    num_refinements_bl.append(float(items[2]))
    print((float(items[2]) - float(items[1]))/(float(items[2])))

