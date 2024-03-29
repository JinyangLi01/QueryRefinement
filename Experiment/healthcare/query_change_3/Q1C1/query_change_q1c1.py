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

from Algorithm import ProvenanceSearchValues_7_20220827 as ps
from Algorithm import LatticeTraversal_4_20220901 as lt

minimal_refinements1 = []
minimal_added_refinements1 = []
running_time1 = []

minimal_refinements2 = []
minimal_added_refinements2 = []
running_time2 = []


data_file = r"../../../../InputData/Healthcare/incomeK/before_selection_incomeK.csv"
query_file_prefix = r"./query"

time_limit = 5*60

def run_constraint(c):
    print("running query change constraint {}".format(c))
    constraint_file = r"./constraint" + str(c) + ".json"

    time_output_file = r"./query_change_q1c1_1.csv"
    time_output = open(time_output_file, "w")
    time_output.write("income,PS,LT\n")

    result_output_file = r"./result_q1c1_1.txt"
    result_output = open(result_output_file, "w")
    result_output.write("selection file, result\n")

    for i in range(0, 10):
        print("query", i)
        query_file = query_file_prefix + str(i) + ".json"
        print("========================== provenance search ===================================")
        minimal_refinements1, running_time1, assign_to_provenance_num, \
        provenance_time, search_time = \
            ps.FindMinimalRefinement(data_file, query_file, constraint_file, time_limit)

        print("running time = {}".format(running_time1))

        running_time2 = 0
        # print("========================== lattice traversal ===================================")
        # minimal_refinements2, minimal_added_refinements2, running_time2 = \
        #     lt.FindMinimalRefinement(data_file, query_file, constraint_file, time_limit)
        # if running_time2 > time_limit:
        #     print("naive alg out of time with {} time limit".format(time_limit))
        # else:
        #     print("running time = {}".format(running_time2))
        print(*minimal_refinements1, sep="\n")
        result_output.write("\n")
        idx = i * 50
        time_output.write("{},{:0.2f},{:0.2f},{:0.2f}\n".format(idx, running_time1, provenance_time,
                                                                search_time))
        result_output.write("{}\n".format(idx))
        result_output.write(", ".join(str(item) for item in minimal_added_refinements1))
        result_output.write("\n")
        result_output.write("\n".join(str(item) for item in minimal_refinements1))
        result_output.write("\n")
    result_output.close()
    time_output.close()


run_constraint(1)
