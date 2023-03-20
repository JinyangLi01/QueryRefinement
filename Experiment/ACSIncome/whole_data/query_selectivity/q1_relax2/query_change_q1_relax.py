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
sys.path.append(r"../../../../../")
from Algorithm import ProvenanceSearchValues_8_20230119 as ps
from Algorithm import LatticeTraversal_5_20230121 as lt

minimal_refinements1 = []
minimal_added_refinements1 = []
running_time1 = []

minimal_refinements2 = []
minimal_added_refinements2 = []
running_time2 = []

data_file_prefix = r"../../../data/"
query_file_prefix = r"./q"
time_limit = 10 * 60

time_output_prefix = r"./result_"


def run_constraint(q, c):
    print("running query change constraint {}".format(c))
    constraint_file = r"./constraint_" + c + ".json"

    time_output_file = r"./query_change_q" + str(q) + '_' + c + ".csv"
    time_output = open(time_output_file, "w")
    time_output.write("_,PS,PS_prov,PS_search,base,base_prov,base_search\n")

    result_output_file = r"./result_query_change_q" + str(q) + c + ".txt"
    result_output = open(result_output_file, "w")
    result_output.write("selection file, result\n")

    for i in range(0, 8):
        print("query", i)
        query_file = query_file_prefix + str(i) + ".json"
        print("========================== provenance search ===================================")
        minimal_refinements1, running_time1, _, \
            provenance_time1, search_time1 = \
            ps.FindMinimalRefinement(data_file_prefix, separator, query_file, constraint_file, data_format, time_limit)

        print("running time = {}".format(running_time1))
        print(*minimal_refinements1, sep="\n")

        running_time2, provenance_time2, search_time2 = 0, 0, 0

        # print("========================== lattice traversal ===================================")
        # minimal_refinements2, minimal_added_refinements2, running_time2, provenance_time2, search_time2 = \
        #     lt.FindMinimalRefinement(data_file_prefix, separator, query_file, constraint_file, time_limit)
        # if running_time2 > time_limit:
        #     print("naive alg out of time with {} time limit".format(time_limit))
        # else:
        #     print("running time = {}".format(running_time2))
        # print(*minimal_refinements2, sep="\n")

        result_output.write("\n")
        idx = i
        if running_time2 < time_limit:
            time_output.write("{},{:0.2f},{:0.2f},{:0.2f},"
                              "{:0.2f},{:0.2f},{:0.2f}\n".format(idx, running_time1, provenance_time1, search_time1,
                                                                 running_time2, provenance_time2, search_time2))
        else:
            time_output.write("{},{:0.2f},{:0.2f},{:0.2f},,,\n".format(idx, running_time1, provenance_time1,
                                                                       search_time1))
        result_output.write("{}\n".format(idx))
        result_output.write(",".join(str(item) for item in minimal_added_refinements1))
        result_output.write("\n")
        result_output.write("\n".join(str(item) for item in minimal_refinements1))
        result_output.write("\n")
    result_output.close()
    time_output.close()


separator = ','
data_format = ".csv"
run_constraint(1, "relax1")
