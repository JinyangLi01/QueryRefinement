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

from Algorithm import ProvenanceSearchValues_4_20220712 as ps
from Algorithm import LatticeTraversal_2_2022405 as lt

data_file = r"../../../InputData/Healthcare/incomeK/before_selection_incomeK.csv"
query_file_prefix = r"../../../InputData/Healthcare/incomeK/query"
constraint_file_prefix = r"../../../InputData/Healthcare/incomeK/constraint"

time_output_prefix = r"./result_"


def file(q, c):
    time_output_file = time_output_prefix + str(q) + str(c) + ".csv"
    time_output = open(time_output_file, "w")
    time_output.write("selection file, running time ps, running time lt\n")
    return time_output

time_limit = 60 * 5


def compare(q, c):
    print("run with query{} constraint{}".format(q, c))
    query_file = query_file_prefix + str(q) + ".json"
    constraint_file = constraint_file_prefix + str(c) + ".json"

    print("========================== provenance search ===================================")
    minimal_refinements1, running_time1 = \
        ps.FindMinimalRefinement(data_file, query_file, constraint_file, time_limit)

    print("running time = {}".format(running_time1))
    print(*minimal_refinements1, sep="\n")

    print("========================== lattice traversal ===================================")

    minimal_refinements2, minimal_added_refinements2, running_time2 = \
        lt.FindMinimalRefinement(data_file, query_file, constraint_file, time_limit)
    if running_time2 > time_limit:
        print("naive alg out of time")
    else:
        print("running time = {}".format(running_time2))
        print(*minimal_refinements2, sep="\n")


    time_output.write("\n")
    idx = "q" + str(q) + "c" + str(c)
    time_output.write("{}, {:0.2f}\n".format(idx, running_time1))
    time_output.write("{}\n".format(idx))
    time_output.write("\n".join(str(item) for item in minimal_refinements1))
    time_output.write("\n")

time_output = file(2, 1)
compare(2, 1)

time_output.close()
