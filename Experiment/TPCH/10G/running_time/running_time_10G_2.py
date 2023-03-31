"""
executable
without optimizations
"""

import copy
from typing import List, Any
import numpy as np
import pandas as pd
import time
from intbitset import intbitset
import json
import sys
sys.path.append(r"../../../../")

from Algorithm import ProvenanceSearchValues_8_20230119 as ps
from Algorithm import LatticeTraversal_5_20230121 as lt


data_file_prefix = r"../../../../InputData/TPC-H/10Gdata/"
query_file_prefix = r"../"
constraint_file_prefix = r"../"
time_limit = 60 * 60 * 2

time_output_prefix = r"./result_"


def file(q, c):
    time_output_file = time_output_prefix + "q" + str(q) + c + ".csv"
    time_output = open(time_output_file, "w")
    time_output.write("selection file, running time ps, running time lt\n")
    return time_output



def compare(q, c, time_output):
    print("run with query {} constraint {} ".format(q, c))
    query_file = query_file_prefix + "q" + str(q) + "/q" + str(q) + ".json"
    constraint_file = constraint_file_prefix + "q" + str(q) + "/constraint_" + c + ".json"

    minimal_refinements1 = []
    running_time1, provenance_time1, search_time1 = 0, 0, 0
    print("========================== provenance search ===================================")
    minimal_refinements1, _, running_time1, _, \
        provenance_time1, search_time1 = \
        ps.FindMinimalRefinement(data_file_prefix, separator, query_file, constraint_file, format, time_limit)

    print("running time = {}".format(running_time1))
    print(*minimal_refinements1, sep="\n")

    minimal_refinements2 = []
    running_time2, provenance_time2, search_time2 = 0, 0, 0
    # print("========================== lattice traversal ===================================")
    #
    # minimal_refinements2, minimal_added_refinements2, running_time2, provenance_time2, search_time2 = \
    #     lt.FindMinimalRefinement(data_file_prefix, separator, query_file, constraint_file, time_limit)
    # if running_time2 > time_limit:
    #     print("naive alg out of time")
    # else:
    #     print("running time = {}".format(running_time2))
    #     print(*minimal_refinements2, sep="\n")


    time_output.write("\n")
    idx = "Q" + str(q) + "C" + c
    time_output.write("{},{:0.2f},{:0.2f},{:0.2f}\n".format(idx, running_time1, provenance_time1, search_time1))
    if running_time2 < time_limit:
        time_output.write("{},{:0.2f},{:0.2f},{:0.2f}\n".format(idx, running_time2, provenance_time2, search_time2))

    time_output.write("\n\n=================================== provenance search ===================================\n")
    time_output.write("\n".join(str(item) for item in minimal_refinements1))
    time_output.write("\n")
    time_output.write("\n\n=================================== baseline ===================================\n")
    time_output.write("\n".join(str(item) for item in minimal_refinements2))
    time_output.write("\n")
    # summary_file.write(("{},{:0.2f},".format(idx, running_time1)))
    # if running_time2 < time_limit:
    #     summary_file.write("{:0.2f}\n".format(running_time2))
    # else:
    #     summary_file.write("\n")

# summary_file = open(r"time.csv", "w")
# summary_file.write("file,PS,LT\n")


def run(q, c):
    time_output = file(q, c)
    compare(q, c, time_output)
    time_output.close()

separator = '|'
format = ".tbl"

run(3, "refine1")



