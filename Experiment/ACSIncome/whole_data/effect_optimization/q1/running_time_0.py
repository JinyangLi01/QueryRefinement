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

from Algorithm import ProvenanceSearchValues_8_20230119 as ps
from Algorithm import LatticeTraversal_5_20230121 as lt
from Algorithm import ProvenanceSearchValues_8_no_optimization as ps_no_optimization


data_file_prefix = r"../../../data/"
query_file_prefix = r"./q"
constraint_file_prefix = r"./"
time_output_prefix = r"./result_"


def file(q, c):
    time_output_file = time_output_prefix + str(q) + str(c) + ".csv"
    time_output = open(time_output_file, "w")
    time_output.write("QC,ps,ps_prov,ps_search,ps_noopt,ps_noopt_prov,ps_noopt_search\n")
    return time_output

result_output_file = r"./running_time_result.txt"
result_output = open(result_output_file, "w")
result_output.write("QC,ps,ps_prov,ps_search,ps_noopt,ps_noopt_prov,ps_noopt_search\n")


time_limit = 60 * 60
separator = ','

def compare(q, c, time_output):
    print("run with query{} constraint{}".format(q, c))
    result_output.write("query{} constraint{}\n".format(q, c))
    query_file = query_file_prefix + str(q) + ".json"
    constraint_file = constraint_file_prefix + str(c) + ".json"

    print("========================== provenance search ===================================")
    minimal_refinements1, _, running_time1, _, \
    provenance_time1, search_time1 = \
        ps.FindMinimalRefinement(data_file_prefix, separator, query_file, constraint_file, data_file_format, time_limit)

    print("running time = {}".format(running_time1))
    print(*minimal_refinements1, sep="\n")

    print("========================== provenance search without optimization  ===================================")

    minimal_refinements2, running_time2, _, \
        provenance_time2, search_time2 = \
        ps_no_optimization.FindMinimalRefinement(data_file_prefix, separator, query_file, constraint_file, data_file_format, time_limit)

    print("running time = {}".format(running_time2))
    print(*minimal_refinements2, sep="\n")

    # print("========================== baseline  ===================================")
    #
    #
    # minimal_refinements3, _, running_time3, \
    #     provenance_time3, search_time3 = \
    #     lt.FindMinimalRefinement(data_file_prefix, separator, query_file, constraint_file,
    #                                              data_file_format, time_limit)
    #
    # print("running time = {}".format(running_time3))
    # print(*minimal_refinements3, sep="\n")

    time_output.write("\n")
    idx = "Q" + str(q) + "C" + str(c)

    time_output.write("{},{:0.4f},{:0.4f},{:0.4f},"
                      "{:0.4f},{:0.4f},{:0.4f}\n\n".format(idx, running_time1, provenance_time1, search_time1,
                                                         running_time2, provenance_time2, search_time2))
    time_output.write("{}\n\n".format(minimal_refinements1))
    time_output.write("{}\n\n".format(minimal_refinements2))
    # time_output.write("{}\n\n".format(minimal_refinements3))

    result_output.write("{},{:0.4f},{:0.4f},{:0.4f},"
                      "{:0.4f},{:0.4f},{:0.4f}\n".format(idx, running_time1, provenance_time1, search_time1,
                                                         running_time2, provenance_time2, search_time2))


summary_file = open(r"time1.csv", "w")
summary_file.write("file,PS,LT\n")

data_file_format = '.csv'

def run(q, c):
    time_output = file(q, c)
    compare(q, c, time_output)
    time_output.close()


run(1, "constraint_relax1")
# run(1, 2)
# run(1, 3)
# run(2, 1)
# run(2, 2)
# run(2, 3)
